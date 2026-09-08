const initSqlJs = require('sql.js');
const fs = require('fs');
const path = require('path');

const DB_DIR = path.join(__dirname, '..', 'data');
const DB_PATH = path.join(DB_DIR, 'rankings.db');

let db = null;
let dbReady = null;

function initDatabase() {
  if (dbReady) return dbReady;

  dbReady = (async () => {
    if (!fs.existsSync(DB_DIR)) fs.mkdirSync(DB_DIR, { recursive: true });

    const SQL = await initSqlJs();

    if (fs.existsSync(DB_PATH)) {
      const buffer = fs.readFileSync(DB_PATH);
      db = new SQL.Database(buffer);
    } else {
      db = new SQL.Database();
    }

    // Create schema
    db.run(`
      CREATE TABLE IF NOT EXISTS keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        keyword TEXT NOT NULL,
        stt INTEGER,
        created_at TEXT DEFAULT (datetime('now')),
        UNIQUE(project, keyword)
      )
    `);
    db.run(`
      CREATE TABLE IF NOT EXISTS rankings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword_id INTEGER NOT NULL,
        position INTEGER,
        page INTEGER,
        url TEXT,
        local_check TEXT,
        checked_at TEXT NOT NULL,
        check_time TEXT,
        FOREIGN KEY (keyword_id) REFERENCES keywords(id)
      )
    `);
    db.run(`CREATE INDEX IF NOT EXISTS idx_rankings_keyword ON rankings(keyword_id)`);
    db.run(`CREATE INDEX IF NOT EXISTS idx_rankings_checked ON rankings(checked_at)`);
    db.run(`CREATE INDEX IF NOT EXISTS idx_keywords_project ON keywords(project)`);
    db.run(`
      CREATE TABLE IF NOT EXISTS sync_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        synced_at TEXT DEFAULT (datetime('now')),
        rows_count INTEGER DEFAULT 0
      )
    `);
    db.run(`
      CREATE TABLE IF NOT EXISTS ai_insights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        insights_json TEXT NOT NULL,
        analyzed_at TEXT DEFAULT (datetime('now')),
        keyword_count INTEGER DEFAULT 0
      )
    `);
    db.run(`CREATE INDEX IF NOT EXISTS idx_ai_project ON ai_insights(project)`);
    db.run(`
      CREATE TABLE IF NOT EXISTS serp_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword_id INTEGER NOT NULL,
        paa_json TEXT,
        related_json TEXT,
        competitors_json TEXT,
        collected_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (keyword_id) REFERENCES keywords(id)
      )
    `);
    db.run(`CREATE INDEX IF NOT EXISTS idx_serp_keyword ON serp_data(keyword_id)`);

    saveDb();
    return db;
  })();

  return dbReady;
}

function saveDb() {
  if (!db) return;
  const data = db.export();
  const buffer = Buffer.from(data);
  fs.writeFileSync(DB_PATH, buffer);
}

// Helper to run queries
function queryAll(sql, params = []) {
  const stmt = db.prepare(sql);
  stmt.bind(params);
  const results = [];
  while (stmt.step()) {
    results.push(stmt.getAsObject());
  }
  stmt.free();
  return results;
}

function queryOne(sql, params = []) {
  const results = queryAll(sql, params);
  return results.length > 0 ? results[0] : null;
}

function runSql(sql, params = []) {
  db.run(sql, params);
}

// ============ Keywords ============

function getKeywords(project) {
  return queryAll('SELECT * FROM keywords WHERE project = ? ORDER BY stt ASC', [project]);
}

function getProjects() {
  return queryAll('SELECT DISTINCT project FROM keywords ORDER BY project').map(r => r.project);
}

// ============ Rankings ============

function getLatestRankings(project) {
  return queryAll(`
    SELECT
      k.stt,
      k.keyword,
      r.position,
      r.page,
      r.url,
      r.local_check,
      r.checked_at,
      r.check_time,
      prev.position as prev_position
    FROM keywords k
    LEFT JOIN (
      SELECT keyword_id, position, page, url, local_check, checked_at, check_time,
        ROW_NUMBER() OVER (PARTITION BY keyword_id ORDER BY checked_at DESC, check_time DESC) as rn
      FROM rankings
    ) r ON r.keyword_id = k.id AND r.rn = 1
    LEFT JOIN (
      SELECT keyword_id, position,
        ROW_NUMBER() OVER (PARTITION BY keyword_id ORDER BY checked_at DESC, check_time DESC) as rn
      FROM rankings
    ) prev ON prev.keyword_id = k.id AND prev.rn = 2
    WHERE k.project = ?
    ORDER BY k.stt ASC
  `, [project]);
}

function getKeywordHistory(project, keyword, limit = 30) {
  return queryAll(`
    SELECT r.position, r.page, r.url, r.checked_at, r.check_time
    FROM rankings r
    JOIN keywords k ON k.id = r.keyword_id
    WHERE k.project = ? AND k.keyword = ?
    ORDER BY r.checked_at DESC, r.check_time DESC
    LIMIT ?
  `, [project, keyword, limit]);
}

function getStats(project) {
  return queryOne(`
    SELECT
      COUNT(DISTINCT k.id) as total_keywords,
      SUM(CASE WHEN r.position BETWEEN 1 AND 3 THEN 1 ELSE 0 END) as top3,
      SUM(CASE WHEN r.position BETWEEN 4 AND 10 THEN 1 ELSE 0 END) as top10,
      SUM(CASE WHEN r.position BETWEEN 11 AND 30 THEN 1 ELSE 0 END) as top30,
      SUM(CASE WHEN r.position BETWEEN 31 AND 50 THEN 1 ELSE 0 END) as top50,
      SUM(CASE WHEN r.position > 50 OR r.position IS NULL OR r.position < 0 THEN 1 ELSE 0 END) as not_found,
      ROUND(AVG(CASE WHEN r.position > 0 THEN r.position END), 1) as avg_position
    FROM keywords k
    LEFT JOIN (
      SELECT keyword_id, position,
        ROW_NUMBER() OVER (PARTITION BY keyword_id ORDER BY checked_at DESC, check_time DESC) as rn
      FROM rankings
    ) r ON r.keyword_id = k.id AND r.rn = 1
    WHERE k.project = ?
  `, [project]);
}

// ============ Sync ============

function getLastSync(project) {
  return queryOne('SELECT * FROM sync_log WHERE project = ? ORDER BY synced_at DESC LIMIT 1', [project]);
}

// ============ Save Keywords Only (no rankings) ============

function saveKeywordsOnly(project, keywordsList) {
  let saved = 0;
  for (let i = 0; i < keywordsList.length; i++) {
    const keyword = keywordsList[i].trim();
    if (!keyword) continue;
    runSql(
      'INSERT INTO keywords (project, keyword, stt) VALUES (?, ?, ?) ON CONFLICT(project, keyword) DO UPDATE SET stt = excluded.stt',
      [project, keyword, i + 1]
    );
    saved++;
  }
  saveDb();
  return saved;
}

// ============ Bulk Import ============

function importSheetData(project, rows) {
  let imported = 0;

  for (const row of rows) {
    if (!row.keyword || !row.keyword.trim()) continue;

    // Upsert keyword
    runSql(
      'INSERT INTO keywords (project, keyword, stt) VALUES (?, ?, ?) ON CONFLICT(project, keyword) DO UPDATE SET stt = excluded.stt',
      [project, row.keyword.trim(), row.stt || 0]
    );

    // Get keyword ID
    const kw = queryOne('SELECT id FROM keywords WHERE project = ? AND keyword = ?', [project, row.keyword.trim()]);
    if (!kw) continue;

    // Check if this exact ranking already exists
    const existing = queryOne(
      'SELECT id FROM rankings WHERE keyword_id = ? AND checked_at = ? AND check_time = ?',
      [kw.id, row.date || '', row.time || '']
    );
    if (existing) continue;

    const pos = row.position === '' || row.position === undefined ? null : parseInt(row.position);
    const page = row.page === '' || row.page === undefined ? null : parseInt(row.page);

    runSql(
      'INSERT INTO rankings (keyword_id, position, page, url, local_check, checked_at, check_time) VALUES (?, ?, ?, ?, ?, ?, ?)',
      [kw.id, isNaN(pos) ? null : pos, isNaN(page) ? null : page, row.url || null, row.local || null, row.date || '', row.time || '']
    );
    imported++;
  }

  // Log sync
  runSql('INSERT INTO sync_log (project, rows_count) VALUES (?, ?)', [project, imported]);

  // Save to disk
  saveDb();

  return imported;
}

function saveAiInsights(project, insights) {
  // Delete old insights for this project
  runSql('DELETE FROM ai_insights WHERE project = ?', [project]);
  runSql(
    'INSERT INTO ai_insights (project, insights_json, keyword_count) VALUES (?, ?, ?)',
    [project, JSON.stringify(insights), insights.totalKeywords || 0]
  );
  saveDb();
}

function getAiInsights(project) {
  const results = queryAll(
    'SELECT insights_json, analyzed_at FROM ai_insights WHERE project = ? ORDER BY analyzed_at DESC LIMIT 1',
    [project]
  );
  if (!results.length) return null;
  const row = results[0];
  return {
    ...JSON.parse(row.insights_json),
    analyzedAt: row.analyzed_at,
  };
}

/**
 * Get keywords that have been checked recently (within hoursAgo hours)
 * Used for resume-from-stop feature
 */
function getRecentlyCheckedKeywords(project, hoursAgo = 72) {
  // checked_at is stored as Vietnamese date format (dd/mm/yyyy) and check_time as HH:mm:ss
  // We need to find keywords with recent rankings
  const rows = queryAll(`
    SELECT DISTINCT k.keyword
    FROM keywords k
    JOIN rankings r ON r.keyword_id = k.id
    WHERE k.project = ?
    ORDER BY r.id DESC
  `, [project]);

  // Filter by time - parse the checked_at + check_time
  const now = Date.now();
  const cutoffMs = hoursAgo * 3600 * 1000;
  const recentKeywords = new Set();

  for (const row of rows) {
    // Get the latest check for this keyword
    const latest = queryOne(`
      SELECT r.checked_at, r.check_time
      FROM rankings r
      JOIN keywords k ON k.id = r.keyword_id
      WHERE k.project = ? AND k.keyword = ?
      ORDER BY r.id DESC
      LIMIT 1
    `, [project, row.keyword]);

    if (!latest || !latest.checked_at) continue;

    try {
      // Parse Vietnamese date format: dd/mm/yyyy or d/m/yyyy
      const parts = latest.checked_at.split('/');
      if (parts.length === 3) {
        const day = parseInt(parts[0]);
        const month = parseInt(parts[1]) - 1;
        const year = parseInt(parts[2]);
        const timeParts = (latest.check_time || '00:00:00').split(':');
        const h = parseInt(timeParts[0]) || 0;
        const m = parseInt(timeParts[1]) || 0;
        const s = parseInt(timeParts[2]) || 0;
        const checkDate = new Date(year, month, day, h, m, s);
        if (now - checkDate.getTime() < cutoffMs) {
          recentKeywords.add(row.keyword);
        }
      }
    } catch { }
  }

  return recentKeywords;
}

/**
 * Wipe ranking history for a project
 * @param {string} project - Project name
 * @param {number} count - Number of recent results to delete (0 = all)
 * @returns {number} Number of deleted rows
 */
function wipeRankings(project, count = 0) {
  if (count === 0) {
    // Delete ALL rankings for this project
    const result = runSql(`
      DELETE FROM rankings WHERE keyword_id IN (
        SELECT id FROM keywords WHERE project = ?
      )
    `, [project]);
    saveDb();
    // Count deleted
    const remaining = queryAll(`
      SELECT COUNT(*) as cnt FROM rankings WHERE keyword_id IN (
        SELECT id FROM keywords WHERE project = ?
      )
    `, [project]);
    console.log(`[DB] Wiped all rankings for "${project}"`);
    return result || 0;
  } else {
    // Delete the N most recent rankings for this project
    runSql(`
      DELETE FROM rankings WHERE id IN (
        SELECT r.id FROM rankings r
        JOIN keywords k ON k.id = r.keyword_id
        WHERE k.project = ?
        ORDER BY r.id DESC
        LIMIT ?
      )
    `, [project, count]);
    saveDb();
    console.log(`[DB] Wiped ${count} most recent rankings for "${project}"`);
    return count;
  }
}

/**
 * Delete all keywords and rankings for a project
 */
function deleteKeywords(project) {
  const kwCount = queryOne('SELECT COUNT(*) as c FROM keywords WHERE project = ?', [project]);
  const rkCount = queryOne(
    'SELECT COUNT(*) as c FROM rankings WHERE keyword_id IN (SELECT id FROM keywords WHERE project = ?)', [project]
  );
  runSql('DELETE FROM rankings WHERE keyword_id IN (SELECT id FROM keywords WHERE project = ?)', [project]);
  runSql('DELETE FROM keywords WHERE project = ?', [project]);
  saveDb();
  return { keywords: kwCount?.c || 0, rankings: rkCount?.c || 0 };
}

/**
 * Delete a project entirely — keywords, rankings, and AI insights
 */
function deleteProject(project) {
  const kw = queryOne('SELECT COUNT(*) as c FROM keywords WHERE project = ?', [project])?.c || 0;
  const rk = queryOne(
    'SELECT COUNT(*) as c FROM rankings WHERE keyword_id IN (SELECT id FROM keywords WHERE project = ?)', [project]
  )?.c || 0;
  runSql('DELETE FROM rankings WHERE keyword_id IN (SELECT id FROM keywords WHERE project = ?)', [project]);
  runSql('DELETE FROM keywords WHERE project = ?', [project]);
  runSql('DELETE FROM ai_insights WHERE project = ?', [project]);
  saveDb();
  return { keywords: kw, rankings: rk };
}

// ============ SERP Intelligence Data ============

function saveSerpData(project, keyword, serpData) {
  if (!db || !serpData) return;
  const row = queryOne('SELECT id FROM keywords WHERE project = ? AND keyword = ?', [project, keyword]);
  if (!row) return;
  const kwId = row.id;

  runSql(`INSERT INTO serp_data (keyword_id, paa_json, related_json, competitors_json)
            VALUES (?, ?, ?, ?)`,
    [kwId,
      JSON.stringify(serpData.paa || []),
      JSON.stringify(serpData.relatedSearches || []),
      JSON.stringify(serpData.competitors || []),
    ]);
  saveDb();
}

function getSerpData(project) {
  return queryAll(`
        SELECT k.keyword,
               s.paa_json, s.related_json, s.competitors_json,
               s.collected_at
        FROM serp_data s
        JOIN keywords k ON k.id = s.keyword_id
        WHERE k.project = ?
        AND s.id IN (
            SELECT MAX(s2.id) FROM serp_data s2
            JOIN keywords k2 ON k2.id = s2.keyword_id
            WHERE k2.project = ?
            GROUP BY s2.keyword_id
        )
        ORDER BY k.keyword
    `, [project, project]).map(row => ({
    keyword: row.keyword,
    paa: JSON.parse(row.paa_json || '[]'),
    relatedSearches: JSON.parse(row.related_json || '[]'),
    competitors: JSON.parse(row.competitors_json || '[]'),
    collectedAt: row.collected_at,
  }));
}

module.exports = {
  initDatabase,
  getKeywords,
  getProjects,
  getLatestRankings,
  getKeywordHistory,
  getStats,
  getLastSync,
  importSheetData,
  saveKeywordsOnly,
  saveAiInsights,
  getAiInsights,
  getRecentlyCheckedKeywords,
  wipeRankings,
  deleteKeywords,
  deleteProject,
  saveSerpData,
  getSerpData,
};
