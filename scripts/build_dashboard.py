import json

# Load classified keywords data
with open('matcha_keywords_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Flatten list for the "All" tab and general tables
all_keywords = []
no = 1
for gname, items in data['groups'].items():
    for item in items:
        all_keywords.append({
            'no': no,
            'group': gname,
            'keyword': item['keyword'],
            'sv': item['sv'],
            'comp': item['comp'],
            'priority': item['priority'],
            'action': item['action']
        })
        no += 1

# Calculate statistics
total_keywords = len(all_keywords)
total_sv = sum(item['sv'] for item in all_keywords)
b2b_count = len(data['groups']['Bột matcha giá sỉ / B2B'])
buy_count = len(data['groups']['Mua bột matcha ở đâu'])
pure_count = len(data['groups']['Bột matcha nguyên chất'])
faq_count = len(data['groups']['Bột matcha - Câu hỏi'])
fb_count = len(data['groups']['Pha chế & Ứng dụng F&B'])
other_count = len(data['groups']['Bột matcha khác'])

highest_sv_item = max(all_keywords, key=lambda x: x['sv']) if all_keywords else {'keyword': 'N/A', 'sv': 0}

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phân Nhóm & Lọc Từ Khóa Matcha - WIN Flavor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #090d16;
            --bg-secondary: #111827;
            --bg-card: #1f2937;
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f9fafb;
            --text-secondary: #9ca3af;
            --text-muted: #6b7280;
            
            --primary: #10b981; /* Emerald/Green for Matcha theme */
            --primary-glow: rgba(16, 185, 129, 0.15);
            --secondary: #3b82f6;
            --accent: #8b5cf6;
            
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-full: 9999px;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
            --shadow-glow: 0 0 25px rgba(16, 185, 129, 0.2);
            
            --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        [data-theme="light"] {{
            --bg-primary: #f3f4f6;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --border-color: #e5e7eb;
            --text-primary: #111827;
            --text-secondary: #4b5563;
            --text-muted: #9ca3af;
            --primary: #059669;
            --primary-glow: rgba(5, 150, 105, 0.1);
            --shadow-glow: 0 4px 20px rgba(5, 150, 105, 0.08);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            transition: var(--transition);
            line-height: 1.5;
            padding-bottom: 50px;
        }}

        .container {{
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 24px;
        }}

        /* Header Layout */
        header {{
            background: linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(9, 13, 22, 0.95) 100%);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 16px 0;
            transition: var(--transition);
        }}
        
        [data-theme="light"] header {{
            background: rgba(255, 255, 255, 0.9);
        }}

        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-area h1 {{
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(to right, #10b981, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .logo-area p {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 18px;
            font-size: 0.875rem;
            font-weight: 600;
            border-radius: var(--radius-md);
            border: 1px solid transparent;
            cursor: pointer;
            transition: var(--transition);
            text-decoration: none;
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--primary) 0%, #059669 100%);
            color: #ffffff;
            box-shadow: var(--shadow-glow);
        }}

        .btn-primary:hover {{
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
        }}

        .btn-secondary {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }}

        .btn-secondary:hover {{
            background-color: rgba(255, 255, 255, 0.05);
            border-color: var(--text-secondary);
        }}
        
        [data-theme="light"] .btn-secondary:hover {{
            background-color: #f3f4f6;
        }}

        .btn-icon {{
            width: 40px;
            height: 40px;
            padding: 0;
            border-radius: var(--radius-md);
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: var(--transition);
        }}

        .btn-icon:hover {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        
        [data-theme="light"] .btn-icon:hover {{
            background-color: #f3f4f6;
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 32px;
            margin-bottom: 24px;
        }}

        .stat-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 20px;
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary);
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--primary);
            opacity: 0.7;
        }}

        .stat-card.blue::before {{ background: var(--secondary); }}
        .stat-card.accent::before {{ background: var(--accent); }}

        .stat-title {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }}

        .stat-value {{
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--text-primary);
            line-height: 1.2;
        }}

        .stat-desc {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 8px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        /* Dashboard Main Layout */
        .dashboard-body {{
            margin-top: 10px;
        }}

        .controls-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .search-wrapper {{
            position: relative;
            flex-grow: 1;
            max-width: 400px;
            width: 100%;
        }}

        .search-input {{
            width: 100%;
            padding: 12px 16px 12px 42px;
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-size: 0.9rem;
            font-family: inherit;
            transition: var(--transition);
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }}

        .search-icon {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }}

        /* Tabs Styles */
        .tabs-list {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border-color);
        }}

        .tab-btn {{
            padding: 10px 20px;
            background-color: transparent;
            border: none;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.9rem;
            border-radius: var(--radius-md);
            cursor: pointer;
            white-space: nowrap;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .tab-btn:hover {{
            background-color: rgba(255, 255, 255, 0.03);
            color: var(--text-primary);
        }}
        
        [data-theme="light"] .tab-btn:hover {{
            background-color: rgba(0, 0, 0, 0.03);
        }}

        .tab-btn.active {{
            background-color: var(--primary-glow);
            color: var(--primary);
            box-shadow: inset 0 0 0 1px rgba(16, 185, 129, 0.2);
        }}

        .badge-count {{
            font-size: 0.75rem;
            padding: 2px 6px;
            border-radius: var(--radius-full);
            background-color: rgba(255, 255, 255, 0.08);
            color: var(--text-secondary);
        }}

        .tab-btn.active .badge-count {{
            background-color: var(--primary);
            color: white;
        }}

        /* Table Card & Styles */
        .table-card {{
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }}

        .table-responsive {{
            overflow-x: auto;
            max-height: 600px;
            position: relative;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }}

        th {{
            background-color: rgba(17, 24, 39, 0.8);
            position: sticky;
            top: 0;
            z-index: 10;
            font-weight: 700;
            color: var(--text-primary);
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            backdrop-filter: blur(8px);
        }}

        [data-theme="light"] th {{
            background-color: #f3f4f6;
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
            font-weight: 500;
            transition: var(--transition);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background-color: rgba(255, 255, 255, 0.015);
        }}
        
        [data-theme="light"] tr:hover td {{
            background-color: rgba(0, 0, 0, 0.01);
        }}

        .col-no {{ width: 70px; text-align: center; color: var(--text-muted); }}
        .col-group {{ width: 220px; font-weight: 600; color: var(--text-secondary); }}
        .col-kw {{ font-weight: 600; color: var(--text-primary); font-size: 0.95rem; }}
        .col-sv {{ width: 140px; font-weight: 700; text-align: right; font-family: monospace; }}
        .col-comp {{ width: 130px; text-align: center; }}
        .col-pri {{ width: 110px; text-align: center; }}
        .col-act {{ width: 160px; text-align: center; }}

        /* Status Badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 4px 10px;
            font-size: 0.75rem;
            font-weight: 700;
            border-radius: var(--radius-full);
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }}

        .badge-danger {{
            background-color: rgba(239, 68, 68, 0.12);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }}

        .badge-warning {{
            background-color: rgba(245, 158, 11, 0.12);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.2);
        }}

        .badge-success {{
            background-color: rgba(16, 185, 129, 0.12);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}

        .badge-purple {{
            background-color: rgba(139, 92, 246, 0.12);
            color: #a78bfa;
            border: 1px solid rgba(139, 92, 246, 0.2);
        }}

        .badge-blue {{
            background-color: rgba(59, 130, 246, 0.12);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }}

        /* Table Footer Stats */
        .table-footer {{
            padding: 16px 24px;
            background-color: rgba(17, 24, 39, 0.4);
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        [data-theme="light"] .table-footer {{
            background-color: #f9fafb;
        }}

        .empty-state {{
            padding: 48px;
            text-align: center;
            color: var(--text-muted);
            display: none;
        }}

        .empty-state svg {{
            margin-bottom: 12px;
            color: var(--text-muted);
            opacity: 0.5;
        }}

        /* Alerts info */
        .alert-info-box {{
            background-color: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.15);
            border-radius: var(--radius-md);
            padding: 14px 18px;
            margin-bottom: 24px;
            font-size: 0.875rem;
            color: #60a5fa;
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }}

        .alert-info-box strong {{
            color: var(--text-primary);
        }}
    </style>
</head>
<body>

    <header>
        <div class="container header-content">
            <div class="logo-area">
                <h1>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--primary)"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                    WIN Flavor Keyword Hub
                </h1>
                <p>Phân nhóm & Bộ lọc từ khóa Matcha phục vụ chiến dịch SEO B2B F&B</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-secondary" onclick="exportToCSV()" title="Tải file CSV chất lượng cao">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                    Tải CSV (.csv)
                </button>
                <button class="btn btn-primary" onclick="exportToExcel()" title="Tải file Excel tương thích MS Excel">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                    Xuất file Excel (.xls)
                </button>
                <button class="btn-icon" onclick="toggleTheme()" id="theme-toggle-btn" title="Chuyển chế độ sáng/tối">
                    <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" id="theme-icon"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
                </button>
            </div>
        </div>
    </header>

    <main class="container dashboard-body">
        
        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Tổng từ khóa đã lọc</div>
                <div class="stat-value">{total_keywords}</div>
                <div class="stat-desc">Đã lọc trùng & loại bỏ Cozy, Nhật, Đài Loan...</div>
            </div>
            <div class="stat-card blue">
                <div class="stat-title">Tổng Volume tìm kiếm</div>
                <div class="stat-value">{total_sv:,}</div>
                <div class="stat-desc">Lượt tìm kiếm tích lũy hàng tháng</div>
            </div>
            <div class="stat-card accent">
                <div class="stat-title">Từ khóa B2B & Mua hàng</div>
                <div class="stat-value">{b2b_count + buy_count}</div>
                <div class="stat-desc">Có giá trị chuyển đổi thương mại cao</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Keyword Volume Cao Nhất</div>
                <div class="stat-value" style="font-size: 1.1rem; font-weight: 700; margin-top: 10px; color: var(--primary);">{highest_sv_item['keyword']}</div>
                <div class="stat-desc">Volume: {highest_sv_item['sv']:,} / tháng</div>
            </div>
        </div>

        <div class="alert-info-box">
            <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="flex-shrink:0"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <div>
                <strong>Quy tắc lọc và làm sạch từ khóa:</strong> Bộ từ khóa đã loại trừ triệt để các thương hiệu bán lẻ cạnh tranh (*Cozy, Phúc Long, Gongcha,...) và các nước xuất xứ như *Nhật Bản, Đài Loan, Hàn Quốc* để tối ưu hóa nguồn lực SEO cho <strong>WIN Flavor</strong> (Nhà cung cấp hương liệu và nguyên liệu F&B B2B). Đã bổ sung các từ khóa ngách về *Hương liệu Matcha (Matcha Flavor)* cực kỳ sát sườn với hoạt động kinh doanh của doanh nghiệp.
            </div>
        </div>

        <!-- Search & Tab controls -->
        <div class="controls-row">
            <div class="search-wrapper">
                <svg class="search-icon" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                <input type="text" class="search-input" id="search-box" placeholder="Tìm kiếm từ khóa..." oninput="handleSearch()">
            </div>
        </div>

        <!-- Tabs -->
        <div class="tabs-list" id="tabs-container">
            <button class="tab-btn active" onclick="switchTab('All')">
                Tất cả từ khóa <span class="badge-count">{total_keywords}</span>
            </button>
            <button class="tab-btn" onclick="switchTab('Bột matcha giá sỉ / B2B')">
                Sỉ & B2B <span class="badge-count">{b2b_count}</span>
            </button>
            <button class="tab-btn" onclick="switchTab('Mua bột matcha ở đâu')">
                Địa điểm mua / Giá <span class="badge-count">{buy_count}</span>
            </button>
            <button class="tab-btn" onclick="switchTab('Bột matcha nguyên chất')">
                Nguyên chất & Uji <span class="badge-count">{pure_count}</span>
            </button>
            <button class="tab-btn" onclick="switchTab('Pha chế & Ứng dụng F&B')">
                Pha chế & F&B <span class="badge-count">{fb_count}</span>
            </button>
            <button class="tab-btn" onclick="switchTab('Bột matcha - Câu hỏi')">
                Câu hỏi / Sức khỏe <span class="badge-count">{faq_count}</span>
            </button>
            <button class="tab-btn" onclick="switchTab('Bột matcha khác')">
                Phụ trợ / Khác <span class="badge-count">{other_count}</span>
            </button>
        </div>

        <!-- Table Card -->
        <div class="table-card">
            <div class="table-responsive">
                <table id="main-keyword-table">
                    <thead>
                        <tr>
                            <th class="col-no">No.</th>
                            <th class="col-group">Nhóm chủ đề</th>
                            <th class="col-kw">Từ khóa (Keyword)</th>
                            <th class="col-sv" style="text-align: right">Search volume</th>
                            <th class="col-comp" style="text-align: center">Cạnh tranh</th>
                            <th class="col-pri" style="text-align: center">Ưu tiên</th>
                            <th class="col-act" style="text-align: center">Mục tiêu nhóm</th>
                        </tr>
                    </thead>
                    <tbody id="table-body">
                        <!-- Rendered by JS -->
                    </tbody>
                </table>
                <div class="empty-state" id="empty-state">
                    <svg width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    <p>Không tìm thấy từ khóa nào phù hợp với tìm kiếm.</p>
                </div>
            </div>
            <div class="table-footer">
                <div id="footer-count">Đang hiển thị {total_keywords} từ khóa</div>
                <div>WIN Flavor B2B SEO Strategy © 2026</div>
            </div>
        </div>

    </main>

    <script>
        // Data embedded directly
        const rawKeywords = {json.dumps(all_keywords, ensure_ascii=False)};
        
        let currentTab = 'All';
        let searchQuery = '';

        function renderTable() {{
            const tbody = document.getElementById('table-body');
            const emptyState = document.getElementById('empty-state');
            const footerCount = document.getElementById('footer-count');
            
            tbody.innerHTML = '';
            
            // Filter data
            let filtered = rawKeywords;
            if (currentTab !== 'All') {{
                filtered = filtered.filter(item => item.group === currentTab);
            }}
            
            if (searchQuery.trim() !== '') {{
                const q = searchQuery.toLowerCase();
                filtered = filtered.filter(item => 
                    item.keyword.toLowerCase().includes(q) || 
                    item.group.toLowerCase().includes(q)
                );
            }}
            
            if (filtered.length === 0) {{
                emptyState.style.display = 'block';
                document.getElementById('main-keyword-table').querySelector('thead').style.display = 'none';
                footerCount.innerText = 'Đang hiển thị 0 từ khóa';
                return;
            }}
            
            emptyState.style.display = 'none';
            document.getElementById('main-keyword-table').querySelector('thead').style.display = '';
            
            filtered.forEach((item, idx) => {{
                const tr = document.createElement('tr');
                
                // Cạnh tranh badge
                let compBadge = '';
                if (item.comp === 'Cao') {{
                    compBadge = '<span class="badge badge-danger">Cao</span>';
                }} else if (item.comp === 'Trung bình') {{
                    compBadge = '<span class="badge badge-warning">T.Bình</span>';
                }} else {{
                    compBadge = '<span class="badge badge-success">Thấp</span>';
                }}
                
                // Action badge
                let actBadge = '';
                if (item.action === 'Tăng hạng top 10') {{
                    actBadge = '<span class="badge badge-purple">Tăng hạng top 10</span>';
                }} else {{
                    actBadge = '<span class="badge badge-blue">Duy trì top 10</span>';
                }}
                
                tr.innerHTML = `
                    <td class="col-no">${{idx + 1}}</td>
                    <td class="col-group">${{item.group}}</td>
                    <td class="col-kw">${{item.keyword}}</td>
                    <td class="col-sv" style="text-align: right">${{item.sv ? item.sv.toLocaleString() : ''}}</td>
                    <td class="col-comp" style="text-align: center">${{compBadge}}</td>
                    <td class="col-pri" style="text-align: center"><span class="badge" style="background-color:rgba(255,255,255,0.05);color:var(--text-primary)">${{item.priority}}</span></td>
                    <td class="col-act" style="text-align: center">${{actBadge}}</td>
                `;
                tbody.appendChild(tr);
            }});
            
            footerCount.innerText = `Đang hiển thị ${{filtered.length}} từ khóa`;
        }}

        function switchTab(tabName) {{
            currentTab = tabName;
            
            // Update active button styling
            const tabs = document.getElementById('tabs-container').querySelectorAll('.tab-btn');
            tabs.forEach(btn => {{
                if (btn.innerText.includes(tabName) || (tabName === 'All' && btn.innerText.includes('Tất cả'))) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
            
            renderTable();
        }}

        function handleSearch() {{
            searchQuery = document.getElementById('search-box').value;
            renderTable();
        }}

        function toggleTheme() {{
            const currentTheme = document.body.getAttribute('data-theme');
            const themeBtn = document.getElementById('theme-toggle-btn');
            const themeIcon = document.getElementById('theme-icon');
            
            if (currentTheme === 'light') {{
                document.body.removeAttribute('data-theme');
                themeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>';
            }} else {{
                document.body.setAttribute('data-theme', 'light');
                themeIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z"/>';
            }}
        }}

        function exportToCSV() {{
            let csvContent = "No.,Nhóm,Keyword,Search volume,Cạnh tranh,Ưu tiên,Nhóm\\n";
            
            rawKeywords.forEach((item, idx) => {{
                let svStr = item.sv ? item.sv : "";
                csvContent += `${{idx + 1}},"${{item.group}}","${{item.keyword}}",${{svStr}},"${{item.comp}}","${{item.priority}}","${{item.action}}"\\n`;
            }});
            
            let blob = new Blob(['\\uFEFF' + csvContent], {{
                type: 'text/csv;charset=utf-8;'
            }});
            let url = URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'matcha_keywords_classified.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }}

        function exportToExcel() {{
            // Build simple HTML table representing the data
            let htmlTable = `<table>
                <thead>
                    <tr>
                        <th style="background-color:#059669;color:#ffffff;font-weight:bold;border:1px solid #d1d5db;">No.</th>
                        <th style="background-color:#059669;color:#ffffff;font-weight:bold;border:1px solid #d1d5db;">Nhóm</th>
                        <th style="background-color:#059669;color:#ffffff;font-weight:bold;border:1px solid #d1d5db;">Keyword</th>
                        <th style="background-color:#059669;color:#ffffff;font-weight:bold;border:1px solid #d1d5db;">Search volume</th>
                        <th style="background-color:#059669;color:#ffffff;font-weight:bold;border:1px solid #d1d5db;">Cạnh tranh</th>
                        <th style="background-color:#059669;color:#ffffff;font-weight:bold;border:1px solid #d1d5db;">Ưu tiên</th>
                        <th style="background-color:#059669;color:#ffffff;font-weight:bold;border:1px solid #d1d5db;">Nhóm</th>
                    </tr>
                </thead>
                <tbody>`;
                
            rawKeywords.forEach((item, idx) => {{
                let svStr = item.sv ? item.sv : "";
                htmlTable += `<tr>
                    <td style="border:1px solid #e5e7eb;text-align:center;">${{idx + 1}}</td>
                    <td style="border:1px solid #e5e7eb;">${{item.group}}</td>
                    <td style="border:1px solid #e5e7eb;font-weight:bold;">${{item.keyword}}</td>
                    <td style="border:1px solid #e5e7eb;text-align:right;">${{svStr}}</td>
                    <td style="border:1px solid #e5e7eb;text-align:center;">${{item.comp}}</td>
                    <td style="border:1px solid #e5e7eb;text-align:center;">${{item.priority}}</td>
                    <td style="border:1px solid #e5e7eb;text-align:center;">${{item.action}}</td>
                </tr>`;
            }});
            
            htmlTable += "</tbody></table>";
            
            let template = `
            <html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40">
            <head>
                <!--[if gte mso 9]>
                <xml>
                    <x:ExcelWorkbook>
                        <x:ExcelWorksheets>
                            <x:ExcelWorksheet>
                                <x:Name>Matcha Keywords</x:Name>
                                <x:WorksheetOptions>
                                    <x:DisplayGridlines/>
                                </x:WorksheetOptions>
                            </x:ExcelWorksheet>
                        </x:ExcelWorksheets>
                    </x:ExcelWorkbook>
                </xml>
                <![endif]-->
                <meta charset="utf-8">
                <style>
                    table {{ border-collapse: collapse; }}
                    td, th {{ border: 1px solid #d1d5db; padding: 8px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
                </style>
            </head>
            <body>
                ${{htmlTable}}
            </body>
            </html>`;

            let blob = new Blob(['\\uFEFF' + template], {{
                type: 'application/vnd.ms-excel;charset=utf-8'
            }});
            let url = URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'matcha_keywords_classified.xls';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }}

        // Initial render
        renderTable();
    </script>
</body>
</html>
"""

# Write to file
output_file = 'matcha_keywords_dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated dashboard page: {output_file}")
