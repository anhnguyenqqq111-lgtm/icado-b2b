/**
 * Ollama Integration — Local AI for SEO Analysis
 *
 * Uses Ollama API (http://localhost:11434) with gemma3:4b model.
 * Drop-in replacement for gemini.js with same interface.
 */

const { spawn, execSync } = require('child_process');

const OLLAMA_BASE = process.env.OLLAMA_URL || 'http://localhost:11434';
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || 'gemma3:4b';
const OLLAMA_EXE = process.env.OLLAMA_PATH || 'C:\\Users\\MSI\\AppData\\Local\\Programs\\Ollama\\ollama.exe';

let ollamaProcess = null;

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

/**
 * Start Ollama process
 */
async function startOllama() {
    if (await isAvailable()) return { started: false, message: 'Already running' };

    try {
        ollamaProcess = spawn(OLLAMA_EXE, ['serve'], {
            detached: true,
            stdio: 'ignore',
            windowsHide: true,
        });
        ollamaProcess.unref();

        // Wait up to 10s for Ollama to be ready
        for (let i = 0; i < 20; i++) {
            await sleep(500);
            if (await isAvailable()) {
                console.log('[Ollama] ✅ Started successfully');
                return { started: true, message: 'Ollama started' };
            }
        }
        return { started: false, message: 'Ollama started but not responding' };
    } catch (err) {
        return { started: false, message: err.message };
    }
}

/**
 * Stop Ollama process
 */
async function stopOllama() {
    try {
        execSync('taskkill /F /IM ollama.exe /T 2>nul', { stdio: 'ignore' });
        ollamaProcess = null;
        console.log('[Ollama] ⏹ Stopped');
        return { stopped: true };
    } catch {
        return { stopped: false, message: 'Ollama not running or cannot stop' };
    }
}

/**
 * Check if Ollama is available
 */
async function isAvailable() {
    try {
        const res = await fetch(`${OLLAMA_BASE}/api/tags`, { signal: AbortSignal.timeout(3000) });
        return res.ok;
    } catch {
        return false;
    }
}

/**
 * Call Ollama API
 */
async function callOllama(prompt, options = {}) {
    const { temperature = 0.3, maxTokens = 4096, jsonMode = true } = options;

    const body = {
        model: OLLAMA_MODEL,
        prompt,
        stream: false,
        options: {
            temperature,
            num_predict: maxTokens,
        },
    };

    if (jsonMode) {
        body.format = 'json';
    }

    const response = await fetch(`${OLLAMA_BASE}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        throw new Error(`Ollama error ${response.status}: ${await response.text()}`);
    }

    const data = await response.json();
    const text = data.response || '';

    if (jsonMode) {
        try {
            return JSON.parse(text);
        } catch {
            // Try to extract JSON from response
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            if (jsonMatch) return JSON.parse(jsonMatch[0]);
            throw new Error('Could not parse Ollama JSON response');
        }
    }

    return text;
}

/**
 * Analyze keywords and rankings — SEO insights
 */
async function analyzeKeywords(keywords, rankings) {
    const keywordData = keywords.slice(0, 100).map(kw => {
        const rank = rankings.find(r => r.keyword === kw.keyword);
        return {
            keyword: kw.keyword,
            rank: rank?.position || 'Not ranked',
            url: rank?.url || '',
        };
    });

    const prompt = `You are an SEO expert. Analyze these keyword rankings and provide actionable insights.

Keywords data (keyword | rank | url):
${keywordData.map(k => `- "${k.keyword}" | Rank: ${k.rank} | ${k.url}`).join('\n')}

Respond in JSON format with EXACTLY this structure:
{
  "topics": [
    {
      "name": "Topic cluster name",
      "priority": "high",
      "keywords": ["keyword1", "keyword2"],
      "suggestedTitle": "Suggested article title",
      "reason": "Why this topic matters"
    }
  ],
  "suggestions": [
    {
      "type": "new_content",
      "title": "Action title",
      "description": "What to do and why",
      "priority": "high",
      "keywords": ["related keywords"]
    }
  ]
}

Types can be: new_content, optimize, merge, internal_link.
Priority can be: high, medium, low.
Focus on Vietnamese market SEO. Be specific and actionable. Respond in Vietnamese.`;

    return await callOllama(prompt);
}

/**
 * Generate content brief from SERP data
 */
async function generateContentBrief(keyword, serpData) {
    const paaText = serpData.paa?.length > 0 ? `\nPeople Also Ask:\n${serpData.paa.map(q => `- ${q}`).join('\n')}` : '';
    const relatedText = serpData.relatedSearches?.length > 0 ? `\nRelated Searches:\n${serpData.relatedSearches.map(r => `- ${r}`).join('\n')}` : '';
    const competitorText = serpData.competitors?.length > 0 ? `\nTop Competitors:\n${serpData.competitors.map(c => `- ${c.domain}: "${c.title}"`).join('\n')}` : '';

    const prompt = `You are an SEO content strategist. Create a content brief for this keyword.

Target Keyword: "${keyword}"
${paaText}
${relatedText}
${competitorText}

Respond in JSON format:
{
  "title": "Suggested article title (Vietnamese, SEO-optimized)",
  "searchIntent": "informational/commercial/transactional/navigational",
  "targetWordCount": 2000,
  "outline": [
    {"heading": "H2 heading text", "points": ["key point 1", "key point 2"]},
  ],
  "paaToAnswer": ["questions to answer in the article"],
  "internalLinkSuggestions": ["related topics to link to"],
  "metaDescription": "SEO meta description (155 chars max)"
}

Write everything in Vietnamese. Be specific and practical.`;

    return await callOllama(prompt, { maxTokens: 6144 });
}

/**
 * Classify keyword intents in batch
 */
async function classifyIntents(keywords) {
    const kwList = keywords.slice(0, 50).map(k => k.keyword || k);

    const prompt = `Classify the search intent of each keyword.

Keywords:
${kwList.map((k, i) => `${i + 1}. ${k}`).join('\n')}

Respond in JSON format:
{
  "classifications": [
    {"keyword": "...", "intent": "informational|commercial|transactional|navigational", "confidence": 0.9}
  ]
}`;

    return await callOllama(prompt);
}

/**
 * Get Ollama model info
 */
async function getModelInfo() {
    try {
        const res = await fetch(`${OLLAMA_BASE}/api/tags`);
        const data = await res.json();
        return {
            available: true,
            provider: 'ollama',
            model: OLLAMA_MODEL,
            models: data.models?.map(m => ({ name: m.name, size: m.size })) || [],
        };
    } catch {
        return { available: false, provider: 'ollama', model: OLLAMA_MODEL, models: [] };
    }
}

module.exports = {
    callOllama,
    analyzeKeywords,
    generateContentBrief,
    classifyIntents,
    isAvailable,
    getModelInfo,
    startOllama,
    stopOllama,
};
