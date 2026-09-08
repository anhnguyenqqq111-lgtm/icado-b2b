/**
 * Google Sheets Helper — Read & Write via OAuth
 *
 * Supports:
 * - OAuth2 authentication (credentials.json → token.json)
 * - Read projects from "Project" sheet
 * - Read keywords from "Keyword_KPI" sheet
 * - Write ranking results to project-specific sheets
 */

const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');

const SETTINGS_PATH = path.join(__dirname, '..', 'settings.json');
const CREDS_PATH = path.join(__dirname, '..', 'credentials.json');
const TOKEN_PATH = path.join(__dirname, '..', 'token.json');

const SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
];

let settings = null;
let sheetsService = null;
let authClient = null;

// ============ Settings ============

function getSettings() {
    if (!settings) {
        settings = JSON.parse(fs.readFileSync(SETTINGS_PATH, 'utf8'));
    }
    return settings;
}

function saveSettings(newSettings) {
    settings = { ...getSettings(), ...newSettings };
    fs.writeFileSync(SETTINGS_PATH, JSON.stringify(settings, null, 2), 'utf8');
}

// ============ OAuth2 Authentication ============

async function getAuthClient() {
    if (authClient) return authClient;

    if (!fs.existsSync(CREDS_PATH)) {
        console.warn('[Sheets] No credentials.json found, OAuth unavailable');
        return null;
    }

    const creds = JSON.parse(fs.readFileSync(CREDS_PATH, 'utf8'));
    const { client_id, client_secret } = creds.installed || creds.web || {};

    // Dynamic port: matches the PORT env variable or defaults to 3000
    const port = process.env.PORT || 3000;
    const REDIRECT_URI = `http://localhost:${port}`;

    const oauth2Client = new google.auth.OAuth2(client_id, client_secret, REDIRECT_URI);

    if (fs.existsSync(TOKEN_PATH)) {
        try {
            const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
            oauth2Client.setCredentials(token);

            if (token.expiry_date && token.expiry_date < Date.now()) {
                console.log('[Sheets] Token expired, refreshing...');
                const { credentials } = await oauth2Client.refreshAccessToken();
                oauth2Client.setCredentials(credentials);
                fs.writeFileSync(TOKEN_PATH, JSON.stringify(credentials, null, 2));
            }

            authClient = oauth2Client;
            return authClient;
        } catch (err) {
            console.warn('[Sheets] Token invalid, need re-auth:', err.message);
        }
    }

    authClient = oauth2Client;
    return null;
}

function getAuthUrl() {
    if (!authClient) return null;
    return authClient.generateAuthUrl({
        access_type: 'offline', scope: SCOPES, prompt: 'consent',
    });
}

async function exchangeAuthCode(code) {
    if (!authClient) await getAuthClient();
    const { tokens } = await authClient.getToken(code);
    authClient.setCredentials(tokens);
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
    console.log('[Sheets] ✅ OAuth token saved');
    sheetsService = null;
    return true;
}

async function getSheetsService() {
    if (sheetsService) return sheetsService;
    const auth = await getAuthClient();
    if (!auth) return null;
    sheetsService = google.sheets({ version: 'v4', auth });
    return sheetsService;
}

// ============ Read Operations ============

async function listProjects() {
    const service = await getSheetsService();
    if (!service) return [];

    const { GOOGLE_SHEET_ID } = getSettings();
    try {
        const res = await service.spreadsheets.values.get({
            spreadsheetId: GOOGLE_SHEET_ID, range: 'Project!A:Z',
        });
        const values = res.data.values || [];
        if (values.length < 2) return [];

        const header = values[0].map(h => h.trim());
        const nameIdx = header.findIndex(h => {
            const u = h.toUpperCase().normalize('NFC');
            return ['DỰ ÁN', 'DU AN', 'NAME', 'PROJECT', 'TÊN', 'TEN'].some(k => u.includes(k));
        });
        const domainIdx = header.findIndex(h => {
            const u = h.toUpperCase().normalize('NFC');
            return ['DOMAIN', 'URL', 'WEBSITE'].some(k => u.includes(k));
        });

        const ni = nameIdx >= 0 ? nameIdx : 0;
        const di = domainIdx >= 0 ? domainIdx : 1;

        return values.slice(1)
            .map(row => ({ name: (row[ni] || '').trim(), domain: (row[di] || '').trim().replace(/\/$/, '') }))
            .filter(p => p.name);
    } catch (err) {
        console.error('[Sheets] Error reading Project sheet:', err.message);
        return [];
    }
}

async function getKeywordsForProject(projectName) {
    const service = await getSheetsService();
    if (!service) return [];

    const { GOOGLE_SHEET_ID } = getSettings();
    try {
        const res = await service.spreadsheets.values.get({
            spreadsheetId: GOOGLE_SHEET_ID, range: 'Keyword_KPI!A:Z',
        });
        const values = res.data.values || [];
        if (values.length < 2) return [];

        const header = values[0].map(h => h.trim());
        const projectIdx = header.findIndex(h => {
            const u = h.toUpperCase().normalize('NFC');
            return ['DỰ ÁN', 'DU AN', 'PROJECT', 'NAME'].some(k => u.includes(k));
        });
        const kwIdx = header.findIndex(h => {
            const u = h.toUpperCase().normalize('NFC');
            return ['KEYWORDS', 'KEYWORD', 'KEY', 'TỪ KHÓA', 'TU KHOA', 'KW'].some(k => u.includes(k));
        });

        if (kwIdx === -1) return [];

        const norm = projectName.toLowerCase().trim();
        return values.slice(1)
            .filter(row => {
                const kw = (row[kwIdx] || '').trim();
                if (!kw) return false;
                if (projectIdx >= 0) {
                    const proj = (row[projectIdx] || '').trim().toLowerCase();
                    return proj === norm || proj.includes(norm) || norm.includes(proj);
                }
                return true;
            })
            .map(row => (row[kwIdx] || '').trim());
    } catch (err) {
        console.error('[Sheets] Error reading Keyword_KPI:', err.message);
        return [];
    }
}

async function getSheetData(project) {
    const service = await getSheetsService();
    if (!service) return [];

    const { GOOGLE_SHEET_ID, HEADER_MAP } = getSettings();
    try {
        const res = await service.spreadsheets.values.get({
            spreadsheetId: GOOGLE_SHEET_ID, range: `${project}!A:Z`,
        });
        const values = res.data.values || [];
        if (values.length < 2) return [];

        const header = values[0];
        const reverseMap = {};
        if (HEADER_MAP) {
            for (const [headerName, dataKey] of Object.entries(HEADER_MAP)) {
                const colIdx = header.indexOf(headerName);
                if (colIdx >= 0) reverseMap[dataKey] = colIdx;
            }
        }

        return values.slice(1).map((row, i) => {
            const index = i + 1;
            const stt = reverseMap.idx !== undefined ? parseInt(row[reverseMap.idx]) || index : index;
            const keyword = reverseMap.kw !== undefined ? (row[reverseMap.kw] || '').trim() : null;
            const position = reverseMap.rank !== undefined ? parsePos(row[reverseMap.rank]) : null;
            const page = reverseMap.page !== undefined ? parseInt(row[reverseMap.page]) || null : null;
            const date = reverseMap.date !== undefined ? (row[reverseMap.date] || '') : '';
            const url = reverseMap.url !== undefined ? (row[reverseMap.url] || '') : '';
            const local = reverseMap.local !== undefined ? (row[reverseMap.local] || '') : '';
            const time = reverseMap.time !== undefined ? (row[reverseMap.time] || '') : '';
            return { stt, keyword, position, page, date, url, local, time };
        });
    } catch (err) {
        console.error(`[Sheets] Error reading "${project}":`, err.message);
        return [];
    }
}

function parsePos(val) {
    if (!val || val === '' || val === '-') return null;
    const n = parseInt(val);
    return isNaN(n) || n <= 0 ? null : n;
}

// ============ Write Operations ============

async function ensureSheetAndHeader(sheetName, headers) {
    const service = await getSheetsService();
    if (!service) return false;

    const { GOOGLE_SHEET_ID } = getSettings();
    try {
        const ss = await service.spreadsheets.get({
            spreadsheetId: GOOGLE_SHEET_ID,
            fields: 'sheets(properties(title,sheetId))',
        });
        const titles = ss.data.sheets.map(s => s.properties.title);

        if (!titles.includes(sheetName)) {
            await service.spreadsheets.batchUpdate({
                spreadsheetId: GOOGLE_SHEET_ID,
                requestBody: { requests: [{ addSheet: { properties: { title: sheetName } } }] },
            });
        }

        const headerRes = await service.spreadsheets.values.get({
            spreadsheetId: GOOGLE_SHEET_ID, range: `${sheetName}!1:1`,
        });
        const existing = (headerRes.data.values || [[]])[0].map(h => h.trim().toUpperCase());
        const expected = headers.map(h => h.trim().toUpperCase());

        if (existing.slice(0, expected.length).join(',') !== expected.join(',')) {
            await service.spreadsheets.values.update({
                spreadsheetId: GOOGLE_SHEET_ID,
                range: `${sheetName}!A1`,
                valueInputOption: 'USER_ENTERED',
                requestBody: { values: [headers] },
            });
        }
        return true;
    } catch (err) {
        console.error(`[Sheets] Error ensuring sheet "${sheetName}":`, err.message);
        return false;
    }
}

async function writeRankingToSheet(projectName, keyword, ranking, date, url = '', page = '') {
    const service = await getSheetsService();
    if (!service) return false;

    const { GOOGLE_SHEET_ID } = getSettings();
    const sheetName = projectName;
    const HEADERS = ['Keywords', 'Ranking', 'Date_check', 'URL', 'Page'];

    try {
        await ensureSheetAndHeader(sheetName, HEADERS);

        const res = await service.spreadsheets.values.get({
            spreadsheetId: GOOGLE_SHEET_ID,
            range: `'${sheetName}'!A:E`,
        });
        const values = res.data.values || [];

        const normalizedKw = keyword.toLowerCase().trim();
        let foundRow = -1;
        for (let i = 1; i < values.length; i++) {
            if ((values[i][0] || '').trim().toLowerCase() === normalizedKw) {
                foundRow = i + 1;
                break;
            }
        }

        const rowData = [keyword, ranking > 0 ? ranking : '', date, url, page];

        if (foundRow > 0) {
            await service.spreadsheets.values.update({
                spreadsheetId: GOOGLE_SHEET_ID,
                range: `'${sheetName}'!A${foundRow}`,
                valueInputOption: 'USER_ENTERED',
                requestBody: { values: [rowData] },
            });
        } else {
            await service.spreadsheets.values.append({
                spreadsheetId: GOOGLE_SHEET_ID,
                range: `'${sheetName}'!A:E`,
                valueInputOption: 'USER_ENTERED',
                requestBody: { values: [rowData] },
            });
        }
        return true;
    } catch (err) {
        console.error(`[Sheets] Error writing ranking to "${sheetName}":`, err.message);
        return false;
    }
}

// ============ Exports ============

module.exports = {
    getSettings,
    saveSettings,
    listProjects,
    listProjectsFromSheet: listProjects,
    getKeywordsForProject,
    getSheetData,
    ensureSheetAndHeader,
    exchangeAuthCode,
    getAuthClient,
    getAuthUrl,
    writeRankingToSheet,
};
