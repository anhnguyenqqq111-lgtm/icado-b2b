/**
 * Google reCAPTCHA Audio Solver
 * Port from Python gcaptsolver.py
 *
 * Flow: Detect CAPTCHA → Click checkbox → Request audio → Download →
 *       ffmpeg convert to WAV → Google Speech Recognition → Submit answer
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');
const https = require('https');
const http = require('http');

// ============ FFmpeg ============

const ffmpegPath = (() => {
    try { return require('ffmpeg-static'); } catch { }
    // Fallback: check local file or PATH
    const local = path.join(__dirname, '..', 'ffmpeg.exe');
    if (fs.existsSync(local)) return local;
    try {
        require('child_process').execSync('ffmpeg -version', { stdio: 'ignore', timeout: 3000 });
        return 'ffmpeg';
    } catch { }
    return null;
})();

function convertToWav(inputPath, outputPath) {
    if (!ffmpegPath) throw new Error('ffmpeg not found — install ffmpeg-static: npm install ffmpeg-static');

    execFileSync(ffmpegPath, [
        '-y', '-i', inputPath,
        '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le',
        '-loglevel', 'error', outputPath
    ], { timeout: 15000 });
}

// ============ Audio Download ============

function downloadFile(url, destPath) {
    return new Promise((resolve, reject) => {
        const client = url.startsWith('https') ? https : http;
        const file = fs.createWriteStream(destPath);
        client.get(url, { timeout: 20000 }, (res) => {
            if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                // Follow redirect
                downloadFile(res.headers.location, destPath).then(resolve).catch(reject);
                return;
            }
            if (res.statusCode !== 200) {
                reject(new Error(`HTTP ${res.statusCode}`));
                return;
            }
            res.pipe(file);
            file.on('finish', () => { file.close(); resolve(); });
        }).on('error', reject);
    });
}

// ============ Speech Recognition via Google Web API ============

async function transcribeAudio(audioUrl) {
    const tmpDir = os.tmpdir();
    const tmpAudio = path.join(tmpDir, `captcha_${Date.now()}.webm`);
    const tmpWav = path.join(tmpDir, `captcha_${Date.now()}.wav`);

    try {
        // Download audio
        await downloadFile(audioUrl, tmpAudio);

        const stat = fs.statSync(tmpAudio);
        if (stat.size < 1024) throw new Error('Audio file too small');

        // Convert to WAV
        convertToWav(tmpAudio, tmpWav);

        // Read WAV and send to Google Speech Recognition API
        const wavData = fs.readFileSync(tmpWav);
        const base64Audio = wavData.toString('base64');

        // Use Google Speech Recognition Web API (free, same as Python's recognize_google)
        const response = await fetch('https://www.google.com/speech-api/v2/recognize?output=json&lang=en-US&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw', {
            method: 'POST',
            headers: {
                'Content-Type': 'audio/l16; rate=16000;',
            },
            body: wavData,
        });

        const text = await response.text();
        // Parse the response (second JSON line contains the result)
        const lines = text.trim().split('\n').filter(l => l.trim());
        for (const line of lines) {
            try {
                const json = JSON.parse(line);
                if (json.result && json.result[0] && json.result[0].alternative) {
                    return json.result[0].alternative[0].transcript;
                }
            } catch { }
        }

        throw new Error('No transcription result');
    } finally {
        // Cleanup
        for (const f of [tmpAudio, tmpWav]) {
            try { if (fs.existsSync(f)) fs.unlinkSync(f); } catch { }
        }
    }
}

// ============ Puppeteer CAPTCHA Interactions ============

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

function randomDelay(min = 1000, max = 2000) {
    return sleep(min + Math.random() * (max - min));
}

/**
 * Click the reCAPTCHA checkbox
 */
async function clickCheckbox(page) {
    for (let attempt = 0; attempt < 3; attempt++) {
        try {
            // Find anchor iframe
            const frames = page.frames();
            for (const frame of frames) {
                const url = frame.url() || '';
                if (url.includes('recaptcha') && url.includes('anchor')) {
                    const checkbox = await frame.waitForSelector('#recaptcha-anchor', { timeout: 10000 });
                    if (checkbox) {
                        await randomDelay();
                        await checkbox.click();
                        console.log('[CAPTCHA] ✅ Clicked checkbox');
                        return true;
                    }
                }
            }
        } catch { }
        if (attempt < 2) await sleep(2000);
    }
    return false;
}

/**
 * Click the audio button in the challenge iframe
 */
async function requestAudioVersion(page) {
    for (let attempt = 0; attempt < 3; attempt++) {
        try {
            await sleep(3000);
            const frames = page.frames();
            let challengeFrame = null;
            for (const frame of frames) {
                const url = frame.url() || '';
                if (url.includes('recaptcha') && url.includes('bframe')) {
                    challengeFrame = frame;
                    break;
                }
            }

            if (!challengeFrame) {
                if (attempt < 2) { await sleep(2000); continue; }
                throw new Error('Challenge iframe not found');
            }

            const audioBtn = await challengeFrame.waitForSelector('#recaptcha-audio-button', { timeout: 15000 });
            if (audioBtn) {
                await randomDelay();
                await audioBtn.click();
                console.log('[CAPTCHA] 🔊 Switched to audio challenge');
                return challengeFrame;
            }
        } catch { }
        if (attempt < 2) await sleep(3000);
    }
    throw new Error('Could not request audio version');
}

/**
 * Solve the audio CAPTCHA challenge
 */
async function solveAudioCaptcha(challengeFrame) {
    // Wait for audio element
    const audioEl = await challengeFrame.waitForSelector('#audio-source', { timeout: 15000 });
    if (!audioEl) throw new Error('Audio source not found');

    const audioSrc = await audioEl.evaluate(el => el.getAttribute('src'));
    if (!audioSrc) throw new Error('Audio source URL empty');

    console.log(`[CAPTCHA] 🎧 Downloading audio...`);

    // Transcribe
    const text = await transcribeAudio(audioSrc);
    console.log(`[CAPTCHA] 📤 Transcription: "${text}"`);

    // Enter answer
    const responseInput = await challengeFrame.waitForSelector('#audio-response', { timeout: 5000 });
    await responseInput.click();
    await responseInput.type(text, { delay: 50 });

    // Click verify
    const verifyBtn = await challengeFrame.waitForSelector('#recaptcha-verify-button', { timeout: 5000 });
    await verifyBtn.click();
    console.log('[CAPTCHA] ✅ Submitted answer');

    await sleep(2000);
    return true;
}

/**
 * Complete CAPTCHA solving flow
 * Port of solve_captcha_complete() from gcaptsolver.py
 *
 * @param {import('puppeteer').Page} page
 * @param {object} options
 * @returns {Promise<boolean>} true if solved or no captcha
 */
async function solveCaptcha(page, options = {}) {
    const { maxRetries = 3, keyword = '' } = options;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            console.log(`[CAPTCHA] 🔄 Attempt ${attempt + 1}/${maxRetries} for: ${keyword}`);

            // Check if captcha exists
            const hasCaptcha = await detectCaptcha(page);
            if (!hasCaptcha.hasCaptcha) {
                console.log('[CAPTCHA] ✅ No CAPTCHA detected');
                return true;
            }

            console.log(`[CAPTCHA] 🛡️ Type: ${hasCaptcha.type}`);

            if (hasCaptcha.type === 'iframe_checkbox' || hasCaptcha.type === 'iframe_challenge') {
                // Step 1: Click checkbox (if it's the checkbox type)
                if (hasCaptcha.type === 'iframe_checkbox') {
                    const clicked = await clickCheckbox(page);
                    if (!clicked) throw new Error('Cannot click checkbox');
                    await randomDelay(2000, 4000);
                }

                // Step 2: Switch to audio
                const challengeFrame = await requestAudioVersion(page);
                await randomDelay(1000, 3000);

                // Step 3: Solve audio
                await solveAudioCaptcha(challengeFrame);
                await randomDelay(2000, 5000);

                console.log('[CAPTCHA] 🎉 CAPTCHA solved!');
                return true;
            } else if (hasCaptcha.type === 'google_sorry') {
                console.log('[CAPTCHA] ⚠️ Google sorry page — need WARP toggle');
                return false;
            } else {
                console.log(`[CAPTCHA] ⚠️ Unsupported type: ${hasCaptcha.type}`);
                return false;
            }
        } catch (err) {
            console.error(`[CAPTCHA] ❌ Attempt ${attempt + 1} failed: ${err.message}`);
            if (attempt < maxRetries - 1) await randomDelay(3000, 5000);
        }
    }

    console.log('[CAPTCHA] ❌ All attempts exhausted');
    return false;
}

/**
 * Detect CAPTCHA on the page
 */
async function detectCaptcha(page) {
    try {
        await sleep(2000);

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

        const hasCaptchaForm = await page.evaluate(() => {
            return !!(
                document.getElementById('captcha-form') ||
                document.querySelector('.g-recaptcha') ||
                document.querySelector("[action*='sorry']")
            );
        });
        if (hasCaptchaForm) return { hasCaptcha: true, type: 'html_captcha' };

        const title = await page.title();
        const lowerTitle = (title || '').toLowerCase();
        if (lowerTitle.includes('unusual traffic') || lowerTitle.includes('sorry')) {
            return { hasCaptcha: true, type: 'google_sorry' };
        }
    } catch { }

    return { hasCaptcha: false, type: null };
}

module.exports = {
    solveCaptcha,
    detectCaptcha,
    transcribeAudio,
};
