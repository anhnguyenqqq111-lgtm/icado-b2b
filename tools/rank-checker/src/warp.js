/**
 * Cloudflare WARP Controller
 * Port from Python warp_ctrler.py
 *
 * Controls WARP VPN connection for IP rotation during rank checking
 */

const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

// Candidate paths for warp-cli
const CANDIDATES = [
    'warp-cli',
    'warp-cli.exe',
    String.raw`C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe`,
    String.raw`C:\Program Files (x86)\Cloudflare\Cloudflare WARP\warp-cli.exe`,
];

let warpCliPath = null;

/**
 * Find warp-cli executable
 */
function findWarpCli() {
    if (warpCliPath) return warpCliPath;

    for (const candidate of CANDIDATES) {
        if (path.isAbsolute(candidate) && fs.existsSync(candidate)) {
            warpCliPath = candidate;
            return warpCliPath;
        }
    }

    // Try to find in PATH via where command
    try {
        const { execSync } = require('child_process');
        const result = execSync('where warp-cli', { encoding: 'utf-8', timeout: 5000 }).trim();
        if (result) {
            warpCliPath = result.split('\n')[0].trim();
            return warpCliPath;
        }
    } catch { }

    return null;
}

/**
 * Run a warp-cli command
 */
function runCmd(args, timeout = 15000) {
    return new Promise((resolve, reject) => {
        const cli = findWarpCli();
        if (!cli) {
            return reject(new Error('warp-cli not found'));
        }

        execFile(cli, args, { timeout }, (err, stdout, stderr) => {
            if (err) {
                return reject(err);
            }
            resolve((stdout || '') + (stderr ? '\n' + stderr : ''));
        });
    });
}

/**
 * Get WARP connection status
 * @returns {Promise<'connected'|'disconnected'|'not_installed'|'unknown'>}
 */
async function warpStatus() {
    const cli = findWarpCli();
    if (!cli) return 'not_installed';

    try {
        const output = await runCmd(['status']);
        const s = output.toLowerCase();

        // Check "status update: <word>" pattern
        const match = s.match(/status update:\s*([a-z]+)/);
        if (match) {
            const st = match[1].trim();
            if (st === 'connected' || st === 'disconnected') return st;
        }

        // Check for exact words
        if (/\bdisconnected\b/.test(s)) return 'disconnected';
        if (/\bconnected\b/.test(s)) return 'connected';

        return 'unknown';
    } catch {
        return 'unknown';
    }
}

/**
 * Wait for WARP to reach a specific state
 */
async function waitForState(target, timeout = 10000, poll = 500) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
        const st = await warpStatus();
        if (st === target) return true;
        await new Promise(r => setTimeout(r, poll));
    }
    return false;
}

/**
 * Connect WARP
 */
async function warpOn(waitTimeout = 10000) {
    const cli = findWarpCli();
    if (!cli) throw new Error('warp-cli not found');

    try {
        const output = await runCmd(['connect']);
        console.log('[WARP] Connect:', output.trim());
    } catch (e) {
        console.error('[WARP] Connect error:', e.message);
        return false;
    }

    return await waitForState('connected', waitTimeout);
}

/**
 * Disconnect WARP
 */
async function warpOff(waitTimeout = 10000) {
    const cli = findWarpCli();
    if (!cli) throw new Error('warp-cli not found');

    try {
        const output = await runCmd(['disconnect']);
        console.log('[WARP] Disconnect:', output.trim());
    } catch (e) {
        console.error('[WARP] Disconnect error:', e.message);
        return false;
    }

    return await waitForState('disconnected', waitTimeout);
}

/**
 * Toggle WARP connection
 */
async function warpToggle() {
    const st = await warpStatus();
    console.log('[WARP] Current status:', st);

    if (st === 'connected') {
        console.log('[WARP] Disconnecting...');
        return { success: await warpOff(), newState: 'disconnected' };
    }
    if (st === 'disconnected') {
        console.log('[WARP] Connecting...');
        return { success: await warpOn(), newState: 'connected' };
    }

    // Unknown state: try to connect
    console.log('[WARP] Unknown state, attempting connect...');
    try {
        const success = await warpOn();
        return { success, newState: success ? 'connected' : 'unknown' };
    } catch {
        return { success: false, newState: 'unknown' };
    }
}

/**
 * Reset WARP connection (disconnect → wait → reconnect)
 * Gets a new IP address for avoiding CAPTCHA blocks
 */
async function warpReset() {
    console.log('[WARP] 🔄 Resetting connection for new IP...');
    const st = await warpStatus();

    if (st === 'connected') {
        await warpOff(10000);
        // Wait a bit before reconnecting
        await new Promise(r => setTimeout(r, 2000));
    }

    const success = await warpOn(15000);
    console.log(`[WARP] Reset ${success ? '✅ done — new IP' : '❌ failed'}`);
    return { success, newState: success ? 'connected' : 'disconnected' };
}

module.exports = { findWarpCli, warpStatus, warpOn, warpOff, warpToggle, warpReset };
