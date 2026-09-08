/**
 * UULE Encoder for Google Local Search
 * Port from Python uule_grabber module
 *
 * UULE = User-Unfriendly Location Encoding
 * Used to force Google Search to show results for a specific location
 */

// Base64-like secret map used by Google
const UULE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';

/**
 * Encode a location string to Google UULE parameter
 * @param {string} location - e.g. "Tan Phu, Ho Chi Minh City, Vietnam"
 * @returns {string} UULE encoded string
 */
function encode(location) {
    if (!location || typeof location !== 'string') return '';
    location = location.trim();
    if (!location) return '';

    // The UULE format: w+CAIQICI{length_char}{base64_location}
    // Length char maps the byte length of the location to a single character
    const locationBytes = Buffer.from(location, 'utf-8');
    const lengthChar = UULE_CHARS[locationBytes.length % 64];

    // Base64 encode the location
    const encoded = locationBytes.toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');

    return `w+CAIQICI${lengthChar}${encoded}`;
}

/**
 * Build a Google Search URL with UULE parameter
 * @param {string} keyword - Search query
 * @param {string} uuleCode - Pre-encoded UULE string
 * @param {object} options - Additional search options
 * @returns {string} Full Google Search URL
 */
function buildSearchUrl(keyword, uuleCode, options = {}) {
    const params = new URLSearchParams({
        q: keyword,
        hl: options.hl || 'vi',
        gl: options.gl || 'vn',
    });
    if (uuleCode) {
        params.set('uule', uuleCode);
    }
    return `https://www.google.com/search?${params.toString()}`;
}

module.exports = { encode, buildSearchUrl };
