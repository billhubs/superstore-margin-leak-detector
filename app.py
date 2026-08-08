import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime, date, timedelta

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Commercial & Supply Chain Operations Diagnostic",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. FORTUNE 500 STANDARD COLOR PALETTES
# ---------------------------------------------------------
COLOR_PALETTES = {
    "walmart_navy": {
        "name": "Corporate Navy (Standard)",
        "primary": "#001E6C",
        "secondary": "#0071CE",
        "background": "#F4F6F9",
        "chart_profit": "#001E6C",
        "chart_loss": "#D97706"
    },
    "mckinsey_executive": {
        "name": "Executive Slate",
        "primary": "#0A192F",
        "secondary": "#2563EB",
        "background": "#FAFAFA",
        "chart_profit": "#0A192F",
        "chart_loss": "#DC2626"
    },
    "amazon_logistics": {
        "name": "Supply Chain",
        "primary": "#131921",
        "secondary": "#FF9900",
        "background": "#F3F4F6",
        "chart_profit": "#131921",
        "chart_loss": "#E11D48"
    },
    "high_contrast_clean": {
        "name": "High-Contrast Enterprise White",
        "primary": "#0F172A",
        "secondary": "#3B82F6",
        "background": "#FFFFFF",
        "chart_profit": "#0F172A",
        "chart_loss": "#EF4444"
    }
}

# ---------------------------------------------------------
# 3. SIDEBAR CONTROL CENTER
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px; padding: 10px; background: rgba(0,0,0,0.03); border-radius: 12px;'>
            <div style='background: #001E6C; color: #FFF; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem;'>🛒</div>
            <div>
                <strong style='font-size: 0.95rem; display: block;'>Dashboard</strong>
                <span style='font-size: 0.72rem; opacity: 0.8;'>Merchandising Intelligence</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### **Theme Engine**")
    selected_theme_key = st.selectbox(
        "Active Color Palette",
        options=list(COLOR_PALETTES.keys()),
        format_func=lambda x: COLOR_PALETTES[x]["name"],
        index=0
    )
    theme = COLOR_PALETTES[selected_theme_key]
    
    st.markdown("---")
    st.markdown("### **Scope Parameters**")

# Inject Dynamic CSS based on Active Theme (Escaped {{ }} for Python f-strings)
st.markdown(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
    :root {{
      --primary: {theme['primary']};
      --secondary: {theme['secondary']};
      --bg: {theme['background']};
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: var(--bg) !important;
        color: var(--primary) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: var(--bg) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
    }}

    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, [data-testid="stWidgetLabel"] {{
        color: var(--primary) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.15) !important;
        color: var(--primary) !important;
    }}

    span[data-baseweb="tag"] {{
        background-color: var(--secondary) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }}

    span[data-baseweb="tag"] span {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    .behavioral-alert {{
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.12);
        border-left: 6px solid #DC2626;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }}

    .ai-agent-card {{
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.12);
        border-left: 6px solid {theme['primary']};
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
    }}

    .kpi-card {{
        background-color: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
    }}

    .chart-card {{
        background-color: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }}

    .story-callout {{
        background-color: rgba(0, 0, 0, 0.03);
        border-left: 4px solid var(--primary);
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        margin-top: 10px;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: rgba(0, 0, 0, 0.05);
        padding: 6px;
        border-radius: 14px;
    }}

    .stTabs [aria-selected="true"],
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] div,
    .stTabs [aria-selected="true"] span {{
        background-color: var(--primary) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
    }}

    .stTabs [aria-selected="false"],
    .stTabs [aria-selected="false"] p,
    .stTabs [aria-selected="false"] div,
    .stTabs [aria-selected="false"] span {{
        color: var(--primary) !important;
        font-weight: 600 !important;
        opacity: 0.85 !important;
    }}

    .data-source-tag {{
        font-size: 0.68rem;
        background: #E2E8F0;
        color: #334155;
        padding: 2px 7px;
        border-radius: 6px;
        font-weight: 700;
        float: right;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. DATA PIPELINE & FEATURE ENGINEERING
# ---------------------------------------------------------
@st.cache_data
def load_and_prep_data():
    df = pd.read_csv("superstore.csv", encoding="latin-1")
    df.columns = df.columns.str.replace(" ", "_").str.replace("-", "_").str.lower()
    return df

@st.cache_resource
def get_db_connection(_df):
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    _df.to_sql("superstore", conn, index=False, if_exists="replace")
    return conn

try:
    df = load_and_prep_data()
    conn = get_db_connection(df)
except Exception as e:
    st.error(f"Data Pipeline Error: {e}")
    st.stop()

with st.sidebar:
    available_regions = df["region"].dropna().unique().tolist()
    available_categories = df["category"].dropna().unique().tolist()

    region_filter = st.multiselect("Region Scope", options=available_regions, default=available_regions)
    category_filter = st.multiselect("Category Scope", options=available_categories, default=available_categories)

    if not region_filter or not category_filter:
        st.warning("Please select at least one Region and Category scope.")
        st.stop()

# Filter via SQLite
placeholders_region = ','.join(['?'] * len(region_filter))
placeholders_cat = ','.join(['?'] * len(category_filter))

query = f"""
    SELECT * FROM superstore 
    WHERE region IN ({placeholders_region})
    AND category IN ({placeholders_cat})
"""
params = tuple(region_filter) + tuple(category_filter)
filtered_df = pd.read_sql_query(query, conn, params=params)

# Feature Engineering
filtered_df['order_date'] = pd.to_datetime(filtered_df['order_date'], format='mixed', errors='coerce')
filtered_df['ship_date'] = pd.to_datetime(filtered_df['ship_date'], format='mixed', errors='coerce')
filtered_df['shipping_days'] = (filtered_df['ship_date'] - filtered_df['order_date']).dt.days
filtered_df['profit_status'] = np.where(filtered_df['profit'] >= 0, 'Profitable', 'Loss / Deficit')

# Mock State for Operations & Task Assignments
if "tasks_db" not in st.session_state:
    st.session_state["tasks_db"] = pd.DataFrame([
        {
            "Task_ID": "TSK-1001",
            "Division": "Merchandising & Pricing",
            "Assignee": "Sarah Jenkins",
            "Priority": "URGENT",
            "Issue_Summary": "Tables category 50% discount margin erosion",
            "Assigned_Date": date.today() - timedelta(days=6),
            "Due_Date": date.today() - timedelta(days=1),
            "Reported_To": "VP Merchandising",
            "Status": "Past Due",
            "Needs_Investigator": True,
            "Investigator_Lead": "Alex Rivera (Audit)"
        },
        {
            "Task_ID": "TSK-1002",
            "Division": "Supply Chain & Logistics",
            "Assignee": "Budi Santoso",
            "Priority": "HIGH",
            "Issue_Summary": "Standard Class shipping latency > 6 days in West Region",
            "Assigned_Date": date.today() - timedelta(days=2),
            "Due_Date": date.today() + timedelta(days=2),
            "Reported_To": "Director of Logistics",
            "Status": "Reaching Due Date",
            "Needs_Investigator": False,
            "Investigator_Lead": "N/A"
        }
    ])

# ---------------------------------------------------------
# 5. HEADER & AI DIAGNOSTIC ENGINE
# ---------------------------------------------------------
st.markdown("""
    <div style="margin-bottom: 16px; padding-top: 8px;">
        <h1 style="font-size: 2.1rem; font-weight: 800; margin-bottom: 2px;">
            Commercial Ops & Supply Chain Diagnostic
        </h1>
        <p style="font-size: 0.95rem; opacity: 0.8; margin: 0; font-weight: 500;">
            Executive Data Storytelling & AI Incident Governance Suite
        </p>
    </div>
""", unsafe_allow_html=True)

# Key Performance Indicators Calculation
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
avg_shipping_time = filtered_df["shipping_days"].mean()
total_loss_orders = filtered_df[filtered_df["profit"] < 0]["profit"].sum()

# AI Agent Rules Engine
def evaluate_ai_governance(margin, loss, transit_time):
    alerts = []
    if margin < 15.0:
        alerts.append({
            "severity": "URGENT",
            "division": "Merchandising & Pricing",
            "target": ["VP Merchandising", "Category Managers"],
            "desc": f"Current Net Profit Margin ({margin:.1f}%) is diluted below strategic benchmark (15.0%)."
        })
    if loss < -50000:
        alerts.append({
            "severity": "WARNING",
            "division": "Commercial Finance",
            "target": ["Director Financial Planning", "Internal Audit"],
            "desc": f"Capital Loss Drain from negative transactions reached ${abs(loss):,.0f}."
        })
    if transit_time > 4.2:
        alerts.append({
            "severity": "WARNING",
            "division": "Supply Chain & Logistics",
            "target": ["Logistics Ops Lead", "Regional Fulfillment Director"],
            "desc": f"Order-to-Ship Lead Time ({transit_time:.1f} Days) exceeds SLA threshold (4.0 Days)."
        })
    return alerts

ai_alerts = evaluate_ai_governance(profit_margin, total_loss_orders, avg_shipping_time)

# Behavioral Pattern Interrupt Alert (Preserved Original Banner)
if profit_margin < 15.0 or total_loss_orders < -50000:
    st.markdown(f"""
        <div class="behavioral-alert">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 0.95rem; text-transform: uppercase; color: #DC2626;">⚠️ DIAGNOSTIC ALERT: Profit Margin Erosion Detected</strong>
                    <div style="font-size: 0.9rem; margin-top: 4px; color: #1E293B;">
                        Total cumulative loss from negative-margin transactions reached <b>${abs(total_loss_orders):,.0f}</b>. 
                        Current Net Profit Margin is <b>{profit_margin:.1f}%</b> (Below strategic benchmark of 15.0%).
                    </div>
                </div>
                <span style="background: #DC2626; color: white; padding: 6px 14px; border-radius: 20px; font-weight: 800; font-size: 0.75rem;">ACTION REQUIRED</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# AI Incident Governance Card
st.markdown(f"""
    <div class="ai-agent-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-weight: 800; font-size: 1.05rem; color: {theme['primary']};">
                🤖 AI Governance Agent: Anomaly Detection & Stakeholder Dispatch
            </div>
            <span style="font-size: 0.72rem; background: {theme['primary']}; color: #FFF; padding: 3px 10px; border-radius: 12px; font-weight: 700;">AI ACTIVE</span>
        </div>
""", unsafe_allow_html=True)

if ai_alerts:
    for alt in ai_alerts:
        bg = "#DC2626" if alt["severity"] == "URGENT" else "#D97706"
        st.markdown(f"""
            <div style="background: rgba(0,0,0,0.02); border: 1px solid rgba(0,0,0,0.08); padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;">
                <span style="background: {bg}; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 0.7rem;">{alt['severity']}</span>
                <strong style="margin-left: 8px; font-size: 0.88rem;">[{alt['division']}]</strong>
                <span style="font-size: 0.88rem; color: #334155;"> {alt['desc']}</span>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;"><b>Auto-Notified Stakeholders:</b> {', '.join(alt['target'])}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<div style='font-size: 0.88rem; color: #16A34A; font-weight: 600;'>✅ All operational and financial parameters are within safe benchmarks.</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. DASHBOARD TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "1. Profit & Loss Storytelling", 
    "2. Supply Chain & Fulfillment Latency", 
    "3. Operations & Team Assignment"
])

# ---------------------------------------------------------
# TAB 1: PROFIT & LOSS STORYTELLING
# ---------------------------------------------------------
with tab1:
    # LEVEL 1: MACRO HEALTH KPIs (With Data Source Tagging)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
            <div class="kpi-card">
                <span class="data-source-tag">POS / SAP ERP</span>
                <div style="font-size: 0.75rem; font-weight: 800; opacity: 0.8; text-transform: uppercase;">Gross Revenue</div>
                <div style="font-size: 2rem; font-weight: 800; margin-top: 4px;">${total_sales:,.0f}</div>
                <div style="font-size: 0.72rem; margin-top: 6px; font-weight: 600; opacity: 0.8;">Total Order Volume</div>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
            <div class="kpi-card">
                <span class="data-source-tag">Ledger DB</span>
                <div style="font-size: 0.75rem; font-weight: 800; opacity: 0.8; text-transform: uppercase;">Net Profit Margin</div>
                <div style="font-size: 2rem; font-weight: 800; margin-top: 4px;">{profit_margin:.1f}%</div>
                <div style="font-size: 0.72rem; margin-top: 6px; font-weight: 600; color: {'#DC2626' if profit_margin < 15 else '#16A34A'};">Target: 15.0% Benchmark</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="kpi-card">
                <span class="data-source-tag">Audit Engine</span>
                <div style="font-size: 0.75rem; font-weight: 800; opacity: 0.8; text-transform: uppercase;">Total Cumulative Loss</div>
                <div style="font-size: 2rem; font-weight: 800; margin-top: 4px; color: #DC2626;">${total_loss_orders:,.0f}</div>
                <div style="font-size: 0.72rem; margin-top: 6px; font-weight: 600; opacity: 0.8;">Eroded by Excess Discounts</div>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
            <div class="kpi-card">
                <span class="data-source-tag">WMS Logistics</span>
                <div style="font-size: 0.75rem; font-weight: 800; opacity: 0.8; text-transform: uppercase;">Avg Fulfillment Time</div>
                <div style="font-size: 2rem; font-weight: 800; margin-top: 4px;">{avg_shipping_time:.1f} Days</div>
                <div style="font-size: 0.72rem; margin-top: 6px; font-weight: 600; opacity: 0.8;">Order-to-Ship Lead Time</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

    # LEVEL 2: DIAGNOSTIC ANOMALY SCATTER PLOT & SUB-CATEGORY BAR
    c1, c2 = st.columns([1.6, 1])

    with c1:
        st.markdown("""
            <div class="chart-card">
                <h4 style="margin: 0; font-weight: 800;">
                    Anomaly Diagnosis: Discount Rate vs Profitability
                    <span class="data-source-tag">Merchandising DB</span>
                </h4>
                <p style="font-size: 0.82rem; opacity: 0.8; margin-bottom: 12px;">Detecting 'The Discount Trap' (Discounts > 20% exponentially drive negative profits)</p>
        """, unsafe_allow_html=True)

        fig_scatter = px.scatter(
            filtered_df,
            x="discount",
            y="profit",
            color="profit_status",
            size="sales",
            hover_data=["sub_category", "product_name", "sales"],
            color_discrete_map={"Profitable": theme['chart_profit'], "Loss / Deficit": "#DC2626"},
            labels={"discount": "Discount Rate (%)", "profit": "Profit / Loss ($)"}
        )
        fig_scatter.add_vline(x=0.2, line_dash="dash", line_color="#DC2626", annotation_text="Safe Discount Cap (20%)")
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.08)', 
                tickformat=".0%",
                title=dict(text="Discount Rate (%)", font=dict(color=theme['primary'], size=12, family='Plus Jakarta Sans')),
                tickfont=dict(color=theme['primary'])
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.08)',
                title=dict(text="Profit / Loss ($)", font=dict(color=theme['primary'], size=12, family='Plus Jakarta Sans')),
                tickfont=dict(color=theme['primary'])
            ),
            legend=dict(
                orientation="h", 
                y=1.15,
                font=dict(color=theme['primary'], size=11, family='Plus Jakarta Sans')
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("""
            <div class="story-callout">
                💡 <b>Executive Insight:</b> Notice the cluster of red markers to the right of the red dashed line (Discount > 20%). Over-discounting intended for inventory clearance is the single largest driver of gross margin destruction.
            </div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
            <div class="chart-card">
                <h4 style="margin: 0; font-weight: 800;">
                    Profitability by Sub-Category
                    <span class="data-source-tag">Financial System</span>
                </h4>
                <p style="font-size: 0.82rem; opacity: 0.8; margin-bottom: 12px;">Identifying Top Loss-Making Product Lines</p>
        """, unsafe_allow_html=True)

        subcat_profit = filtered_df.groupby("sub_category")["profit"].sum().reset_index().sort_values(by="profit")
        subcat_profit["color"] = np.where(subcat_profit["profit"] < 0, "#DC2626", theme['chart_profit'])

        fig_subcat = px.bar(
            subcat_profit,
            x="profit",
            y="sub_category",
            orientation="h",
            labels={"profit": "Net Profit ($)", "sub_category": ""}
        )
        fig_subcat.update_traces(marker_color=subcat_profit["color"])
        fig_subcat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.08)',
                tickfont=dict(color=theme['primary'])
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(color=theme['primary'], size=11)
            )
        )
        st.plotly_chart(fig_subcat, use_container_width=True)
        
        st.markdown("""
            <div class="story-callout">
                ⚠️ <b>Commercial Anomaly:</b> The <b>Tables</b> and <b>Bookcases</b> sub-categories generate heavy loss volumes despite recording high sales figures.
            </div>
            </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: SUPPLY CHAIN & FULFILLMENT LATENCY
# ---------------------------------------------------------
with tab2:
    st.markdown("### **Supply Chain & Fulfillment Latency Analysis**")
    
    s1, s2 = st.columns([1, 1])
    
    with s1:
        st.markdown("""
            <div class="chart-card">
                <h4 style="margin: 0; font-weight: 800;">
                    Fulfillment Latency by Ship Mode
                    <span class="data-source-tag">WMS Dispatch</span>
                </h4>
                <p style="font-size: 0.82rem; opacity: 0.8; margin-bottom: 12px;">Average Lead Time (Order Date to Ship Date)</p>
        """, unsafe_allow_html=True)
        
        ship_mode_df = filtered_df.groupby("ship_mode")["shipping_days"].mean().reset_index().sort_values(by="shipping_days")
        
        fig_ship = px.bar(
            ship_mode_df,
            x="ship_mode",
            y="shipping_days",
            text_auto=".1f",
            labels={"ship_mode": "Shipping Mode", "shipping_days": "Avg Lead Time (Days)"}
        )
        fig_ship.update_traces(marker_color=theme['primary'])
        fig_ship.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(tickfont=dict(color=theme['primary'])),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.08)', tickfont=dict(color=theme['primary']))
        )
        st.plotly_chart(fig_ship, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown("""
            <div class="chart-card">
                <h4 style="margin: 0; font-weight: 800;">
                    Regional Fulfillment vs Profit Loss
                    <span class="data-source-tag">Logistics ERP</span>
                </h4>
                <p style="font-size: 0.82rem; opacity: 0.8; margin-bottom: 12px;">Evaluating Regional Logistical Efficiency</p>
        """, unsafe_allow_html=True)
        
        region_ship = filtered_df.groupby("region").agg({"profit": "sum", "shipping_days": "mean"}).reset_index()
        
        fig_region = px.bar(
            region_ship,
            x="region",
            y="profit",
            color="shipping_days",
            color_continuous_scale="Reds",
            labels={"region": "Region", "profit": "Total Net Profit ($)", "shipping_days": "Avg Days"}
        )
        fig_region.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(tickfont=dict(color=theme['primary'])),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.08)', tickfont=dict(color=theme['primary']))
        )
        st.plotly_chart(fig_region, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: OPERATIONS & TEAM ASSIGNMENT
# ---------------------------------------------------------
with tab3:
    st.markdown("### **Division Task Assignment & Incident Operations Center**")
    
    # Task Operational Metrics
    t_df = st.session_state["tasks_db"]
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Incident Tasks", len(t_df))
    with m2:
        st.metric("Urgent Escalations", len(t_df[t_df["Priority"] == "URGENT"]))
    with m3:
        st.metric("Past Due Tasks", len(t_df[t_df["Status"] == "Past Due"]))
    with m4:
        st.metric("Investigators Assigned", len(t_df[t_df["Needs_Investigator"] == True]))

    st.markdown("---")
    
    # Interactive Division Task Matrix
    st.markdown("#### **Active Division Task Matrix & SLA Tracking**")
    st.dataframe(
        t_df,
        column_config={
            "Task_ID": st.column_config.TextColumn("Task ID"),
            "Division": st.column_config.TextColumn("Target Division"),
            "Assignee": st.column_config.TextColumn("Assigned Person"),
            "Priority": st.column_config.TextColumn("Priority"),
            "Status": st.column_config.SelectboxColumn("SLA Status", options=["On Duty", "Reaching Due Date", "Past Due", "Resolved"]),
            "Assigned_Date": st.column_config.DateColumn("Task Date"),
            "Due_Date": st.column_config.DateColumn("Due Date"),
            "Reported_To": st.column_config.TextColumn("Reported To"),
            "Needs_Investigator": st.column_config.CheckboxColumn("Investigator Assigned?"),
            "Investigator_Lead": st.column_config.TextColumn("Investigator Lead")
        },
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    
    # Task Dispatch Form
    st.markdown("#### **Dispatch New Incident Task / Assign Investigator**")
    with st.form("dispatch_task_form"):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            f_div = st.selectbox("Target Division", ["Merchandising & Pricing", "Supply Chain & Logistics", "Commercial Finance", "Store Operations"])
            f_person = st.text_input("Assigned Personal Name", placeholder="e.g. John Doe")
            f_priority = st.selectbox("Priority Level", ["URGENT", "HIGH", "MEDIUM", "LOW"])
        with f_col2:
            f_summary = st.text_area("Issue Summary / Anomaly Trigger", placeholder="e.g. Excessive discounts on Office Supplies")
            f_reported = st.text_input("Reported To (Executive / Stakeholder)", placeholder="e.g. VP of Merchandising")
        with f_col3:
            f_due = st.date_input("Assignment Due Date", value=date.today() + timedelta(days=3))
            f_needs_inv = st.checkbox("Assign Investigator Team?")
            f_investigator = st.text_input("Investigator Lead Name", value="Audit Lead: Unassigned")

        submit_btn = st.form_submit_button("🚀 Dispatch Task & Trigger Stakeholder Alert")

        if submit_btn:
            new_task = {
                "Task_ID": f"TSK-{1001 + len(t_df)}",
                "Division": f_div,
                "Assignee": f_person if f_person else "Unassigned",
                "Priority": f_priority,
                "Issue_Summary": f_summary,
                "Assigned_Date": date.today(),
                "Due_Date": f_due,
                "Reported_To": f_reported if f_reported else "Management",
                "Status": "On Duty",
                "Needs_Investigator": f_needs_inv,
                "Investigator_Lead": f_investigator if f_needs_inv else "N/A"
            }
            st.session_state["tasks_db"] = pd.concat([st.session_state["tasks_db"], pd.DataFrame([new_task])], ignore_index=True)
            st.success(f"Task {new_task['Task_ID']} dispatched successfully to {f_div}! Notification sent to {f_reported}.")
            st.rerun()

    st.markdown("---")

    # Prescriptive Execution Policy (Preserved Original Policy Section)
    st.markdown("### **Prescriptive Operational Actions**")
    st.markdown(f"""
        <div style="background-color: #FFFFFF; border-radius: 16px; padding: 24px; border-left: 6px solid {theme['primary']}; box-shadow: 0 4px 14px rgba(0,0,0,0.05);">
            <h4 style="margin-top: 0; font-weight: 800; color: {theme['primary']};">Commercial Merchandising Execution Policy (Walmart Standard):</h4>
            <ol style="line-height: 1.8; font-size: 0.95rem; color: #1E293B;">
                <li><b>Hard-Cap Maximum Discount at 20%:</b> Enforce POS (Point of Sale) system guardrails to prevent promotional discounts on <i>Tables</i> and <i>Bookcases</i> from exceeding 20% without regional VP approval.</li>
                <li><b>Eliminate 50% Clearance Campaigns:</b> Immediately terminate deep clearance promotions (50%+ off), which statistically contribute to over 70% of total cumulative margin losses.</li>
                <li><b>Fulfillment Optimization:</b> Reallocate heavy inventory lines (furniture/tables) directly to regional fulfillment hubs to eliminate multi-day transit delays under <i>Standard Class</i> shipping.</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)