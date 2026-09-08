"""
GSC Dashboard — Google Search Console + AI Chatbot
Chạy: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import json
import os

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="GSC Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS — Premium Dark Theme
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* KPI Card styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1A1D23 0%, #252830 100%);
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetric"] label {
        color: #A0A4B0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #FAFAFA !important;
    }
    
    /* Tab styling */
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12141A 0%, #1A1D23 100%);
        border-right: 1px solid rgba(108, 92, 231, 0.15);
    }
    
    /* Divider */
    hr { border-color: rgba(108, 92, 231, 0.2) !important; }
    
    /* Chat */
    div[data-testid="stChatMessage"] {
        background: #1A1D23 !important;
        border: 1px solid rgba(108, 92, 231, 0.15);
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# GSC AUTH & DATA FETCHING
# ============================================================

def get_gsc_service():
    """Khởi tạo GSC API service bằng OAuth."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    
    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
    token_path = os.path.join(os.path.dirname(__file__), ".gsc_token.json")
    
    creds = None
    
    # Load existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If no valid token, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            client_id = st.secrets.get("gsc", {}).get("client_id", "")
            client_secret = st.secrets.get("gsc", {}).get("client_secret", "")
            
            if not client_id or not client_secret:
                return None
            
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"],
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for next time
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    
    return build("searchconsole", "v1", credentials=creds)


@st.cache_data(ttl=3600, show_spinner="Đang tải dữ liệu GSC...")
def fetch_gsc_data(
    property_url: str,
    start_date: str,
    end_date: str,
    dimensions: list[str],
    row_limit: int = 5000,
) -> pd.DataFrame:
    """Lấy dữ liệu Search Analytics từ GSC API."""
    service = get_gsc_service()
    if not service:
        return pd.DataFrame()
    
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": row_limit,
        "dataState": "final",
    }
    
    response = (
        service.searchanalytics()
        .query(siteUrl=property_url, body=body)
        .execute()
    )
    
    rows = response.get("rows", [])
    if not rows:
        return pd.DataFrame()
    
    data = []
    for row in rows:
        entry = {
            dim: row["keys"][i] for i, dim in enumerate(dimensions)
        }
        entry["clicks"] = row.get("clicks", 0)
        entry["impressions"] = row.get("impressions", 0)
        entry["ctr"] = row.get("ctr", 0)
        entry["position"] = row.get("position", 0)
        data.append(entry)
    
    df = pd.DataFrame(data)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(ttl=86400, show_spinner="Đang tải danh sách property...")
def list_gsc_properties() -> list[str]:
    """Lấy danh sách các property trong GSC."""
    service = get_gsc_service()
    if not service:
        return []
    response = service.sites().list().execute()
    return [s["siteUrl"] for s in response.get("siteEntry", [])]


# ============================================================
# DEMO DATA (khi chưa kết nối GSC)
# ============================================================

def generate_demo_data() -> pd.DataFrame:
    """Tạo dữ liệu demo để xem trước dashboard."""
    import random
    random.seed(42)
    
    dates = pd.date_range(end=date.today() - timedelta(days=3), periods=30, freq="D")
    queries = [
        "các loại bảo hiểm hiện nay", "bảo hiểm nhân thọ là gì",
        "bảo hiểm sức khỏe nên mua gì", "so sánh bảo hiểm", 
        "bảo hiểm phi nhân thọ", "mua bảo hiểm online",
        "bảo hiểm xã hội 2026", "bảo hiểm du lịch",
        "bảo hiểm ô tô bắt buộc", "bảo hiểm y tế",
        "home credit bảo hiểm", "vay tiền home credit",
        "thẻ tín dụng home credit", "trả góp home credit",
        "lãi suất home credit 2026",
    ]
    pages = [
        "/bao-hiem/cac-loai-bao-hiem-hien-nay",
        "/bao-hiem/bao-hiem-nhan-tho",
        "/bao-hiem/bao-hiem-suc-khoe",
        "/tai-chinh/vay-tien-online",
        "/tai-chinh/the-tin-dung",
    ]
    
    data = []
    for d in dates:
        for q in random.sample(queries, k=random.randint(8, 15)):
            clicks = random.randint(0, 120)
            impressions = clicks * random.randint(8, 40) + random.randint(10, 200)
            data.append({
                "date": d,
                "query": q,
                "page": random.choice(pages),
                "clicks": clicks,
                "impressions": impressions,
                "ctr": clicks / max(impressions, 1),
                "position": round(random.uniform(1.5, 45.0), 1),
            })
    
    return pd.DataFrame(data)


# ============================================================
# AI ASSISTANT
# ============================================================

def build_ai_context(df: pd.DataFrame) -> dict:
    """Create a compact, aggregate-only context for the AI assistant."""
    numeric = [column for column in ("clicks", "impressions", "ctr", "position") if column in df]
    context = {
        "row_count": len(df),
        "columns": list(df.columns),
        "totals": {column: float(df[column].sum()) for column in numeric if column != "position"},
    }
    if "date" in df and not df.empty:
        context["date_range"] = [str(df["date"].min()), str(df["date"].max())]
    aggregations = {column: "sum" for column in ("clicks", "impressions") if column in df}
    if "position" in df:
        aggregations["position"] = "mean"
    for dimension in ("query", "page"):
        if dimension in df and aggregations:
            grouped = df.groupby(dimension, as_index=False).agg(aggregations)
            sort_column = "clicks" if "clicks" in grouped else next(iter(aggregations))
            context[f"top_{dimension}s"] = (
                grouped.sort_values(sort_column, ascending=False).head(20).round(4).to_dict("records")
            )
    return context

def render_ai_chat(df: pd.DataFrame):
    """Render AI chatbot interface."""
    st.subheader("💬 Hỏi AI về dữ liệu GSC")
    st.caption("VD: _Từ khóa nào có CTR cao nhất?_ · _Top 5 trang có nhiều clicks nhất?_")
    
    api_key = st.secrets.get("openai", {}).get("api_key", "")
    
    if not api_key:
        st.info(
            "💡 Để dùng AI chatbot, thêm OpenAI API key vào "
            "`.streamlit/secrets.toml`:\n\n"
            '```\n[openai]\napi_key = "sk-..."\n```'
        )
        return
    
    try:
        from openai import OpenAI
    except ImportError:
        st.warning("Chưa cài OpenAI SDK. Chạy: `pip install -r requirements.txt`")
        return

    client = OpenAI(api_key=api_key)
    model = st.secrets.get("openai", {}).get("model", "gpt-5.6-luna")
    data_context = build_ai_context(df)
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Hỏi về dữ liệu GSC..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Đang phân tích..."):
                try:
                    recent_history = st.session_state.messages[-6:-1]
                    response = client.responses.create(
                        model=model,
                        instructions=(
                            "Bạn là chuyên gia SEO phân tích Google Search Console. "
                            "Chỉ trả lời từ dữ liệu tổng hợp được cung cấp; nêu rõ khi dữ liệu không đủ. "
                            "Không suy đoán số liệu và trả lời bằng tiếng Việt, ngắn gọn, có hành động đề xuất."
                        ),
                        input=json.dumps(
                            {
                                "question": prompt,
                                "recent_conversation": recent_history,
                                "gsc_summary": data_context,
                            },
                            ensure_ascii=False,
                            default=str,
                        ),
                    )
                    answer = response.output_text
                    st.write(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as e:
                    st.error(f"Lỗi: {e}")


# ============================================================
# MAIN APP
# ============================================================

def main():
    # ---- SIDEBAR ----
    with st.sidebar:
        st.markdown("## 🔍 GSC Dashboard")
        st.caption("Personal SEO Monitor")
        st.divider()
        
        # Data source selection
        data_source = st.radio(
            "📡 Nguồn dữ liệu",
            ["Demo Data", "Google Search Console"],
            index=0,
            help="Chọn 'Demo Data' để xem trước. Kết nối GSC khi đã cấu hình OAuth."
        )
        
        st.divider()
        
        # Date range
        default_end = date.today() - timedelta(days=3)  # GSC có delay 2-3 ngày
        default_start = default_end - timedelta(days=29)
        
        col_s, col_e = st.columns(2)
        with col_s:
            start_date = st.date_input("Từ ngày", value=default_start)
        with col_e:
            end_date = st.date_input("Đến ngày", value=default_end)
        
        st.divider()
        
        # GSC property selection
        selected_property = None
        if data_source == "Google Search Console":
            properties = list_gsc_properties()
            if properties:
                selected_property = st.selectbox("🌐 Property", properties)
            else:
                st.warning("Chưa kết nối được GSC. Kiểm tra `secrets.toml`.")
                data_source = "Demo Data"
        
        st.divider()
        st.caption("Built with Streamlit + Plotly")
    
    # ---- LOAD DATA ----
    if data_source == "Demo Data":
        df = generate_demo_data()
        df = df[(df["date"] >= pd.Timestamp(start_date)) & (df["date"] <= pd.Timestamp(end_date))]
        st.toast("📊 Đang dùng dữ liệu demo", icon="ℹ️")
    else:
        df = fetch_gsc_data(
            property_url=selected_property,
            start_date=str(start_date),
            end_date=str(end_date),
            dimensions=["date", "query", "page"],
            row_limit=5000,
        )
        if df.empty:
            st.warning("Không có dữ liệu cho khoảng thời gian này.")
            return
    
    # ---- HEADER ----
    st.markdown("# 🔍 GSC Dashboard")
    if data_source == "Demo Data":
        st.caption("⚡ Demo Mode — Dữ liệu giả lập để xem trước giao diện")
    else:
        st.caption(f"📡 Live data từ **{selected_property}**")
    
    st.divider()
    
    # ---- KPI CARDS ----
    total_clicks = int(df["clicks"].sum())
    total_impressions = int(df["impressions"].sum())
    avg_ctr = total_clicks / max(total_impressions, 1)
    avg_position = round(df["position"].mean(), 1)
    unique_queries = df["query"].nunique() if "query" in df.columns else 0
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🖱️ Clicks", f"{total_clicks:,}")
    c2.metric("👁️ Impressions", f"{total_impressions:,}")
    c3.metric("📈 CTR", f"{avg_ctr:.2%}")
    c4.metric("📍 Avg Position", f"{avg_position}")
    c5.metric("🔑 Keywords", f"{unique_queries:,}")
    
    st.divider()
    
    # ---- TABS ----
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Xu hướng", "🔑 Từ khóa", "📄 Trang", "💬 Hỏi AI"
    ])
    
    # ---- TAB 1: TRENDS ----
    with tab1:
        if "date" in df.columns:
            daily = df.groupby("date").agg(
                clicks=("clicks", "sum"),
                impressions=("impressions", "sum"),
            ).reset_index()
            daily["ctr"] = daily["clicks"] / daily["impressions"].replace(0, 1)
            
            col_left, col_right = st.columns(2)
            
            with col_left:
                fig_clicks = px.area(
                    daily, x="date", y="clicks",
                    title="Clicks theo ngày",
                    color_discrete_sequence=["#6C5CE7"],
                )
                fig_clicks.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FAFAFA",
                    xaxis_title="", yaxis_title="",
                )
                fig_clicks.update_traces(
                    fill="tozeroy",
                    fillcolor="rgba(108, 92, 231, 0.15)",
                    line=dict(width=2.5),
                )
                st.plotly_chart(fig_clicks, use_container_width=True)
            
            with col_right:
                fig_imp = px.area(
                    daily, x="date", y="impressions",
                    title="Impressions theo ngày",
                    color_discrete_sequence=["#00CEC9"],
                )
                fig_imp.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FAFAFA",
                    xaxis_title="", yaxis_title="",
                )
                fig_imp.update_traces(
                    fill="tozeroy",
                    fillcolor="rgba(0, 206, 201, 0.15)",
                    line=dict(width=2.5),
                )
                st.plotly_chart(fig_imp, use_container_width=True)
            
            # CTR & Position trend
            col_l2, col_r2 = st.columns(2)
            with col_l2:
                fig_ctr = px.line(
                    daily, x="date", y="ctr",
                    title="CTR theo ngày",
                    color_discrete_sequence=["#FDCB6E"],
                )
                fig_ctr.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FAFAFA",
                    xaxis_title="", yaxis_title="",
                    yaxis_tickformat=".1%",
                )
                fig_ctr.update_traces(line=dict(width=2.5))
                st.plotly_chart(fig_ctr, use_container_width=True)
            
            with col_r2:
                if "position" in df.columns:
                    daily_pos = df.groupby("date")["position"].mean().reset_index()
                    fig_pos = px.line(
                        daily_pos, x="date", y="position",
                        title="Avg Position theo ngày (thấp = tốt)",
                        color_discrete_sequence=["#E17055"],
                    )
                    fig_pos.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font_color="#FAFAFA",
                        xaxis_title="", yaxis_title="",
                        yaxis_autorange="reversed",
                    )
                    fig_pos.update_traces(line=dict(width=2.5))
                    st.plotly_chart(fig_pos, use_container_width=True)
    
    # ---- TAB 2: KEYWORDS ----
    with tab2:
        if "query" in df.columns:
            kw = df.groupby("query").agg(
                clicks=("clicks", "sum"),
                impressions=("impressions", "sum"),
                position=("position", "mean"),
            ).reset_index()
            kw["ctr"] = kw["clicks"] / kw["impressions"].replace(0, 1)
            kw["position"] = kw["position"].round(1)
            
            sort_col = st.selectbox(
                "Sắp xếp theo", ["clicks", "impressions", "ctr", "position"],
                index=0, key="kw_sort"
            )
            ascending = sort_col == "position"
            kw_sorted = kw.sort_values(sort_col, ascending=ascending).head(50)
            
            # Styled table
            st.dataframe(
                kw_sorted.style.format({
                    "clicks": "{:,.0f}",
                    "impressions": "{:,.0f}",
                    "ctr": "{:.2%}",
                    "position": "{:.1f}",
                }).background_gradient(
                    subset=["clicks"], cmap="Purples"
                ).background_gradient(
                    subset=["ctr"], cmap="YlGn"
                ),
                use_container_width=True,
                height=600,
            )
            
            # Scatter: Position vs Clicks (tìm cơ hội)
            st.subheader("🎯 Ma trận cơ hội — Position vs Clicks")
            st.caption("Từ khóa ở góc trên-trái = CƠ HỘI LỚN (vị trí thấp nhưng clicks cao)")
            fig_scatter = px.scatter(
                kw, x="position", y="clicks", size="impressions",
                hover_name="query",
                color="ctr",
                color_continuous_scale="Viridis",
                title="",
            )
            fig_scatter.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#FAFAFA",
                xaxis_title="Position (thấp = tốt)",
                yaxis_title="Clicks",
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    # ---- TAB 3: PAGES ----
    with tab3:
        if "page" in df.columns:
            pages = df.groupby("page").agg(
                clicks=("clicks", "sum"),
                impressions=("impressions", "sum"),
                position=("position", "mean"),
                keywords=("query", "nunique"),
            ).reset_index()
            pages["ctr"] = pages["clicks"] / pages["impressions"].replace(0, 1)
            pages["position"] = pages["position"].round(1)
            pages = pages.sort_values("clicks", ascending=False)
            
            st.dataframe(
                pages.style.format({
                    "clicks": "{:,.0f}",
                    "impressions": "{:,.0f}",
                    "ctr": "{:.2%}",
                    "position": "{:.1f}",
                    "keywords": "{:,.0f}",
                }).background_gradient(
                    subset=["clicks"], cmap="Purples"
                ),
                use_container_width=True,
                height=500,
            )
            
            # Bar chart top pages
            fig_pages = px.bar(
                pages.head(15), x="clicks", y="page",
                orientation="h",
                title="Top 15 trang theo Clicks",
                color="ctr",
                color_continuous_scale="Viridis",
            )
            fig_pages.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#FAFAFA",
                yaxis=dict(autorange="reversed"),
                xaxis_title="Clicks", yaxis_title="",
                height=500,
            )
            st.plotly_chart(fig_pages, use_container_width=True)
    
    # ---- TAB 4: AI CHAT ----
    with tab4:
        render_ai_chat(df)


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    main()
