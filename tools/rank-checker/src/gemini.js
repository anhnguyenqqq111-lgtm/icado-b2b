const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const API_KEYS = [
    process.env.GEMINI_API_KEY_1,
    process.env.GEMINI_API_KEY_2,
].filter(Boolean);

let currentKeyIndex = 0;
const GEMINI_MODEL = 'gemini-2.0-flash';
const API_BASE = 'https://generativelanguage.googleapis.com/v1beta/models';
const BATCH_SIZE = 200; // keywords per request
const RATE_LIMIT_DELAY = 4500; // ms between requests (safe for 15 req/min)

function getNextKey() {
    const key = API_KEYS[currentKeyIndex % API_KEYS.length];
    currentKeyIndex++;
    return key;
}

/**
 * Call Gemini API with automatic key rotation and retry on 429
 */
async function callGemini(prompt, maxTokens = 8192, retries = 3) {
    for (let attempt = 0; attempt <= retries; attempt++) {
        const apiKey = getNextKey();
        const url = `${API_BASE}/${GEMINI_MODEL}:generateContent?key=${apiKey}`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: prompt }] }],
                    generationConfig: {
                        temperature: 0.3,
                        maxOutputTokens: maxTokens,
                        responseMimeType: 'application/json',
                    },
                }),
            });

            if (response.status === 429) {
                const waitMs = Math.min(5000 * Math.pow(2, attempt), 60000);
                console.log(`[AI] Rate limited (429), retrying in ${waitMs / 1000}s (attempt ${attempt + 1}/${retries})...`);
                await sleep(waitMs);
                continue;
            }

            if (!response.ok) {
                const err = await response.text();
                throw new Error(`Gemini API error ${response.status}: ${err}`);
            }

            const data = await response.json();
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
            if (!text) throw new Error('Empty response from Gemini');

            try {
                return JSON.parse(text);
            } catch {
                // Try to extract JSON from the response
                const jsonMatch = text.match(/\{[\s\S]*\}/);
                if (jsonMatch) return JSON.parse(jsonMatch[0]);
                return { raw: text };
            }
        } catch (err) {
            if (attempt === retries) throw err;
            console.log(`[AI] Error on attempt ${attempt + 1}: ${err.message}`);
            await sleep(3000);
        }
    }
    throw new Error('All Gemini API retry attempts exhausted');
}

/**
 * Analyze keywords for a project — topic clustering + audit suggestions
 */
async function analyzeProject(projectName, keywords, progressCallback) {
    // keywords = [{ keyword, position, url, stt }, ...]
    const batches = [];
    for (let i = 0; i < keywords.length; i += BATCH_SIZE) {
        batches.push(keywords.slice(i, i + BATCH_SIZE));
    }

    const allTopics = [];
    const allSuggestions = [];

    for (let i = 0; i < batches.length; i++) {
        const batch = batches[i];
        if (progressCallback) {
            progressCallback({
                batch: i + 1,
                totalBatches: batches.length,
                processed: Math.min((i + 1) * BATCH_SIZE, keywords.length),
                total: keywords.length,
            });
        }

        try {
            const result = await analyzeBatch(projectName, batch, i, batches.length);
            if (result.topics) allTopics.push(...result.topics);
            if (result.suggestions) allSuggestions.push(...result.suggestions);
        } catch (err) {
            console.error(`[AI] Batch ${i + 1} error:`, err.message);
        }

        // Rate limit delay between batches
        if (i < batches.length - 1) {
            await sleep(RATE_LIMIT_DELAY);
        }
    }

    // Merge and deduplicate topics
    const mergedTopics = mergeTopics(allTopics);

    return {
        project: projectName,
        analyzedAt: new Date().toISOString(),
        totalKeywords: keywords.length,
        topics: mergedTopics,
        suggestions: allSuggestions,
    };
}

async function analyzeBatch(projectName, batch, batchIdx, totalBatches) {
    const keywordList = batch.map(k => {
        const pos = k.position && k.position > 0 ? `#${k.position}` : 'N/A';
        const url = k.url || 'no-url';
        return `${k.stt}. "${k.keyword}" → pos: ${pos}, url: ${url}`;
    }).join('\n');

    const prompt = `Bạn là chuyên gia SEO phân tích keywords cho dự án "${projectName}".

DANH SÁCH KEYWORDS (batch ${batchIdx + 1}/${totalBatches}):
${keywordList}

HÃY PHÂN TÍCH VÀ TRẢ VỀ JSON:

{
  "topics": [
    {
      "name": "Tên nhóm chủ đề (ngắn gọn, tiếng Việt)",
      "keywords": ["keyword1", "keyword2", ...],
      "mainKeyword": "keyword chính của nhóm",
      "suggestedTitle": "Tiêu đề bài viết gợi ý cho nhóm này",
      "priority": "high|medium|low",
      "reason": "Lý do ưu tiên (1 câu)"
    }
  ],
  "suggestions": [
    {
      "type": "new_content|optimize|merge|internal_link",
      "keywords": ["keyword liên quan"],
      "title": "Tiêu đề/hành động gợi ý",
      "description": "Mô tả chi tiết (2-3 câu)",
      "priority": "high|medium|low"
    }
  ]
}

QUY TẮC:
1. Gom keywords có ngữ nghĩa gần nhau thành 1 topic
2. Keywords ranking N/A → gợi ý "new_content"
3. Keywords cùng URL nhiều → kiểm tra nên tách hay gộp
4. Keywords ranking 11-50 → gợi ý "optimize"
5. Keywords ranking tốt nhưng URL khác nhau cùng chủ đề → gợi ý "internal_link"
6. Keywords trùng ý → gợi ý "merge"
7. Trả về tiếng Việt, ngắn gọn, thực tế`;

    return await callGemini(prompt);
}

/**
 * Merge topic clusters from multiple batches
 */
function mergeTopics(topics) {
    const merged = {};
    for (const t of topics) {
        const key = t.name?.toLowerCase().trim();
        if (!key) continue;

        if (merged[key]) {
            // Merge keywords
            const existing = merged[key];
            const kwSet = new Set([...existing.keywords, ...t.keywords]);
            existing.keywords = [...kwSet];
            // Keep higher priority
            if (t.priority === 'high') existing.priority = 'high';
        } else {
            merged[key] = { ...t };
        }
    }
    return Object.values(merged).sort((a, b) => {
        const pri = { high: 0, medium: 1, low: 2 };
        return (pri[a.priority] || 2) - (pri[b.priority] || 2);
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
    analyzeProject,
    callGemini,
    API_KEYS,
};
