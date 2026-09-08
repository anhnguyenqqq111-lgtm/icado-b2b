/* ============================================
   Rank Dashboard — Frontend Logic
   ============================================ */

const API = '';
let currentProject = '';
let currentDomain = '';
let allRankings = [];
let currentFilter = 'all';
let currentSort = { key: 'stt', dir: 'asc' };
let currentView = 'table';
let distributionChart = null;
let historyChart = null;
let projectDomains = {}; // { projectName: domain }
let sseConnection = null;
let checkerPolling = null;

// ============ Init ============

document.addEventListener('DOMContentLoaded', () => {
    loadProjects();
    setupEventListeners();
    checkWarpStatus();
    pollCheckerStatus();
});

function setupEventListeners() {
    document.getElementById('projectSelect').addEventListener('change', onProjectChange);
    document.getElementById('syncBtn').addEventListener('click', onSync);
    document.getElementById('keywordsBtn').addEventListener('click', openKeywordModal);
    document.getElementById('searchInput').addEventListener('input', onSearch);
    document.getElementById('exportBtn').addEventListener('click', exportCSV);

    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.addEventListener('click', () => onFilterChange(tab));
    });

    document.querySelectorAll('#rankingsTable th.sortable').forEach(th => {
        th.addEventListener('click', () => onSort(th));
    });
}

// ============ Projects ============

async function loadProjects() {
    try {
        const res = await fetch(`${API}/api/projects`);
        const data = await res.json();
        const select = document.getElementById('projectSelect');

        data.projects.forEach(p => {
            const name = typeof p === 'string' ? p : p.name;
            const domain = typeof p === 'string' ? '' : (p.domain || '');
            projectDomains[name] = domain;
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name + (domain ? ` (${domain})` : '');
            select.appendChild(opt);
        });
    } catch (err) {
        console.error('Failed to load projects:', err);
        showToast('Không thể tải danh sách projects', 'error');
    }
}

async function onProjectChange(e) {
    currentProject = e.target.value;
    currentDomain = projectDomains[currentProject] || '';
    // Auto-fill domain input
    const domainInput = document.getElementById('chkDomain');
    if (domainInput && currentDomain) domainInput.value = currentDomain;
    if (!currentProject) {
        document.getElementById('welcomeState').classList.remove('hidden');
        document.getElementById('dashboardContent').classList.add('hidden');
        return;
    }

    document.getElementById('welcomeState').classList.add('hidden');
    document.getElementById('dashboardContent').classList.remove('hidden');

    await loadRankings();
}

// ============ Rankings ============

async function loadRankings() {
    if (!currentProject) return;

    try {
        const res = await fetch(`${API}/api/rankings/${encodeURIComponent(currentProject)}`);
        const data = await res.json();

        allRankings = data.rankings || [];

        if (allRankings.length === 0) {
            document.getElementById('noData').classList.remove('hidden');
            document.querySelector('.table-wrapper').classList.add('hidden');
        } else {
            document.getElementById('noData').classList.add('hidden');
            renderTable();
            // Re-apply current view (table or url-group) after data refresh
            switchView(currentView);
        }

        await loadStats();
        updateDistributionChart();
        updateAuditPanel();
        loadAiInsights();
        loadSyncInfo();
        loadScheduleStatus();
    } catch (err) {
        console.error('Failed to load rankings:', err);
        showToast('Không thể tải dữ liệu ranking', 'error');
    }
}

async function loadStats() {
    try {
        const res = await fetch(`${API}/api/stats/${encodeURIComponent(currentProject)}`);
        const data = await res.json();
        const s = data.stats;

        document.getElementById('statTotal').textContent = s.total_keywords || 0;
        document.getElementById('statTop3').textContent = s.top3 || 0;
        document.getElementById('statTop10').textContent = s.top10 || 0;
        document.getElementById('statTop30').textContent = s.top30 || 0;
        document.getElementById('statNotFound').textContent = s.not_found || 0;
        document.getElementById('statAvg').textContent = s.avg_position || '—';
    } catch (err) {
        console.error('Failed to load stats:', err);
    }
}

async function loadSyncInfo() {
    try {
        const res = await fetch(`${API}/api/stats/${encodeURIComponent(currentProject)}`);
        const data = await res.json();

        if (data.lastSync) {
            document.getElementById('syncStatus').textContent = `Đã sync ${data.lastSync.rows_count} rankings`;
            document.getElementById('lastSyncTime').textContent = `Lần cuối: ${data.lastSync.synced_at}`;
        } else {
            document.getElementById('syncStatus').textContent = 'Chưa sync';
            document.getElementById('lastSyncTime').textContent = '';
        }
    } catch (err) {
        // silent
    }
}

// ============ Render Table ============

function renderTable() {
    const filtered = getFilteredRankings();
    const sorted = getSortedRankings(filtered);
    const tbody = document.getElementById('rankingsBody');

    tbody.innerHTML = sorted.map(r => {
        const pos = r.position;
        const rankClass = getRankClass(pos);
        const rankDisplay = pos > 0 ? pos : 'N/A';
        const trend = getTrend(r.position, r.prev_position);
        const urlDisplay = r.url ? `<a href="${r.url}" target="_blank" rel="noopener">${truncateUrl(r.url)}</a>` : '—';

        // Rank drop alert: highlight if dropped ≥5 positions
        const drop = (r.prev_position > 0 && pos > 0) ? (pos - r.prev_position) : 0;
        const rowClass = drop >= 5 ? 'rank-drop-alert' : '';

        return `
      <tr data-keyword="${escapeHtml(r.keyword)}" onclick="onKeywordClick(this)" class="${rowClass}">
        <td>${r.stt || ''}</td>
        <td class="keyword-text">${escapeHtml(r.keyword)}${drop >= 5 ? ' <span class="drop-badge">⚠️ -' + drop + '</span>' : ''}</td>
        <td><span class="rank-badge ${rankClass}">${rankDisplay}</span></td>
        <td>${r.page > 0 ? r.page : '—'}</td>
        <td class="url-text">${urlDisplay}</td>
        <td style="font-size:11px;color:var(--text-secondary)">${r.local_check || ''}</td>
        <td style="font-size:12px;color:var(--text-secondary)">${r.checked_at || ''} ${r.check_time || ''}</td>
        <td>${trend}</td>
      </tr>
    `;
    }).join('');
}

function getRankClass(position) {
    if (!position || position <= 0) return 'rank-notfound';
    if (position <= 3) return 'rank-top3';
    if (position <= 10) return 'rank-top10';
    if (position <= 20) return 'rank-top30';
    return 'rank-50plus';
}

function getTrend(current, previous) {
    if (!previous || previous <= 0) {
        if (!current || current <= 0) return '<span class="trend-same">—</span>';
        return '<span class="trend-new">NEW</span>';
    }
    if (!current || current <= 0) return '<span class="trend-down">↓ OUT</span>';

    const diff = previous - current;
    if (diff > 0) return `<span class="trend-up">↑ ${diff}</span>`;
    if (diff < 0) return `<span class="trend-down">↓ ${Math.abs(diff)}</span>`;
    return '<span class="trend-same">—</span>';
}

function truncateUrl(url) {
    try {
        const u = new URL(url);
        const path = u.pathname.replace(/\/$/, '');
        if (path.length > 40) return u.hostname + path.substring(0, 37) + '...';
        return u.hostname + path;
    } catch {
        return url.substring(0, 50);
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

// ============ Filters ============

function onFilterChange(tab) {
    document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    currentFilter = tab.dataset.filter;
    renderTable();
}

function onSearch() {
    renderTable();
}

function getFilteredRankings() {
    let filtered = [...allRankings];
    const search = document.getElementById('searchInput').value.toLowerCase().trim();

    if (search) {
        filtered = filtered.filter(r =>
            (r.keyword && r.keyword.toLowerCase().includes(search)) ||
            (r.url && r.url.toLowerCase().includes(search))
        );
    }

    switch (currentFilter) {
        case 'top3':
            filtered = filtered.filter(r => r.position >= 1 && r.position <= 3);
            break;
        case 'top10':
            filtered = filtered.filter(r => r.position >= 1 && r.position <= 10);
            break;
        case 'top30':
            filtered = filtered.filter(r => r.position >= 1 && r.position <= 30);
            break;
        case 'notfound':
            filtered = filtered.filter(r => !r.position || r.position <= 0);
            break;
        case 'dropping':
            filtered = filtered.filter(r => {
                if (!r.prev_position || r.prev_position <= 0 || !r.position || r.position <= 0) return false;
                return (r.position - r.prev_position) >= 5;
            });
            break;
    }

    return filtered;
}

// ============ Export CSV ============

function exportCSV() {
    const data = getFilteredRankings();
    if (data.length === 0) {
        showToast('Không có dữ liệu để export', 'error');
        return;
    }

    const headers = ['STT', 'Từ khóa', 'Vị trí', 'Trang', 'URL', 'Local', 'Ngày check', 'Giờ check', 'Vị trí trước', 'Thay đổi'];
    const rows = data.map(r => {
        const change = (r.prev_position > 0 && r.position > 0) ? (r.prev_position - r.position) : '';
        return [
            r.stt || '',
            `"${(r.keyword || '').replace(/"/g, '""')}"`,
            r.position > 0 ? r.position : 'N/A',
            r.page > 0 ? r.page : '',
            `"${(r.url || '').replace(/"/g, '""')}"`,
            `"${(r.local_check || '').replace(/"/g, '""')}"`,
            r.checked_at || '',
            r.check_time || '',
            r.prev_position > 0 ? r.prev_position : '',
            change,
        ].join(',');
    });

    const csv = '\uFEFF' + headers.join(',') + '\n' + rows.join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentProject}_rankings_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}

// ============ Sort ============

function onSort(th) {
    const key = th.dataset.sort;

    document.querySelectorAll('#rankingsTable th').forEach(t => {
        t.classList.remove('sort-asc', 'sort-desc');
    });

    if (currentSort.key === key) {
        currentSort.dir = currentSort.dir === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort = { key, dir: 'asc' };
    }

    th.classList.add(currentSort.dir === 'asc' ? 'sort-asc' : 'sort-desc');
    renderTable();
}

function getSortedRankings(rankings) {
    const { key, dir } = currentSort;
    return [...rankings].sort((a, b) => {
        let aVal = a[key];
        let bVal = b[key];

        // Handle null/undefined positions
        if (key === 'position') {
            aVal = aVal > 0 ? aVal : 999;
            bVal = bVal > 0 ? bVal : 999;
        }

        if (typeof aVal === 'string') {
            aVal = (aVal || '').toLowerCase();
            bVal = (bVal || '').toLowerCase();
        }

        if (aVal < bVal) return dir === 'asc' ? -1 : 1;
        if (aVal > bVal) return dir === 'asc' ? 1 : -1;
        return 0;
    });
}

// ============ Charts ============

function updateDistributionChart() {
    const stats = {
        top3: allRankings.filter(r => r.position >= 1 && r.position <= 3).length,
        top10: allRankings.filter(r => r.position >= 4 && r.position <= 10).length,
        top30: allRankings.filter(r => r.position >= 11 && r.position <= 20).length,
        top50: allRankings.filter(r => r.position >= 21 && r.position <= 50).length,
        notfound: allRankings.filter(r => !r.position || r.position <= 0).length,
    };

    const ctx = document.getElementById('distributionChart').getContext('2d');

    if (distributionChart) distributionChart.destroy();

    distributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Top 3', 'Top 4-10', 'Top 11-20', 'Top 21-50', 'Không tìm thấy'],
            datasets: [{
                data: [stats.top3, stats.top10, stats.top30, stats.top50, stats.notfound],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.9)',
                    'rgba(74, 222, 128, 0.8)',
                    'rgba(234, 179, 8, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(148, 163, 184, 0.6)',
                ],
                borderColor: '#ffffff',
                borderWidth: 3,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#64748b',
                        font: { family: "'Inter', sans-serif", size: 11, weight: 500 },
                        padding: 12,
                        usePointStyle: true,
                        pointStyleWidth: 8,
                    }
                },
                tooltip: {
                    backgroundColor: '#ffffff',
                    borderColor: '#e2e8f0',
                    borderWidth: 1,
                    cornerRadius: 8,
                    titleFont: { family: "'Inter', sans-serif", weight: 600, color: '#1a1a2e' },
                    bodyFont: { family: "'Inter', sans-serif" },
                    titleColor: '#1a1a2e',
                    bodyColor: '#374151',
                    padding: 10,
                    callbacks: {
                        label: ctx => {
                            const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = total > 0 ? Math.round(ctx.parsed / total * 100) : 0;
                            return ` ${ctx.label}: ${ctx.parsed} (${pct}%)`;
                        }
                    }
                }
            }
        }
    });
}

async function onKeywordClick(row) {
    // Deselect previous
    document.querySelectorAll('#rankingsTable tbody tr.selected').forEach(tr => tr.classList.remove('selected'));
    row.classList.add('selected');

    const keyword = row.dataset.keyword;
    if (!keyword) return;

    document.getElementById('historyChartTitle').textContent = `Lịch sử: "${keyword}"`;
    document.getElementById('historyHint').classList.add('hidden');

    try {
        const res = await fetch(`${API}/api/history/${encodeURIComponent(currentProject)}/${encodeURIComponent(keyword)}`);
        const data = await res.json();
        renderHistoryChart(data.history || []);
    } catch (err) {
        console.error('Failed to load history:', err);
    }
}

function renderHistoryChart(history) {
    const ctx = document.getElementById('historyChart').getContext('2d');

    if (historyChart) historyChart.destroy();

    // Reverse to chronological order
    const sorted = [...history].reverse();

    historyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sorted.map(h => `${h.checked_at || ''}`),
            datasets: [{
                label: 'Vị trí',
                data: sorted.map(h => h.position > 0 ? h.position : null),
                borderColor: '#22c55e',
                backgroundColor: 'rgba(34, 197, 94, 0.08)',
                borderWidth: 2.5,
                pointRadius: 4,
                pointBackgroundColor: '#22c55e',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                tension: 0.3,
                fill: true,
                spanGaps: true,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    reverse: true,
                    min: 1,
                    grid: { color: 'rgba(226, 232, 240, 0.5)' },
                    ticks: {
                        color: '#64748b',
                        font: { family: "'Inter', sans-serif", size: 11 },
                        stepSize: 5,
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#64748b',
                        font: { family: "'Inter', sans-serif", size: 10 },
                        maxRotation: 45,
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#ffffff',
                    borderColor: '#22c55e',
                    borderWidth: 1,
                    cornerRadius: 8,
                    titleFont: { family: "'Inter', sans-serif" },
                    bodyFont: { family: "'Inter', sans-serif", weight: 600 },
                    titleColor: '#1a1a2e',
                    bodyColor: '#374151',
                    padding: 10,
                    callbacks: {
                        label: ctx => ` Vị trí: ${ctx.parsed.y}`
                    }
                }
            }
        }
    });
}

// ============ Sync ============

async function onSync() {
    if (!currentProject) {
        showToast('Chọn project trước khi sync', 'error');
        return;
    }

    const btn = document.getElementById('syncBtn');
    btn.classList.add('loading');
    btn.disabled = true;

    try {
        const res = await fetch(`${API}/api/sync/${encodeURIComponent(currentProject)}`, {
            method: 'POST'
        });
        const data = await res.json();

        if (data.success) {
            showToast(`Sync thành công: ${data.imported} rankings mới`, 'success');
            await loadRankings();
        } else {
            showToast(data.error || 'Sync thất bại', 'error');
        }
    } catch (err) {
        showToast('Lỗi kết nối: ' + err.message, 'error');
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}

// ============ Native Checker Control ============

let checkerSSE = null;

async function startNativeChecker() {
    if (!currentProject) {
        showToast('Chọn project trước', 'error');
        return;
    }

    const maxPages = parseInt(document.getElementById('chkMaxPages').value) || 5;
    const chunkSize = parseInt(document.getElementById('chkChunkSize').value) || 5;
    const domainInput = document.getElementById('chkDomain');
    const domain = (domainInput ? domainInput.value.trim() : '') || currentDomain;

    if (!domain) {
        showToast('Nhập domain trước (VD: telosacademy.edu.vn)', 'error');
        if (domainInput) domainInput.focus();
        return;
    }

    const startBtn = document.getElementById('checkerStartBtn');
    startBtn.disabled = true;
    startBtn.classList.add('loading');

    try {
        const res = await fetch(`${API}/api/checker/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project: currentProject,
                domain: domain,
                options: { maxPages, chunkSize },
            }),
        });
        const data = await res.json();

        if (data.success) {
            showToast(`Đang check ${data.total} keywords...`, 'success');
            document.getElementById('checkerPauseBtn').disabled = false;
            document.getElementById('checkerStopBtn').disabled = false;
            document.getElementById('checkerProgress').style.display = 'flex';
            startCheckerSSE();
        } else {
            showToast(data.error || data.message || 'Lỗi', 'error');
            startBtn.disabled = false;
            startBtn.classList.remove('loading');
        }
    } catch (err) {
        showToast('Lỗi: ' + err.message, 'error');
        startBtn.disabled = false;
        startBtn.classList.remove('loading');
    }
}

function stopNativeChecker() {
    fetch(`${API}/api/checker/stop`, { method: 'POST' })
        .then(r => r.json())
        .then(d => showToast(d.message || 'Stopped', 'info'))
        .catch(e => showToast('Lỗi: ' + e.message, 'error'));
}

function pauseNativeChecker() {
    fetch(`${API}/api/checker/pause`, { method: 'POST' })
        .then(r => r.json())
        .then(d => {
            const btn = document.getElementById('checkerPauseBtn');
            if (d.state === 'paused') {
                btn.textContent = '▶ Resume';
            } else {
                btn.textContent = '⏸ Pause';
            }
        })
        .catch(e => showToast('Lỗi: ' + e.message, 'error'));
}

function toggleWipeMenu() {
    const menu = document.getElementById('wipeMenu');
    menu.classList.toggle('hidden');
    // Close on outside click
    if (!menu.classList.contains('hidden')) {
        setTimeout(() => {
            document.addEventListener('click', function closeMenu(e) {
                if (!e.target.closest('.wipe-control')) {
                    menu.classList.add('hidden');
                    document.removeEventListener('click', closeMenu);
                }
            });
        }, 10);
    }
}

async function wipeHistory(count) {
    document.getElementById('wipeMenu').classList.add('hidden');

    const label = count === 0 ? 'tất cả' : `${count} gần nhất`;
    if (!confirm(`Xóa ${label} kết quả check rank của "${currentProject}"?`)) return;

    try {
        const res = await fetch(`${API}/api/rankings/wipe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project: currentProject, count }),
        });
        const data = await res.json();
        if (data.success) {
            showToast(`Đã xóa ${data.deleted} kết quả`, 'info');
            loadRankings();
        } else {
            showToast(data.error || 'Lỗi', 'error');
        }
    } catch (e) {
        showToast('Lỗi: ' + e.message, 'error');
    }
}

async function deleteProjectKeywords() {
    document.getElementById('wipeMenu').classList.add('hidden');
    if (!currentProject) return;

    if (!confirm(`⚠️ Xóa TẤT CẢ keywords và dữ liệu ranking của "${currentProject}"?\n\nThao tác này không thể hoàn tác!`)) return;

    try {
        const res = await fetch(`${API}/api/keywords/${encodeURIComponent(currentProject)}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            showToast(`Đã xóa ${data.keywords} keywords + ${data.rankings} rankings`, 'info');
            loadRankings();
        } else {
            showToast(data.error || 'Lỗi', 'error');
        }
    } catch (e) {
        showToast('Lỗi: ' + e.message, 'error');
    }
}

async function deleteCurrentProject() {
    if (!currentProject) { showToast('Chọn project trước', 'error'); return; }
    if (!confirm(`🗑️ Xóa hoàn toàn project "${currentProject}"?\n\nTất cả keywords, rankings và AI insights sẽ bị xóa.\nThao tác này không thể hoàn tác!`)) return;

    try {
        const res = await fetch(`${API}/api/projects/${encodeURIComponent(currentProject)}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            showToast(`Đã xóa project "${currentProject}" (${data.keywords} kw, ${data.rankings} rankings)`, 'info');
            currentProject = '';
            document.getElementById('projectSelect').value = '';
            loadProjects();
        } else {
            showToast(data.error || 'Lỗi', 'error');
        }
    } catch (e) {
        showToast('Lỗi: ' + e.message, 'error');
    }
}

// ============ Schedule ============

async function toggleSchedule() {
    const interval = document.getElementById('scheduleInterval').value;
    const statusEl = document.getElementById('scheduleStatus');

    if (!interval) {
        // Stop schedule
        try {
            await fetch(`${API}/api/scheduler/stop`, { method: 'POST' });
            statusEl.textContent = '';
            document.getElementById('scheduleBtn').textContent = '📅 Đặt lịch';
        } catch (e) {
            showToast('Lỗi: ' + e.message, 'error');
        }
        return;
    }

    if (!currentProject) {
        showToast('Chọn project trước', 'error');
        return;
    }

    const domain = document.getElementById('chkDomain')?.value?.trim() || currentDomain;
    const hours = parseInt(interval);

    try {
        const res = await fetch(`${API}/api/scheduler/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project: currentProject,
                domain,
                options: {
                    maxPages: parseInt(document.getElementById('chkMaxPages').value) || 5,
                    chunkSize: parseInt(document.getElementById('chkChunkSize').value) || 5,
                },
                schedule: { intervalHours: hours },
            }),
        });
        const data = await res.json();
        if (data.running) {
            statusEl.textContent = `✅ Auto-check mỗi ${hours}h`;
            document.getElementById('scheduleBtn').textContent = '⏹ Tắt lịch';
        }
    } catch (e) {
        showToast('Lỗi: ' + e.message, 'error');
    }
}

async function loadScheduleStatus() {
    try {
        const res = await fetch(`${API}/api/scheduler/status`);
        const data = await res.json();
        const statusEl = document.getElementById('scheduleStatus');
        if (data.running) {
            statusEl.textContent = `✅ Đang chạy — lần tiếp: ${data.nextRun || '—'}`;
            document.getElementById('scheduleBtn').textContent = '⏹ Tắt lịch';
        }
    } catch { }
}

function startCheckerSSE() {
    if (checkerSSE) checkerSSE.close();
    checkerSSE = new EventSource(`${API}/api/checker/stream`);

    checkerSSE.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === 'result') {
                onCheckerResult(data);
            } else if (data.type === 'status') {
                updateCheckerUI(data);
            }
        } catch { }
    };

    checkerSSE.onerror = () => {
        // SSE will auto-reconnect
    };
}

function onCheckerResult(r) {
    // Add result to rankings table in real-time
    const tbody = document.getElementById('rankingsBody');
    const rankClass = getRankClass(parseInt(r.rank) || 0);
    const rankDisplay = r.rank && r.rank !== '-' ? r.rank : 'N/A';
    const urlDisplay = r.url && !r.url.startsWith('[x]') ? `<a href="${r.url}" target="_blank">${truncateUrl(r.url)}</a>` : (r.url || '—');
    const captchaWarn = r.captcha ? ' 🛡️' : '';
    const serpTags = (r.serpFeatures || []).map(f => `<span class="serp-tag">${f}</span>`).join('');

    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${r.idx || ''}</td>
        <td class="keyword-text">${escapeHtml(r.keyword)}${captchaWarn}${serpTags ? '<div class="serp-features">' + serpTags + '</div>' : ''}</td>
        <td><span class="rank-badge ${rankClass}">${rankDisplay}</span></td>
        <td>${r.page && r.page !== '-' ? r.page : '—'}</td>
        <td class="url-text">${urlDisplay}</td>
        <td style="font-size:11px;color:var(--text-secondary)">${r.local || ''}</td>
        <td style="font-size:12px;color:var(--text-secondary)">${r.date || ''} ${r.time || ''}</td>
        <td>—</td>
    `;
    tbody.appendChild(tr);
}

function updateCheckerUI(status) {
    const pct = status.percent || 0;
    const fill = document.getElementById('checkerProgressFill');
    const text = document.getElementById('checkerProgressText');
    if (fill) fill.style.width = pct + '%';
    if (text) text.textContent = `${status.done || 0}/${status.total || 0} | ${pct}%`;

    if (status.state === 'done' || status.state === 'idle' || status.state === 'error') {
        const startBtn = document.getElementById('checkerStartBtn');
        startBtn.disabled = false;
        startBtn.classList.remove('loading');
        document.getElementById('checkerPauseBtn').disabled = true;
        document.getElementById('checkerStopBtn').disabled = true;
        document.getElementById('checkerPauseBtn').textContent = '⏸ Pause';

        if (status.state === 'done') {
            // Reload rankings from DB
            setTimeout(() => loadRankings(), 1000);
        }

        if (checkerSSE) { checkerSSE.close(); checkerSSE = null; }
    }
}

async function pollCheckerStatus() {
    try {
        const res = await fetch(`${API}/api/checker/status`);
        const status = await res.json();

        if (status.state === 'running' || status.state === 'paused') {
            updateCheckerUI(status);
            document.getElementById('checkerProgress').style.display = 'flex';
            document.getElementById('checkerStartBtn').disabled = true;
            document.getElementById('checkerStartBtn').classList.add('loading');
            document.getElementById('checkerPauseBtn').disabled = false;
            document.getElementById('checkerStopBtn').disabled = false;
            startCheckerSSE();
        } else {
            updateCheckerUI(status);
        }
    } catch { }

    // Keep polling
    setInterval(async () => {
        try {
            const res = await fetch(`${API}/api/checker/status`);
            const status = await res.json();
            updateCheckerUI(status);
        } catch { }
    }, 5000);
}

// ============ Open Sheet ============

async function openLinkedSheet() {
    try {
        const res = await fetch(`${API}/api/settings`);
        const data = await res.json();
        const sheetId = data.GOOGLE_SHEET_ID;
        if (sheetId) {
            window.open(`https://docs.google.com/spreadsheets/d/${sheetId}`, '_blank');
        } else {
            showToast('Chưa cấu hình Google Sheet ID', 'error');
        }
    } catch (e) {
        showToast('Lỗi: ' + e.message, 'error');
    }
}

// ============ WARP Control ============

async function checkWarpStatus() {
    try {
        const res = await fetch(`${API}/api/warp/status`);
        const data = await res.json();
        const dot = document.getElementById('warpIndicator');
        const btn = document.getElementById('warpToggleBtn');
        if (!dot || !btn) return;

        if (data.status === 'connected') {
            dot.classList.remove('offline');
            dot.classList.add('online');
            dot.title = 'WARP Connected';
            btn.textContent = 'WARP ON';
        } else if (data.status === 'disconnected') {
            dot.classList.remove('online');
            dot.classList.add('offline');
            dot.title = 'WARP Disconnected';
            btn.textContent = 'WARP OFF';
        } else {
            dot.classList.remove('online');
            dot.classList.add('offline');
            dot.title = data.installed ? 'WARP: Unknown' : 'WARP: Not installed';
            btn.textContent = 'WARP';
            if (!data.installed) btn.disabled = true;
        }
    } catch { }
}

async function toggleWarp() {
    const btn = document.getElementById('warpToggleBtn');
    btn.disabled = true;
    try {
        const res = await fetch(`${API}/api/warp/toggle`, { method: 'POST' });
        const data = await res.json();
        showToast(data.success ? `WARP: ${data.newState}` : 'WARP toggle failed', data.success ? 'success' : 'error');
        await checkWarpStatus();
    } catch (err) {
        showToast('WARP error: ' + err.message, 'error');
    } finally {
        btn.disabled = false;
    }
}

// ============ Settings Modal ============

async function openSettingsModal() {
    document.getElementById('settingsModal').classList.remove('hidden');
    try {
        const res = await fetch(`${API}/api/settings`);
        const s = await res.json();
        document.getElementById('settingSheetId').value = s.GOOGLE_SHEET_ID || '';
        document.getElementById('settingUule').value = s.UULE_CODE || '';
    } catch { }

    // Check OAuth status
    try {
        const res = await fetch(`${API}/api/sheets/auth-url`);
        const data = await res.json();
        const el = document.getElementById('oauthStatus');
        if (data.authenticated) {
            el.innerHTML = '<span style="color:var(--green)">✅ Đã xác thực</span>';
        } else if (data.authUrl) {
            el.innerHTML = `<span style="color:var(--yellow)">⚠️ Chưa xác thực</span><br><a href="${data.authUrl}" onclick="closeSettingsModal()">Click để xác thực Google Sheets</a>`;
        }
    } catch { }

    // Check Ollama status
    await checkOllamaStatus();
}

let ollamaRunning = false;

async function checkOllamaStatus() {
    try {
        const res = await fetch(`${API}/api/ai/provider`);
        const data = await res.json();
        const textEl = document.getElementById('ollamaStatusText');
        const btnEl = document.getElementById('ollamaToggleBtn');
        ollamaRunning = data.ollama?.available || false;

        if (ollamaRunning) {
            const model = data.ollama?.model || 'unknown';
            textEl.innerHTML = `<span style="color:var(--green)">✅ Đang chạy</span> <span style="color:var(--text-dim);font-size:12px">(${model})</span>`;
            btnEl.textContent = '⏹ Tắt Ollama';
            btnEl.style.background = 'var(--red, #ef4444)';
        } else {
            textEl.innerHTML = '<span style="color:var(--text-dim)">⏹ Đã tắt</span>';
            btnEl.textContent = '▶ Bật Ollama';
            btnEl.style.background = 'var(--green, #22c55e)';
        }
        btnEl.style.display = 'inline-block';
        btnEl.style.color = '#fff';
        btnEl.style.border = 'none';
        btnEl.style.borderRadius = '6px';
        btnEl.style.cursor = 'pointer';
    } catch { }
}

async function toggleOllama() {
    const btn = document.getElementById('ollamaToggleBtn');
    const textEl = document.getElementById('ollamaStatusText');
    btn.disabled = true;

    if (ollamaRunning) {
        btn.textContent = '⏳ Đang tắt...';
        try {
            await fetch(`${API}/api/ai/ollama/stop`, { method: 'POST' });
            showToast('Ollama đã tắt — tiết kiệm RAM', 'info');
        } catch { }
    } else {
        btn.textContent = '⏳ Đang khởi động...';
        textEl.innerHTML = '<span style="color:var(--yellow)">⏳ Đang khởi động (~5s)...</span>';
        try {
            const res = await fetch(`${API}/api/ai/ollama/start`, { method: 'POST' });
            const data = await res.json();
            if (data.started) {
                showToast('Ollama đã bật — sẵn sàng cho AI Insights', 'success');
            } else {
                showToast(data.message || 'Không thể khởi động Ollama', 'error');
            }
        } catch { }
    }

    btn.disabled = false;
    await checkOllamaStatus();
}

function closeSettingsModal() {
    document.getElementById('settingsModal').classList.add('hidden');
}

async function saveSettingsModal() {
    try {
        const body = {
            GOOGLE_SHEET_ID: document.getElementById('settingSheetId').value.trim(),
            UULE_CODE: document.getElementById('settingUule').value.trim(),
        };
        const res = await fetch(`${API}/api/settings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        const data = await res.json();
        if (data.success) {
            showToast('Đã lưu cài đặt', 'success');
            closeSettingsModal();
        } else {
            showToast(data.error || 'Lỗi', 'error');
        }
    } catch (err) {
        showToast('Lỗi: ' + err.message, 'error');
    }
}

function onExport() {
    if (allRankings.length === 0) {
        showToast('Không có dữ liệu để export', 'error');
        return;
    }

    const headers = ['STT', 'Từ khóa', 'Vị trí', 'Trang', 'URL', 'Local', 'Cập nhật', 'Giờ check', 'Trend'];
    const rows = allRankings.map(r => {
        const trend = r.prev_position ? (r.prev_position - (r.position || 0)) : '';
        return [
            r.stt || '',
            r.keyword || '',
            r.position > 0 ? r.position : 'N/A',
            r.page > 0 ? r.page : '',
            r.url || '',
            r.local_check || '',
            r.checked_at || '',
            r.check_time || '',
            trend
        ];
    });

    const csv = [headers, ...rows].map(row =>
        row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')
    ).join('\n');

    const bom = '\uFEFF';
    const blob = new Blob([bom + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rankings_${currentProject}_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);

    showToast('Export CSV thành công', 'success');
}

// ============ Toast ============

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;

    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// ============ Keyword Management ============

async function openKeywordModal() {
    if (!currentProject) {
        showToast('Chọn project trước', 'error');
        return;
    }

    document.getElementById('keywordModal').classList.remove('hidden');

    // Load existing keywords
    try {
        const res = await fetch(`${API}/api/keywords/${encodeURIComponent(currentProject)}`);
        const data = await res.json();
        const keywords = (data.keywords || []).map(k => k.keyword);
        document.getElementById('keywordInput').value = keywords.join('\n');
        document.getElementById('keywordCount').textContent = `${keywords.length} từ khóa đã lưu`;
    } catch (err) {
        console.error('Failed to load keywords:', err);
    }
}

function closeKeywordModal() {
    document.getElementById('keywordModal').classList.add('hidden');
}

async function saveKeywords() {
    if (!currentProject) return;

    const text = document.getElementById('keywordInput').value;
    const keywords = text.split('\n').map(k => k.trim()).filter(k => k.length > 0);

    if (keywords.length === 0) {
        showToast('Chưa nhập từ khóa nào', 'error');
        return;
    }

    try {
        const res = await fetch(`${API}/api/keywords/${encodeURIComponent(currentProject)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords }),
        });
        const data = await res.json();

        if (data.success) {
            showToast(`Đã lưu ${keywords.length} từ khóa`, 'success');
            document.getElementById('keywordCount').textContent = `${keywords.length} từ khóa đã lưu`;
            closeKeywordModal();
        } else {
            showToast(data.error || 'Lỗi lưu từ khóa', 'error');
        }
    } catch (err) {
        showToast('Lỗi: ' + err.message, 'error');
    }
}

// ============ Create Project ============

async function createProject() {
    const nameInput = document.getElementById('newProjectName');
    const kwInput = document.getElementById('newProjectKeywords');
    const projectName = nameInput.value.trim();
    const keywordsText = kwInput.value.trim();

    if (!projectName) {
        showToast('Nhập tên project', 'error');
        nameInput.focus();
        return;
    }

    if (!keywordsText) {
        showToast('Nhập ít nhất 1 từ khóa', 'error');
        kwInput.focus();
        return;
    }

    const keywords = keywordsText.split('\n').map(k => k.trim()).filter(k => k.length > 0);
    const btn = document.getElementById('createProjectBtn');
    btn.classList.add('loading');
    btn.disabled = true;

    try {
        // 1. Save keywords
        const kwRes = await fetch(`${API}/api/keywords/${encodeURIComponent(projectName)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords }),
        });
        const kwData = await kwRes.json();

        if (!kwData.success) {
            showToast(kwData.error || 'Lỗi lưu từ khóa', 'error');
            return;
        }

        showToast(`Đã tạo project "${projectName}" với ${keywords.length} từ khóa`, 'success');

        // 2. Add project to dropdown and select it
        const select = document.getElementById('projectSelect');
        let exists = false;
        for (const opt of select.options) {
            if (opt.value === projectName) { exists = true; break; }
        }
        if (!exists) {
            const opt = document.createElement('option');
            opt.value = projectName;
            opt.textContent = projectName;
            select.appendChild(opt);
        }
        select.value = projectName;
        currentProject = projectName;

        // 3. Switch to dashboard view
        document.getElementById('welcomeState').classList.add('hidden');
        document.getElementById('dashboardContent').classList.remove('hidden');

        // 4. Try to sync ranking data from Sheet
        try {
            const syncRes = await fetch(`${API}/api/sync/${encodeURIComponent(projectName)}`, { method: 'POST' });
            const syncData = await syncRes.json();
            if (syncData.success && syncData.imported > 0) {
                showToast(`Sync thành công: ${syncData.imported} rankings`, 'success');
            }
        } catch (e) {
            // Sync may fail if sheet doesn't exist yet — that's ok
        }

        // 5. Load rankings
        await loadRankings();

    } catch (err) {
        showToast('Lỗi: ' + err.message, 'error');
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}

// ============ Audit Panel ============

function updateAuditPanel() {
    const critical = []; // Not found
    const warning = [];  // Ranking 11-50
    const down = [];     // Trend down
    const ok = [];       // Top 10

    for (const r of allRankings) {
        const pos = r.position;
        const prev = r.prev_position;
        const kw = r.keyword || `#${r.stt}`;

        if (!pos || pos <= 0) {
            critical.push({ keyword: kw, position: pos, label: 'N/A' });
        } else if (pos <= 10) {
            // Check if dropping
            if (prev && prev > 0 && pos > prev) {
                down.push({ keyword: kw, position: pos, prev, diff: pos - prev });
            } else {
                ok.push({ keyword: kw, position: pos });
            }
        } else {
            // Check if dropping
            if (prev && prev > 0 && pos > prev) {
                down.push({ keyword: kw, position: pos, prev, diff: pos - prev });
            } else {
                warning.push({ keyword: kw, position: pos });
            }
        }
    }

    // Sort by position
    warning.sort((a, b) => a.position - b.position);
    down.sort((a, b) => b.diff - a.diff);
    ok.sort((a, b) => a.position - b.position);

    // Update counts
    document.getElementById('auditCriticalCount').textContent = critical.length;
    document.getElementById('auditWarningCount').textContent = warning.length;
    document.getElementById('auditDownCount').textContent = down.length;
    document.getElementById('auditOkCount').textContent = ok.length;

    // Summary
    const needAction = critical.length + warning.length + down.length;
    document.getElementById('auditSummary').textContent = needAction > 0
        ? `${needAction} keywords cần hành động`
        : 'Tất cả keywords đang tốt';

    // Render lists
    document.getElementById('auditCriticalList').innerHTML = critical.slice(0, 20).map(r =>
        `<div class="audit-item"><span class="audit-item-kw">${escapeHtml(r.keyword)}</span><span class="audit-item-pos pos-na">N/A</span></div>`
    ).join('');

    document.getElementById('auditWarningList').innerHTML = warning.slice(0, 20).map(r =>
        `<div class="audit-item"><span class="audit-item-kw">${escapeHtml(r.keyword)}</span><span class="audit-item-pos pos-yellow">#${r.position}</span></div>`
    ).join('');

    document.getElementById('auditDownList').innerHTML = down.slice(0, 20).map(r =>
        `<div class="audit-item"><span class="audit-item-kw">${escapeHtml(r.keyword)}</span><span class="audit-item-pos pos-red">#${r.position} ↓${r.diff}</span></div>`
    ).join('');

    document.getElementById('auditOkList').innerHTML = ok.slice(0, 20).map(r =>
        `<div class="audit-item"><span class="audit-item-kw">${escapeHtml(r.keyword)}</span><span class="audit-item-pos pos-green">#${r.position}</span></div>`
    ).join('');
}

// ============ View Switching ============

function switchView(view) {
    currentView = view;

    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });

    const tableWrapper = document.querySelector('.table-wrapper');
    const urlGroupView = document.getElementById('urlGroupView');
    const filterTabs = document.getElementById('filterTabs');

    if (view === 'table') {
        tableWrapper.classList.remove('hidden');
        urlGroupView.classList.add('hidden');
        filterTabs.style.display = '';
    } else {
        tableWrapper.classList.add('hidden');
        urlGroupView.classList.remove('hidden');
        filterTabs.style.display = 'none';
        renderUrlGroupView();
    }
}

function renderUrlGroupView() {
    const container = document.getElementById('urlGroupView');
    const search = document.getElementById('searchInput').value.toLowerCase().trim();

    // Group rankings by URL
    const groups = {};
    for (const r of allRankings) {
        const url = r.url || '(không có URL)';
        if (!groups[url]) {
            groups[url] = { url, keywords: [], positions: [] };
        }
        groups[url].keywords.push(r);
        if (r.position && r.position > 0) {
            groups[url].positions.push(r.position);
        }
    }

    // Convert to array and sort by keyword count (desc)
    let groupArr = Object.values(groups).map(g => ({
        ...g,
        count: g.keywords.length,
        avgPos: g.positions.length > 0
            ? Math.round(g.positions.reduce((a, b) => a + b, 0) / g.positions.length * 10) / 10
            : null,
    }));

    // Apply search filter
    if (search) {
        groupArr = groupArr.filter(g =>
            g.url.toLowerCase().includes(search) ||
            g.keywords.some(k => (k.keyword || '').toLowerCase().includes(search))
        );
    }

    // Sort: most keywords first, then by avg position
    groupArr.sort((a, b) => b.count - a.count || (a.avgPos || 999) - (b.avgPos || 999));

    container.innerHTML = groupArr.map((g, idx) => {
        const isNoUrl = g.url === '(không có URL)';
        const urlDisplay = isNoUrl
            ? '<em>(không có URL — chưa index)</em>'
            : `<a href="${escapeHtml(g.url)}" target="_blank" rel="noopener">${escapeHtml(g.url)}</a>`;
        const avgDisplay = g.avgPos !== null ? `Avg: #${g.avgPos}` : 'N/A';

        const kwRows = g.keywords.map(k => {
            const pos = k.position && k.position > 0 ? k.position : 'N/A';
            const rankClass = getRankClass(k.position);
            return `<tr>
                <td>${k.stt || ''}</td>
                <td style="font-weight:500">${escapeHtml(k.keyword || '')}</td>
                <td><span class="rank-badge ${rankClass}">${pos}</span></td>
                <td>${k.checked_at || ''}</td>
            </tr>`;
        }).join('');

        return `
        <div class="url-group-card ${isNoUrl ? 'no-url' : ''}" id="urlgroup-${idx}">
            <div class="url-group-header" onclick="toggleUrlGroup(${idx})">
                <span class="url-group-url">${urlDisplay}</span>
                <div class="url-group-meta">
                    <span class="url-group-stat kw-count">${g.count} keywords</span>
                    <span class="url-group-stat avg-pos">${avgDisplay}</span>
                    <span class="url-group-chevron">▶</span>
                </div>
            </div>
            <div class="url-group-keywords">
                <table>
                    <thead><tr><th>#</th><th>Từ khóa</th><th>Vị trí</th><th>Cập nhật</th></tr></thead>
                    <tbody>${kwRows}</tbody>
                </table>
            </div>
        </div>`;
    }).join('');
}

function toggleUrlGroup(idx) {
    const card = document.getElementById(`urlgroup-${idx}`);
    if (card) card.classList.toggle('expanded');
}

// ============ AI Insights ============

let aiPollInterval = null;

async function loadAiInsights() {
    if (!currentProject) return;
    try {
        const res = await fetch(`/api/ai/insights/${encodeURIComponent(currentProject)}`);
        const data = await res.json();

        if (data.insights) {
            renderAiInsights(data.insights);
            document.getElementById('aiInsightsPanel').classList.remove('hidden');
        } else {
            document.getElementById('aiInsightsPanel').classList.add('hidden');
        }
    } catch (err) {
        console.error('Failed to load AI insights:', err);
    }
}

async function triggerAiAnalysis() {
    if (!currentProject) {
        showToast('Chọn project trước', 'error');
        return;
    }
    if (allRankings.length === 0) {
        showToast('Sync dữ liệu trước khi phân tích AI', 'error');
        return;
    }

    const btn = document.getElementById('aiBtn');
    btn.classList.add('loading');
    btn.disabled = true;

    try {
        const res = await fetch(`/api/ai/analyze/${encodeURIComponent(currentProject)}`, {
            method: 'POST',
        });
        const data = await res.json();

        if (data.error) {
            showToast(data.error, 'error');
            btn.classList.remove('loading');
            btn.disabled = false;
            return;
        }

        // Show progress panel
        document.getElementById('aiInsightsPanel').classList.remove('hidden');
        document.getElementById('aiProgress').style.display = 'flex';
        document.getElementById('aiTopics').innerHTML = '';
        document.getElementById('aiSuggestions').innerHTML = '';

        const statusEl = document.getElementById('aiStatus');
        statusEl.textContent = 'Đang phân tích...';
        statusEl.className = 'ai-status running';

        showToast(`Đang phân tích ${data.totalKeywords} keywords bằng AI...`, 'info');

        // Start polling progress
        startProgressPolling();
    } catch (err) {
        showToast('Lỗi kết nối AI: ' + err.message, 'error');
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}

function startProgressPolling() {
    if (aiPollInterval) clearInterval(aiPollInterval);

    aiPollInterval = setInterval(async () => {
        try {
            const res = await fetch(`/api/ai/progress/${encodeURIComponent(currentProject)}`);
            const prog = await res.json();

            if (prog.status === 'running') {
                const pct = prog.total > 0 ? Math.round(prog.processed / prog.total * 100) : 0;
                document.getElementById('aiProgressFill').style.width = pct + '%';
                document.getElementById('aiProgressText').textContent =
                    `Batch ${prog.batch}/${prog.totalBatches} (${prog.processed}/${prog.total} keywords)`;
            } else if (prog.status === 'done') {
                clearInterval(aiPollInterval);
                aiPollInterval = null;
                document.getElementById('aiProgress').style.display = 'none';
                document.getElementById('aiBtn').classList.remove('loading');
                document.getElementById('aiBtn').disabled = false;
                showToast(`AI phân tích xong via ${prog.provider || 'AI'}!`, 'success');
                loadAiInsights();
            } else if (prog.status === 'error') {
                clearInterval(aiPollInterval);
                aiPollInterval = null;
                document.getElementById('aiProgress').style.display = 'none';
                document.getElementById('aiBtn').classList.remove('loading');
                document.getElementById('aiBtn').disabled = false;
                showToast('AI lỗi: ' + (prog.error || 'Unknown'), 'error');
            }
        } catch (err) {
            console.error('Progress poll error:', err);
        }
    }, 2000);
}

function renderAiInsights(insights) {
    const statusEl = document.getElementById('aiStatus');
    statusEl.textContent = 'Cached';
    statusEl.className = 'ai-status cached';

    const dateEl = document.getElementById('aiAnalyzedAt');
    if (insights.analyzedAt) {
        const d = new Date(insights.analyzedAt);
        dateEl.textContent = `Phân tích lúc: ${d.toLocaleString('vi-VN')}`;
    }

    // Support both Gemini format (topics/suggestions) and Ollama format (topicClusters/quickWins/etc)
    const topics = insights.topics || [];
    const topicClusters = insights.topicClusters || [];
    const suggestions = insights.suggestions || [];
    const quickWins = insights.quickWins || [];
    const needsImprovement = insights.needsImprovement || [];
    const contentGaps = insights.contentGaps || [];
    const summary = insights.summary || '';

    const topicsEl = document.getElementById('aiTopics');
    const sugEl = document.getElementById('aiSuggestions');

    let html = '';

    // Summary
    if (summary) {
        html += `<div style="background:var(--card-bg,#fff);border-radius:10px;padding:16px;margin-bottom:16px;border-left:4px solid var(--green,#22c55e)">
            <strong>📊 Tổng quan:</strong> ${escapeHtml(summary)}
        </div>`;
    }

    // Gemini-style topics
    if (topics.length > 0) {
        html += `<div class="ai-topics-title">📊 Nhóm chủ đề (${topics.length})</div>`;
        topics.forEach((t, i) => {
            const kws = (t.keywords || []).slice(0, 15);
            html += `<div class="ai-topic-card" id="aitopic-${i}" onclick="toggleAiTopic(${i})">
                <div class="ai-topic-header">
                    <span class="ai-topic-name">${escapeHtml(t.name || 'Unnamed')}</span>
                    <div class="ai-topic-meta">
                        <span class="ai-priority ${t.priority || 'low'}">${t.priority || ''}</span>
                        <span class="ai-topic-kw-count">${(t.keywords || []).length} kw</span>
                        <span class="ai-topic-chevron">▶</span>
                    </div>
                </div>
                <div class="ai-topic-body">
                    ${t.suggestedTitle ? `<div class="ai-topic-title-suggestion">📝 ${escapeHtml(t.suggestedTitle)}</div>` : ''}
                    ${t.reason ? `<div class="ai-topic-reason">${escapeHtml(t.reason)}</div>` : ''}
                    <div class="ai-topic-keywords">${kws.map(k => `<span class="ai-kw-tag">${escapeHtml(k)}</span>`).join('')}</div>
                </div>
            </div>`;
        });
    }

    // Ollama-style topic clusters
    if (topicClusters.length > 0) {
        html += `<div style="font-weight:600;font-size:15px;margin:16px 0 8px">📊 Nhóm chủ đề (${topicClusters.length})</div>`;
        topicClusters.forEach((t, i) => {
            const kws = (t.keywords || []).slice(0, 10);
            html += `<div style="background:var(--card-bg,#fff);border-radius:10px;padding:14px;margin-bottom:10px;border-left:4px solid var(--blue,#3b82f6)">
                <strong>${escapeHtml(t.topic || '')}</strong>
                <div style="color:var(--text-dim);font-size:13px;margin:6px 0">${escapeHtml(t.strategy || '')}</div>
                <div style="display:flex;flex-wrap:wrap;gap:4px">${kws.map(k => `<span class="ai-kw-tag">${escapeHtml(k)}</span>`).join('')}</div>
            </div>`;
        });
    }

    topicsEl.innerHTML = html;

    // Suggestions section
    let sugHtml = '';

    // Gemini-style suggestions
    if (suggestions.length > 0) {
        const icons = { new_content: '✍️', optimize: '🔧', merge: '🔗', internal_link: '🔀' };
        sugHtml += `<div class="ai-suggestions-title">💡 Gợi ý hành động (${suggestions.length})</div>`;
        suggestions.forEach(s => {
            const icon = icons[s.type] || '💡';
            const kws = (s.keywords || []).slice(0, 5);
            sugHtml += `<div class="ai-suggestion-card">
                <div class="ai-suggestion-icon">${icon}</div>
                <div class="ai-suggestion-content">
                    <div class="ai-suggestion-title">${escapeHtml(s.title || '')} <span class="ai-priority ${s.priority || 'low'}">${s.priority || ''}</span></div>
                    <div class="ai-suggestion-desc">${escapeHtml(s.description || '')}</div>
                    ${kws.length > 0 ? `<div class="ai-suggestion-keywords">${kws.map(k => `<span class="ai-kw-tag">${escapeHtml(k)}</span>`).join('')}</div>` : ''}
                </div>
            </div>`;
        });
    }

    // Quick Wins (Ollama)
    if (quickWins.length > 0) {
        sugHtml += `<div style="font-weight:600;font-size:15px;margin:16px 0 8px">⚡ Quick Wins (${quickWins.length})</div>`;
        quickWins.forEach(q => {
            sugHtml += `<div style="background:var(--card-bg,#fff);border-radius:10px;padding:14px;margin-bottom:8px;border-left:4px solid var(--green,#22c55e)">
                <strong>${escapeHtml(q.keyword || '')}</strong>
                <div style="color:var(--text-dim);font-size:13px;margin-top:4px">${escapeHtml(q.action || '')}</div>
            </div>`;
        });
    }

    // Needs Improvement (Ollama)
    if (needsImprovement.length > 0) {
        sugHtml += `<div style="font-weight:600;font-size:15px;margin:16px 0 8px">🔧 Cần cải thiện (${needsImprovement.length})</div>`;
        needsImprovement.forEach(n => {
            sugHtml += `<div style="background:var(--card-bg,#fff);border-radius:10px;padding:14px;margin-bottom:8px;border-left:4px solid var(--yellow,#eab308)">
                <strong>${escapeHtml(n.keyword || '')}</strong>
                <div style="color:var(--text-dim);font-size:13px;margin-top:4px">${escapeHtml(n.suggestion || '')}</div>
            </div>`;
        });
    }

    // Content Gaps (Ollama)
    if (contentGaps.length > 0) {
        sugHtml += `<div style="font-weight:600;font-size:15px;margin:16px 0 8px">🔍 Content Gaps (${contentGaps.length})</div>`;
        sugHtml += `<div style="display:flex;flex-wrap:wrap;gap:6px">`;
        contentGaps.forEach(g => {
            sugHtml += `<span class="ai-kw-tag" style="background:var(--red,#ef4444);color:#fff">${escapeHtml(typeof g === 'string' ? g : g.topic || '')}</span>`;
        });
        sugHtml += `</div>`;
    }

    sugEl.innerHTML = sugHtml;
}

function toggleAiTopic(idx) {
    const card = document.getElementById(`aitopic-${idx}`);
    if (card) card.classList.toggle('expanded');
}

// ============ Periodic status checks ============

setInterval(checkWarpStatus, 15000);
