const express = require('express');
const path = require('path');
const db = require('./src/database');
const sheets = require('./src/sheets');
const gemini = require('./src/gemini');
const ollama = require('./src/ollama');
const checker = require('./src/checker');
const warp = require('./src/warp');
const scheduler = require('./src/scheduler');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// OAuth callback — catch ?code= from Google on ANY path (handles /, /oauth/callback, etc.)
app.use(async (req, res, next) => {
    if (req.query.code && !req.path.startsWith('/api/')) {
        try {
            console.log(`[OAuth] Received code on path: ${req.path}`);
            await sheets.getAuthClient();
            await sheets.exchangeAuthCode(req.query.code);
            console.log('[OAuth] ✅ Token saved!');
            return res.redirect('/');
        } catch (err) {
            console.error('[OAuth] ❌ Failed:', err.message);
            return res.redirect('/?auth_error=' + encodeURIComponent(err.message));
        }
    }
    next();
});

app.use(express.static(path.join(__dirname, 'public')));

// ============ SSE Clients ============

let sseClients = [];

function sendSSE(data) {
    const msg = `data: ${JSON.stringify(data)}\n\n`;
    sseClients = sseClients.filter(res => {
        try { res.write(msg); return true; }
        catch { return false; }
    });
}

// ============ Project API ============

app.get('/api/projects', async (req, res) => {
    try {
        const sheetProjects = await sheets.listProjects();
        const localProjects = db.getProjects();

        // Merge: sheet projects with domain + local projects
        const projectMap = {};
        for (const p of sheetProjects) {
            projectMap[p.name || p] = { name: p.name || p, domain: p.domain || '' };
        }
        for (const name of localProjects) {
            if (!projectMap[name]) projectMap[name] = { name, domain: '' };
        }

        res.json({ projects: Object.values(projectMap) });
    } catch (err) {
        console.error('Error listing projects:', err);
        res.json({ projects: db.getProjects().map(name => ({ name, domain: '' })) });
    }
});

app.delete('/api/projects/:project', (req, res) => {
    try {
        const result = db.deleteProject(req.params.project);
        res.json({ success: true, ...result });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Keyword Management ============

app.get('/api/keywords/:project', (req, res) => {
    const keywords = db.getKeywords(req.params.project);
    res.json({ keywords });
});

app.post('/api/keywords/:project', (req, res) => {
    try {
        const { project } = req.params;
        const { keywords } = req.body;
        if (!keywords || !Array.isArray(keywords)) {
            return res.status(400).json({ error: 'keywords must be an array of strings' });
        }
        const saved = db.saveKeywordsOnly(project, keywords);
        res.json({ success: true, added: saved });
    } catch (err) {
        console.error('Error adding keywords:', err);
        res.status(500).json({ error: err.message });
    }
});

app.delete('/api/keywords/:project', (req, res) => {
    try {
        const result = db.deleteKeywords(req.params.project);
        res.json({ success: true, ...result });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get keywords from Google Sheet for a project
app.get('/api/keywords-sheet/:project', async (req, res) => {
    try {
        const keywords = await sheets.getKeywordsForProject(req.params.project);
        res.json({ keywords });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Sync from Google Sheet ============

app.post('/api/sync/:project', async (req, res) => {
    try {
        const { project } = req.params;
        console.log(`[Sync] Starting sync for "${project}"...`);

        const existingKeywords = db.getKeywords(project);
        const sheetRows = await sheets.getSheetData(project);
        if (!sheetRows || sheetRows.length === 0) {
            return res.status(404).json({ error: 'No ranking data found in Google Sheet' });
        }

        const enrichedRows = sheetRows.map(row => {
            if (row.keyword && row.keyword.trim()) return row;
            const kw = existingKeywords.find(k => k.stt === row.stt);
            return { ...row, keyword: kw ? kw.keyword : `Keyword #${row.stt}` };
        });

        const imported = db.importSheetData(project, enrichedRows);
        const lastSync = db.getLastSync(project);
        const keywordsInSheet = enrichedRows.filter(r => r.keyword && !r.keyword.startsWith('Keyword #')).length;

        console.log(`[Sync] Imported ${imported} new rankings for "${project}" (${keywordsInSheet} keywords from sheet)`);
        res.json({
            success: true, imported, lastSync,
            totalRows: sheetRows.length,
            hasKeywords: existingKeywords.length > 0 || keywordsInSheet > 0,
            keywordCount: Math.max(existingKeywords.length, enrichedRows.length),
        });
    } catch (err) {
        console.error('Sync error:', err);
        res.status(500).json({ error: err.message });
    }
});

// ============ Rankings ============

app.get('/api/rankings/:project', (req, res) => {
    try {
        const rankings = db.getLatestRankings(req.params.project);
        res.json({ rankings });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/history/:project/:keyword', (req, res) => {
    try {
        const history = db.getKeywordHistory(req.params.project, decodeURIComponent(req.params.keyword));
        res.json({ history });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/stats/:project', (req, res) => {
    try {
        const stats = db.getStats(req.params.project);
        const lastSync = db.getLastSync(req.params.project);
        res.json({ stats: stats || {}, lastSync });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Raw Sheet Data ============

app.get('/api/sheet/:project', async (req, res) => {
    try {
        const data = await sheets.getSheetData(req.params.project);
        res.json({ data, count: data.length });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Native Checker Control ============

app.post('/api/checker/start', async (req, res) => {
    try {
        const { project, domain, keywords, options } = req.body;

        if (!project) {
            return res.status(400).json({ error: 'Project name is required' });
        }

        // Get domain: from request, from sheet projects, or from settings
        let targetDomain = domain || '';
        if (!targetDomain) {
            // Try to find domain from sheet projects
            const projects = await sheets.listProjects();
            const proj = projects.find(p => p.name === project);
            if (proj?.domain) targetDomain = proj.domain;
        }
        if (!targetDomain) {
            return res.status(400).json({ error: 'Domain is required' });
        }

        // Get keywords: from request, from Sheet (Keyword_KPI), or from DB
        let kwList = keywords || [];
        if (kwList.length === 0) {
            // Try Google Sheet first (Keyword_KPI → match by DỰ ÁN)
            kwList = await sheets.getKeywordsForProject(project);
            // Fall back to DB
            if (kwList.length === 0) {
                const dbKws = db.getKeywords(project);
                kwList = dbKws.map(k => k.keyword);
            }
        }

        if (kwList.length === 0) {
            return res.status(400).json({ error: 'No keywords found' });
        }

        // Resume: skip keywords already checked within 72 hours
        const totalBeforeResume = kwList.length;
        const recentlyChecked = db.getRecentlyCheckedKeywords(project, 72);
        if (recentlyChecked.size > 0) {
            kwList = kwList.filter(kw => !recentlyChecked.has(kw));
            const skipped = totalBeforeResume - kwList.length;
            if (skipped > 0) {
                console.log(`[Checker] Resume: skipping ${skipped} keywords checked within 72h, ${kwList.length} remaining`);
            }
        }

        if (kwList.length === 0) {
            return res.json({ success: false, message: `Tất cả ${totalBeforeResume} keywords đã được check trong 72h qua` });
        }

        // Merge settings
        const settings = sheets.getSettings();
        const checkerOptions = {
            maxPages: options?.maxPages ?? 5,
            chunkSize: options?.chunkSize ?? 5,
            uuleLocation: options?.uuleLocation || settings.UULE_CODE || '',
        };

        // Start checker (runs in background, returns sync)
        await db.initDatabase();
        const result = await checker.startChecker({
            project,
            domain: targetDomain,
            keywords: kwList,
            options: checkerOptions,
            db,
        });

        if (result.success) {
            // Listen for results and stream via SSE
            checker.onResult(r => sendSSE({ type: 'result', ...r }));
        }

        res.json(result);
    } catch (err) {
        console.error('Checker start error:', err);
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/checker/stop', (req, res) => {
    res.json(checker.stopChecker());
});

app.post('/api/checker/pause', (req, res) => {
    res.json(checker.pauseChecker());
});

app.get('/api/checker/status', (req, res) => {
    res.json(checker.getStatus());
});

app.post('/api/rankings/wipe', (req, res) => {
    try {
        const { project, count } = req.body;
        if (!project) return res.status(400).json({ error: 'Project required' });
        const deleted = db.wipeRankings(project, count || 0);
        res.json({ success: true, deleted });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// SSE endpoint for real-time results
app.get('/api/checker/stream', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.flushHeaders();

    // Send current status immediately
    res.write(`data: ${JSON.stringify({ type: 'status', ...checker.getStatus() })}\n\n`);

    sseClients.push(res);

    req.on('close', () => {
        sseClients = sseClients.filter(c => c !== res);
    });
});

// ============ WARP VPN Control ============

app.get('/api/warp/status', async (req, res) => {
    const status = await warp.warpStatus();
    res.json({ status, installed: status !== 'not_installed' });
});

app.post('/api/warp/toggle', async (req, res) => {
    try {
        const result = await warp.warpToggle();
        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/warp/reset', async (req, res) => {
    try {
        const result = await warp.warpReset();
        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Scheduler ============

app.post('/api/scheduler/start', async (req, res) => {
    try {
        const { project, domain, options, schedule } = req.body;

        const task = async () => {
            // Build keywords list
            let kwList = [];
            const dbKws = db.getKeywords(project);
            if (dbKws.length > 0) {
                kwList = dbKws.map(k => k.keyword);
            } else {
                kwList = await sheets.getKeywordsForProject(project);
            }

            if (kwList.length === 0) {
                console.log('[Scheduler] No keywords found, skipping');
                return;
            }

            const settings = sheets.getSettings();
            await checker.startChecker({
                project,
                domain: domain || '',
                keywords: kwList,
                options: {
                    maxPages: options?.maxPages ?? 5,
                    chunkSize: options?.chunkSize ?? 5,
                    uuleLocation: options?.uuleLocation || settings.UULE_CODE || '',
                },
                db,
            });
        };

        const result = scheduler.start(task, schedule);
        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/scheduler/stop', (req, res) => {
    res.json(scheduler.stop());
});

app.get('/api/scheduler/status', (req, res) => {
    res.json(scheduler.getStatus());
});

// ============ Settings ============

app.get('/api/settings', (req, res) => {
    try {
        const s = sheets.getSettings();
        // Don't expose secrets
        res.json({
            GOOGLE_SHEET_ID: s.GOOGLE_SHEET_ID || '',
            UULE_CODE: s.UULE_CODE || '',
            SHEET_HEADERS: s.SHEET_HEADERS || [],
            HEADER_MAP: s.HEADER_MAP || {},
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/settings', (req, res) => {
    try {
        sheets.saveSettings(req.body);
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ SERP Intelligence Data ============

app.get('/api/serp-data/:project', (req, res) => {
    try {
        const data = db.getSerpData(req.params.project);
        // Aggregate: unique PAA questions, related searches, top competitors
        const allPAA = {};
        const allRelated = {};
        const allCompetitors = {};

        data.forEach(d => {
            d.paa.forEach(q => { allPAA[q] = (allPAA[q] || 0) + 1; });
            d.relatedSearches.forEach(r => { allRelated[r] = (allRelated[r] || 0) + 1; });
            d.competitors.forEach(c => {
                if (!allCompetitors[c.domain]) allCompetitors[c.domain] = { domain: c.domain, count: 0, urls: [] };
                allCompetitors[c.domain].count++;
                if (!allCompetitors[c.domain].urls.find(u => u.url === c.url)) {
                    allCompetitors[c.domain].urls.push({ url: c.url, title: c.title });
                }
            });
        });

        res.json({
            keywords: data,
            aggregate: {
                paa: Object.entries(allPAA).sort((a, b) => b[1] - a[1]).map(([q, count]) => ({ question: q, count })),
                relatedSearches: Object.entries(allRelated).sort((a, b) => b[1] - a[1]).map(([r, count]) => ({ query: r, count })),
                competitors: Object.values(allCompetitors).sort((a, b) => b.count - a.count),
            },
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Ranking Trend ============

app.get('/api/rankings/trend/:project', (req, res) => {
    try {
        const keyword = req.query.keyword;
        if (keyword) {
            // Single keyword trend
            const history = db.getKeywordHistory(req.params.project, keyword, 60);
            res.json({ keyword, history });
        } else {
            // All keywords latest rankings for project overview
            const rankings = db.getLatestRankings(req.params.project);
            res.json({ rankings });
        }
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Google Sheets OAuth ============

app.get('/api/sheets/auth-url', async (req, res) => {
    try {
        const auth = await sheets.getAuthClient();
        if (auth?.credentials?.access_token) {
            return res.json({ authenticated: true });
        }
        const url = sheets.getAuthUrl();
        res.json({ authenticated: false, authUrl: url });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ AI Insights (Ollama primary, Gemini fallback) ============

const analysisProgress = {};

// AI provider status
app.get('/api/ai/provider', async (req, res) => {
    const ollamaInfo = await ollama.getModelInfo();
    const geminiAvailable = gemini.API_KEYS?.length > 0;
    res.json({
        active: ollamaInfo.available ? 'ollama' : (geminiAvailable ? 'gemini' : 'none'),
        ollama: ollamaInfo,
        gemini: { available: geminiAvailable, keys: gemini.API_KEYS?.length || 0 },
    });
});

// Start/Stop Ollama from Dashboard
app.post('/api/ai/ollama/start', async (req, res) => {
    const result = await ollama.startOllama();
    res.json(result);
});

app.post('/api/ai/ollama/stop', async (req, res) => {
    const result = await ollama.stopOllama();
    res.json(result);
});

app.get('/api/ai/insights/:project', async (req, res) => {
    try {
        await db.initDatabase();
        const insights = db.getAiInsights(req.params.project);
        const ollamaAvail = await ollama.isAvailable();
        res.json({ insights, hasAI: ollamaAvail || gemini.API_KEYS?.length > 0 });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/ai/progress/:project', (req, res) => {
    const prog = analysisProgress[req.params.project];
    res.json(prog || { status: 'idle' });
});

app.post('/api/ai/analyze/:project', async (req, res) => {
    try {
        const { project } = req.params;
        const ollamaAvail = await ollama.isAvailable();
        const geminiAvail = gemini.API_KEYS?.length > 0;

        if (!ollamaAvail && !geminiAvail) {
            return res.status(400).json({ error: 'No AI available. Start Ollama or add Gemini API key.' });
        }
        if (analysisProgress[project]?.status === 'running') {
            return res.status(409).json({ error: 'Analysis already running' });
        }

        await db.initDatabase();
        const rankings = db.getLatestRankings(project);
        if (!rankings || rankings.length === 0) {
            return res.status(404).json({ error: 'No ranking data. Sync first.' });
        }

        const kwData = rankings.map(r => ({
            stt: r.stt,
            keyword: r.keyword || `Keyword #${r.stt}`,
            position: r.position,
            url: r.url || '',
        }));

        const provider = ollamaAvail ? 'ollama' : 'gemini';
        analysisProgress[project] = {
            status: 'running', provider, processed: 0, total: kwData.length,
            startedAt: new Date().toISOString(),
        };

        res.json({ started: true, provider, totalKeywords: kwData.length });

        try {
            console.log(`[AI] Starting ${provider} analysis for "${project}" (${kwData.length} keywords)...`);
            let insights;

            if (provider === 'ollama') {
                insights = await ollama.analyzeKeywords(kwData, rankings);
            } else {
                insights = await gemini.analyzeProject(project, kwData, (progress) => {
                    analysisProgress[project] = { status: 'running', provider, ...progress };
                });
            }

            db.saveAiInsights(project, insights);
            analysisProgress[project] = { status: 'done', provider };
            console.log(`[AI] ✅ Analysis done via ${provider}`);
        } catch (err) {
            console.error(`[AI] ❌ Analysis failed:`, err.message);
            analysisProgress[project] = { status: 'error', error: err.message };
        }
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Content Brief generation from SERP data
app.post('/api/ai/content-brief', async (req, res) => {
    try {
        const { keyword, project } = req.body;
        if (!keyword) return res.status(400).json({ error: 'Keyword required' });

        const ollamaAvail = await ollama.isAvailable();
        if (!ollamaAvail) return res.status(400).json({ error: 'Ollama not available. Start Ollama first.' });

        // Get SERP data for this keyword
        await db.initDatabase();
        const serpDataAll = db.getSerpData(project || '');
        const kwSerp = serpDataAll.find(s => s.keyword === keyword) || { paa: [], relatedSearches: [], competitors: [] };

        const brief = await ollama.generateContentBrief(keyword, kwSerp);
        res.json({ brief });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Intent classification
app.post('/api/ai/intents', async (req, res) => {
    try {
        const { keywords } = req.body;
        if (!keywords?.length) return res.status(400).json({ error: 'Keywords array required' });

        const ollamaAvail = await ollama.isAvailable();
        if (!ollamaAvail) return res.status(400).json({ error: 'Ollama not available' });

        const result = await ollama.classifyIntents(keywords);
        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// ============ Start Server ============

async function start() {
    await db.initDatabase();
    console.log('  ✅ Database initialized');

    // Initialize OAuth (non-blocking)
    sheets.getAuthClient().catch(() => { });

    app.listen(PORT, () => {
        console.log(`\n  🚀 Rank Dashboard running at http://localhost:${PORT}\n`);
    });
}

start().catch(err => {
    console.error('Failed to start server:', err);
    process.exit(1);
});
