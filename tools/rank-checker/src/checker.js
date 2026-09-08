/**
 * Native Rank Checker Engine
 * Port from Python v4.1.py RankChecker class
 *
 * Uses Puppeteer (headless Chrome) to search Google and find keyword rankings.
 * Supports: chunked parallel execution, CAPTCHA solving, WARP retry, UULE geo-targeting
 */

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const uule = require('./uule');
const warp = require('./warp');
const captchaSolver = require('./captcha-solver');
const sheets = require('./sheets');

puppeteer.use(StealthPlugin());

// ============ Constants ============

const DEFAULT_MAX_PAGES = 5;
const DEFAULT_CHUNK_SIZE = 5;
const PAGE_LOAD_TIMEOUT = 30000;
const SEARCH_RESULT_TIMEOUT = 5000;
const CAPTCHA_RESET_THRESHOLD = 5; // Auto-reset WARP after this many consecutive CAPTCHAs

// CAPTCHA counter for auto-WARP-reset
let consecutiveCaptchas = 0;

// ============ Utility functions ============

function normalizeDomain(url) {
    if (!url) return '';
    if (!url.includes('://')) url = 'https://' + url;
    try {
        const parsed = new URL(url);
        let host = parsed.hostname.toLowerCase();
        if (host.startsWith('www.')) host = host.slice(4);
        return host;
    } catch {
        return '';
    }
}

function extractRealHref(href) {
    if (!href) return '';
    if (href.startsWith('/url?')) {
        try {
            const url = new URL(href, 'https://www.google.com');
            return url.searchParams.get('q') || href;
        } catch {
            return href;
        }
    }
    return href;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============ Browser Management ============

/**
 * Launch a Puppeteer browser with anti-detection options
 */
async function launchBrowser() {
    const args = [
        '--no-default-browser-check',
        '--disable-blink-features=AutomationControlled',
        '--window-size=400,700',
        '--disable-notifications',
        '--disable-geolocation',
        '--disable-translate',
        '--disable-cache',
        '--disable-features=IsolateOrigins,site-per-process',
        '--lang=vi',
        '--disable-dev-shm-usage',
        '--no-sandbox',
    ];

    return puppeteer.launch({
        headless: false,
        args,
        defaultViewport: { width: 400, height: 700 },
        ignoreHTTPSErrors: true,
    });
}

// ============ CAPTCHA Detection ============

/**
 * Check if the page has a CAPTCHA
 * @returns {{ hasCaptcha: boolean, type: string|null }}
 */
async function checkCaptcha(page) {
    try {
        // Check for reCAPTCHA iframes
        const frames = page.frames();
        for (const frame of frames) {
            const url = frame.url() || '';
            if (url.includes('recaptcha') && url.includes('anchor')) {
                return { hasCaptcha: true, type: 'iframe_checkbox' };
            }
            if (url.includes('recaptcha') && url.includes('bframe')) {
                return { hasCaptcha: true, type: 'iframe_challenge' };
            }
        }

        // Check for captcha form elements
        const hasCaptchaForm = await page.evaluate(() => {
            return !!(
                document.getElementById('captcha-form') ||
                document.querySelector('.g-recaptcha') ||
                document.querySelector("[action*='sorry']")
            );
        });
        if (hasCaptchaForm) return { hasCaptcha: true, type: 'html_captcha' };

        // Check page title
        const title = await page.title();
        const lowerTitle = (title || '').toLowerCase();
        if (lowerTitle.includes('unusual traffic') || lowerTitle.includes('sorry')) {
            return { hasCaptcha: true, type: 'google_sorry' };
        }
    } catch { }

    return { hasCaptcha: false, type: null };
}

// ============ Core Search Logic ============

/**
 * Get the local location text from Google search footer
 */
async function getLocalLocation(page) {
    try {
        const selectors = [
            '#footcnt span.dfB0uf', '#fbarcnt span.dfB0uf', 'footer span.dfB0uf',
            '#footcnt span.Q8LRLc', '#fbarcnt span.Q8LRLc', 'footer span.Q8LRLc',
        ];

        for (const selector of selectors) {
            try {
                const text = await page.$eval(selector, el => el.textContent?.trim());
                if (text) return text;
            } catch { }
        }
    } catch { }
    return '-';
}

/**
 * Extract search result hrefs from the current page
 */
async function extractSearchResults(page) {
    try {
        return await page.evaluate(() => {
            const selectors = [
                '#res .tF2Cxc a[href]:has(>h3)',
                '.yuRUbf a[href]',
                '.egMi0.kCrYT a[href]',
            ];
            const allLinks = [];
            for (const sel of selectors) {
                document.querySelectorAll(sel).forEach(a => {
                    const href = a.getAttribute('href') || a.href || '';
                    if (href && !allLinks.includes(href)) allLinks.push(href);
                });
            }
            return allLinks;
        });
    } catch {
        try {
            return await page.evaluate(() => {
                const list = [];
                document.querySelectorAll('#res .tF2Cxc a[href], .yuRUbf a[href]').forEach(a => {
                    const href = a.href || a.getAttribute('href');
                    if (href) list.push(href);
                });
                return list;
            });
        } catch {
            return [];
        }
    }
}

/**
 * Click the "Next page" button in Google search results
 */
async function clickNextPage(page) {
    const nextSelectors = [
        '#pnnext',
        'a[aria-label="Next page"]',
        'a[aria-label*="Trang tiếp theo"]',
    ];

    for (const selector of nextSelectors) {
        try {
            const btn = await page.$(selector);
            if (btn) {
                await btn.evaluate(el => el.scrollIntoView({ block: 'center' }));
                await btn.click();
                await page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 10000 }).catch(() => { });
                return true;
            }
        } catch { }
    }

    try {
        const [btn] = await page.$$('xpath///a[contains(text(),"Next") or contains(text(),"Tiếp theo")]');
        if (btn) {
            await btn.evaluate(el => el.scrollIntoView({ block: 'center' }));
            await btn.click();
            await page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 10000 }).catch(() => { });
            return true;
        }
    } catch { }

    return false;
}

/**
 * Detect SERP features on the current results page
 */
async function detectSerpFeatures(page) {
    try {
        return await page.evaluate(() => {
            const features = [];
            if (document.querySelector('.xpdopen, .ifM9O, .g.mnr-c.g-blk, [data-attrid="wa:/description"]'))
                features.push('Featured Snippet');
            if (document.querySelector('.related-question-pair, [data-sgrd], .wQiwMc'))
                features.push('PAA');
            if (document.querySelector('.HD8Pae, .RzdJxc, video-voyager'))
                features.push('Video');
            if (document.querySelector('.kp-wholepage, .osrp-blk, .knowledge-panel'))
                features.push('Knowledge Panel');
            if (document.querySelector('.immersive-carousel, .F9rcV, .ivg-i'))
                features.push('Images');
            if (document.querySelector('.VkpGBb, .cXedhc, [data-local-attribute]'))
                features.push('Local Pack');
            if (document.querySelector('.usJj9c, .HiHjCd'))
                features.push('Sitelinks');
            return features;
        });
    } catch {
        return [];
    }
}

/**
 * Extract "People Also Ask" questions from SERP
 */
async function extractPAA(page) {
    try {
        return await page.evaluate(() => {
            const questions = [];
            // Multiple selectors for PAA questions across Google layouts
            const selectors = [
                '.related-question-pair [data-q]',
                '.wQiwMc [data-q]',
                '[data-sgrd] [role="heading"]',
                '.related-question-pair span',
            ];
            for (const sel of selectors) {
                document.querySelectorAll(sel).forEach(el => {
                    const q = el.getAttribute('data-q') || el.textContent?.trim();
                    if (q && q.length > 5 && !questions.includes(q)) questions.push(q);
                });
                if (questions.length > 0) break;
            }
            return questions.slice(0, 8);
        });
    } catch {
        return [];
    }
}

/**
 * Extract "Related Searches" from bottom of SERP
 */
async function extractRelatedSearches(page) {
    try {
        return await page.evaluate(() => {
            const related = [];
            const selectors = [
                '#botstuff .k8XOCe a',           // "Related searches" section
                '.Oj5Ld a',                       // Alternative layout
                '#brs a .s75CSd',                 // Older layout: text inside link
                '.AJLUJb a .eONsm',              // Another variation
                '.k8XOCe .s75CSd',               // Text spans
            ];
            for (const sel of selectors) {
                document.querySelectorAll(sel).forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 2 && !related.includes(text)) related.push(text);
                });
                if (related.length > 0) break;
            }
            return related.slice(0, 8);
        });
    } catch {
        return [];
    }
}

/**
 * Extract top competitor URLs + titles from SERP (excluding target domain)
 */
async function extractTopCompetitors(page, targetDomain) {
    try {
        const normalizedTarget = normalizeDomain(targetDomain);
        return await page.evaluate((target) => {
            const competitors = [];
            const results = document.querySelectorAll('#res .tF2Cxc, .yuRUbf');
            results.forEach(el => {
                const linkEl = el.querySelector('a[href]');
                const titleEl = el.querySelector('h3') || linkEl?.querySelector('h3');
                if (!linkEl) return;
                const url = linkEl.href || linkEl.getAttribute('href') || '';
                const title = titleEl?.textContent?.trim() || '';
                if (!url || url.includes('google.com')) return;
                try {
                    const domain = new URL(url).hostname.replace(/^www\./, '');
                    if (target && domain.endsWith(target)) return; // Skip own domain
                    if (!competitors.find(c => c.domain === domain)) {
                        competitors.push({ url, title, domain });
                    }
                } catch { }
            });
            return competitors.slice(0, 5);
        }, normalizedTarget);
    } catch {
        return [];
    }
}

/**
 * Search a keyword on Google and find the position of the target domain
 *
 * Port of RankChecker.search_keyword_return_position()
 *
 * @param {import('puppeteer').Page} page
 * @param {string} keyword
 * @param {string} domain
 * @param {string} uuleCode
 * @param {number} maxPages
 * @returns {Promise<object>}
 */
async function searchKeyword(page, keyword, domain, uuleCode, maxPages = DEFAULT_MAX_PAGES) {
    const normalizedDomain = normalizeDomain(domain);
    let resultUrl = '';
    let pageFound = `-${maxPages}`;
    let posFound = '-';
    let rank = '-';
    let localText = '-';
    let totalCount = 0;

    // Navigate to Google Search
    const searchUrl = uule.buildSearchUrl(keyword, uuleCode);
    try {
        await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: PAGE_LOAD_TIMEOUT });
    } catch (e) {
        return { url: '[x] -- Lỗi timeout', page: '-', pos: posFound, rank, local: localText };
    }

    // Wait for results to load
    try {
        await page.waitForSelector('.tF2Cxc, .yuRUbf', { timeout: SEARCH_RESULT_TIMEOUT });
    } catch { }

    // Get local location
    localText = await getLocalLocation(page);

    // Detect SERP features on first page
    const serpFeatures = await detectSerpFeatures(page);

    // Extract SERP intelligence data (PAA, Related Searches, Competitors)
    const paa = await extractPAA(page);
    const relatedSearches = await extractRelatedSearches(page);
    const competitors = await extractTopCompetitors(page, domain);
    const serpData = { paa, relatedSearches, competitors };

    if (paa.length > 0) console.log(`  📋 PAA: ${paa.length} questions`);
    if (relatedSearches.length > 0) console.log(`  🔗 Related: ${relatedSearches.length} suggestions`);
    if (competitors.length > 0) console.log(`  🏆 Competitors: ${competitors.map(c => c.domain).join(', ')}`);

    // Search through pages
    for (let pageIdx = 0; pageIdx < maxPages; pageIdx++) {
        // Wait for page to load
        try {
            await page.waitForFunction(() => document.readyState === 'complete', { timeout: 15000 });
        } catch {
            return { url: `[x] -- Trang ${pageIdx} tải quá thời gian chờ`, page: '-', pos: posFound, rank, local: localText, serpData };
        }

        // Check for CAPTCHA and try to solve
        const captcha = await checkCaptcha(page);
        if (captcha.hasCaptcha) {
            consecutiveCaptchas++;
            console.log(`🛡️ CAPTCHA #${consecutiveCaptchas} detected (${captcha.type}) for "${keyword}"`);

            const solved = await captchaSolver.solveCaptcha(page, {
                maxRetries: 3,
                keyword,
            });

            if (solved) {
                console.log(`✅ CAPTCHA solved for "${keyword}" — continuing search`);
                consecutiveCaptchas = 0;
                await sleep(2000);
                try {
                    await page.waitForSelector('.tF2Cxc, .yuRUbf', { timeout: SEARCH_RESULT_TIMEOUT });
                } catch { }
            } else {
                console.log(`❌ CAPTCHA not solved for "${keyword}" — will reset WARP after closing browser`);
                return { url: '[x] -- CAPTCHA (unsolved)', page: '-', pos: posFound, rank, local: localText, captcha: true, needWarpReset: true, serpData };
            }
        } else {
            // No CAPTCHA — reset counter
            consecutiveCaptchas = 0;
        }

        // Extract search results
        let hrefs = await extractSearchResults(page);
        hrefs = hrefs.map(h => extractRealHref(h)).filter(Boolean);

        // Search for domain in results
        for (let i = 0; i < hrefs.length; i++) {
            try {
                const hrefDomain = normalizeDomain(hrefs[i]);
                if (normalizedDomain && hrefDomain.endsWith(normalizedDomain)) {
                    return {
                        url: hrefs[i],
                        page: pageIdx + 1,
                        pos: i + 1,
                        rank: totalCount + i + 1,
                        local: localText,
                        serpFeatures,
                        serpData,
                    };
                }
            } catch { }
        }

        totalCount += hrefs.length;

        // Try to go to next page
        if (pageIdx < maxPages - 1) {
            const hasNext = await clickNextPage(page);
            if (!hasNext) break;
            await sleep(2000 + Math.random() * 3000); // 2-5s between pages
        }
    }

    return { url: resultUrl, page: pageFound, pos: posFound, rank, local: localText, serpFeatures, serpData };
}

// ============ Checker Orchestrator ============

// Global state for the active check session
let activeSession = null;

// Track all active browsers for force-close on stop
let activeBrowsers = new Set();

/**
 * Get the current checker status
 */
function getStatus() {
    if (!activeSession) {
        return { state: 'idle' };
    }
    return {
        state: activeSession.state,
        project: activeSession.project,
        total: activeSession.total,
        done: activeSession.done,
        percent: activeSession.total > 0 ? Math.round((activeSession.done / activeSession.total) * 100) : 0,
        results: activeSession.results,
        startedAt: activeSession.startedAt,
        errors: activeSession.errors,
    };
}

/**
 * Subscribe to result updates via callback
 */
function onResult(callback) {
    if (activeSession) {
        activeSession.listeners.push(callback);
    }
}

/**
 * Emit a result to all listeners
 */
function emitResult(result) {
    if (!activeSession) return;
    activeSession.results.push(result);
    activeSession.done++;
    for (const listener of activeSession.listeners) {
        try { listener(result); } catch { }
    }
}

/**
 * Stop the active checker session — force kill all browsers
 */
function stopChecker() {
    if (!activeSession) return { success: false, message: 'No active session' };
    activeSession.state = 'stopping';

    // Force-close all tracked browsers
    for (const browser of activeBrowsers) {
        try {
            const proc = browser.process();
            if (proc) proc.kill('SIGKILL');
        } catch { }
        try { browser.close().catch(() => { }); } catch { }
    }
    activeBrowsers.clear();

    activeSession.state = 'done';
    console.log('[Checker] ⏹ Force stopped — all browsers killed');
    return { success: true, message: 'Stopped' };
}

/**
 * Pause/Resume the active checker session
 */
function pauseChecker() {
    if (!activeSession) return { success: false, message: 'No active session' };
    if (activeSession.state === 'running') {
        activeSession.state = 'paused';
        return { success: true, message: 'Paused', state: 'paused' };
    }
    if (activeSession.state === 'paused') {
        activeSession.state = 'running';
        activeSession.resumeResolve?.();
        return { success: true, message: 'Resumed', state: 'running' };
    }
    return { success: false, message: `Cannot pause in state: ${activeSession.state}` };
}

/**
 * Wait if paused, return false if stopped
 */
async function checkPauseStop() {
    if (!activeSession) return false;
    if (activeSession.state === 'stopping' || activeSession.state === 'done') return false;
    while (activeSession.state === 'paused') {
        await new Promise(resolve => {
            activeSession.resumeResolve = resolve;
            setTimeout(resolve, 500);
        });
        if (activeSession.state === 'stopping' || activeSession.state === 'done') return false;
    }
    return activeSession.state === 'running';
}

/**
 * Check a single keyword with its own browser instance
 */
async function checkSingleKeyword(keyword, domain, uuleCode, maxPages = DEFAULT_MAX_PAGES) {
    let browser = null;

    if (activeSession && (activeSession.state === 'stopping' || activeSession.state === 'done')) {
        return { keyword, url: '[x] -- Stopped', page: '-', pos: '-', rank: '-', local: '-', skipped: true };
    }

    try {
        browser = await launchBrowser();
        activeBrowsers.add(browser);

        const pages = await browser.pages();
        const page = pages.length > 0 ? pages[0] : await browser.newPage();
        await page.setDefaultNavigationTimeout(PAGE_LOAD_TIMEOUT);

        const result = await searchKeyword(page, keyword, domain, uuleCode, maxPages);
        result.keyword = keyword;
        return result;
    } catch (e) {
        if (activeSession && (activeSession.state === 'stopping' || activeSession.state === 'done')) {
            return { keyword, url: '[x] -- Stopped', page: '-', pos: '-', rank: '-', local: '-', skipped: true };
        }
        return { keyword, url: `[x] -- ${e.message}`, page: '-', pos: '-', rank: '-', local: '-' };
    } finally {
        if (browser) {
            activeBrowsers.delete(browser);
            try { await browser.close(); } catch { }
        }
    }
}

/**
 * Wrapper that handles WARP reset AFTER browser is closed
 */
async function checkSingleKeywordWithWarp(keyword, domain, uuleCode, maxPages = DEFAULT_MAX_PAGES) {
    const result = await checkSingleKeyword(keyword, domain, uuleCode, maxPages);

    // WARP reset happens here — AFTER browser is closed, between keywords
    if (result.needWarpReset && consecutiveCaptchas >= CAPTCHA_RESET_THRESHOLD) {
        console.log(`[Checker] 🔄 ${consecutiveCaptchas} consecutive CAPTCHAs — resetting WARP for new IP...`);
        try {
            await warp.warpReset();
            consecutiveCaptchas = 0;
            await sleep(3000);
        } catch (e) {
            console.error('[Checker] WARP reset error:', e.message);
        }
    }

    // Human-like delay between keywords (2-4s — Balanced preset)
    const kwDelay = 2000 + Math.random() * 2000;
    console.log(`[Checker] ⏳ Waiting ${(kwDelay / 1000).toFixed(1)}s before next keyword...`);
    await sleep(kwDelay);

    return result;
}

/**
 * Start checking keywords for a project
 *
 * Port of AppGUI._run_project_once() - chunk-based parallel execution
 */
async function startChecker({ project, domain, keywords, options = {}, db = null }) {
    if (activeSession && activeSession.state === 'running') {
        return { success: false, message: 'Checker already running' };
    }

    const {
        maxPages = DEFAULT_MAX_PAGES,
        chunkSize = DEFAULT_CHUNK_SIZE,
        uuleLocation = '',
    } = options;

    // Encode UULE
    const uuleCode = uuleLocation ? uule.encode(uuleLocation) : '';

    // Clear any leftover browsers
    activeBrowsers.clear();

    // Initialize session
    activeSession = {
        state: 'running',
        project,
        domain,
        total: keywords.length,
        done: 0,
        results: [],
        errors: [],
        listeners: [],
        startedAt: new Date().toISOString(),
        resumeResolve: null,
    };

    console.log(`[Checker] Starting: ${project} (${keywords.length} keywords, chunk=${chunkSize}, maxPages=${maxPages})`);

    // Run in background
    (async () => {
        try {
            for (let chunkStart = 0; chunkStart < keywords.length; chunkStart += chunkSize) {
                // Check pause/stop BEFORE launching chunk
                if (!(await checkPauseStop())) {
                    console.log('[Checker] ⏹ Stopped before chunk start');
                    break;
                }

                const chunk = keywords.slice(chunkStart, chunkStart + chunkSize);
                console.log(`[Checker] Chunk ${Math.floor(chunkStart / chunkSize) + 1}: keywords ${chunkStart + 1}-${chunkStart + chunk.length}`);

                // Run chunk in parallel — stagger start to avoid simultaneous Google hits
                const promises = chunk.map((kw, localIdx) =>
                    sleep(localIdx * (1000 + Math.random() * 1000)) // Stagger: 0s, 1-2s, 2-4s...
                        .then(() => checkSingleKeywordWithWarp(kw, domain, uuleCode, maxPages))
                        .then(result => {
                            // If skipped due to stop, don't emit
                            if (result.skipped) return result;

                            const idx = chunkStart + localIdx + 1;
                            const now = new Date();
                            const dateStr = now.toLocaleDateString('vi-VN');
                            const timeStr = now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

                            const fullResult = {
                                idx,
                                keyword: kw,
                                url: result.url || '-',
                                page: result.page,
                                pos: result.pos,
                                rank: result.rank,
                                local: result.local,
                                date: dateStr,
                                time: timeStr,
                                captcha: result.captcha || false,
                                serpFeatures: result.serpFeatures || [],
                            };

                            if (result.captcha) {
                                activeSession.errors.push({ keyword: kw, error: 'CAPTCHA detected' });
                            }

                            emitResult(fullResult);

                            // Save to database if available
                            if (db) {
                                try {
                                    db.importSheetData(project, [{
                                        keyword: kw,
                                        stt: idx,
                                        position: result.rank !== '-' ? parseInt(result.rank) : null,
                                        page: result.page !== '-' ? parseInt(result.page) : null,
                                        url: result.url || '',
                                        local: result.local || '',
                                        date: dateStr,
                                        time: timeStr,
                                    }]);
                                    // Save SERP intelligence data (PAA, Related, Competitors)
                                    if (result.serpData) {
                                        db.saveSerpData(project, kw, result.serpData);
                                    }
                                } catch (dbErr) {
                                    console.error(`[Checker] DB save error for "${kw}":`, dbErr.message);
                                }
                            }

                            // Write back to Google Sheet (background, non-blocking)
                            sheets.writeRankingToSheet(
                                project, kw,
                                result.rank !== '-' ? parseInt(result.rank) : 0,
                                dateStr,
                                result.url || '',
                                result.page !== '-' ? result.page : '',
                            ).catch(e => console.error(`[Checker] Sheet write error for "${kw}":`, e.message));

                            return fullResult;
                        })
                );

                await Promise.all(promises);

                // Check if stopped during chunk execution
                if (activeSession.state === 'stopping' || activeSession.state === 'done') {
                    console.log('[Checker] ⏹ Stopped during chunk');
                    break;
                }

                // Delay between chunks — longer to let Google cool down
                if (chunkStart + chunkSize < keywords.length) {
                    const chunkDelay = 4000 + Math.random() * 2000; // 4-6s between chunks
                    console.log(`[Checker] ⏳ Chunk delay: ${(chunkDelay / 1000).toFixed(1)}s before next chunk...`);
                    await sleep(chunkDelay);
                }
            }

            if (activeSession.state === 'running') {
                activeSession.state = 'done';
                console.log(`[Checker] ✅ Done: ${activeSession.done}/${activeSession.total} keywords checked`);
            }
        } catch (err) {
            console.error('[Checker] Fatal error:', err);
            activeSession.state = 'error';
            activeSession.errors.push({ error: err.message });
        }
    })();

    return {
        success: true,
        message: `Checker started for ${project}`,
        total: keywords.length,
    };
}

module.exports = {
    startChecker,
    stopChecker,
    pauseChecker,
    getStatus,
    onResult,
    normalizeDomain,
    // Export for testing
    launchBrowser,
    searchKeyword,
    checkCaptcha,
};
