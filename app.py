import streamlit as st
import pandas as pd
import plotly.express as px

# Setting halaman wide
st.set_page_config(page_title="Superstore Margin Monitor", layout="wide")

# Styling CSS untuk memperbesar KPI Card & memberikan efek visual
st.markdown("""
    <style>
    .kpi-card-danger {
        background-color: #FFEFEB;
        border-left: 5px solid #FF4B4B;
        padding: 15px;
        border-radius: 5px;
    }
    .kpi-card-success {
        background-color: #E8F5E9;
        border-left: 5px solid #2E7D32;
        padding: 15px;
        border-radius: 5px;
    }
    .kpi-title { font-size: 14px; color: #555555; margin-bottom: 5px; }
    .kpi-value { font-size: 28px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA & CLEANING ---
@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding="windows-1252")
    df.columns = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
    
    # Parsing tanggal eksplisit M/D/YYYY
    df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce')
    df['ship_date'] = pd.to_datetime(df['ship_date'], format='%m/%d/%Y', errors='coerce')
    df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days
    return df

df = load_data()

st.title("🚨 Superstore Operational & Margin Leakage Monitor")
st.caption("Dashboard kontrol cepat untuk memantau kebocoran profit dan efisiensi pengiriman.")

# --- SECTION 1: TOP KPI CARDS ---
total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
net_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

# Total kerugian dari transaksi bernilai negatif
loss_df = df[df['profit'] < 0]
total_loss = loss_df['profit'].sum()
avg_ship_days = df['shipping_days'].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
        <div class="kpi-card-success">
            <div class="kpi-title">TOTAL NET PROFIT</div>
            <div class="kpi-value" style="color: #2E7D32;">${total_profit:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    margin_color = "#2E7D32" if net_margin >= 5 else ("#FFA000" if net_margin >= 2 else "#FF4B4B")
    st.markdown(f"""
        <div class="kpi-card-success" style="border-left-color: {margin_color};">
            <div class="kpi-title">NET MARGIN (%)</div>
            <div class="kpi-value" style="color: {margin_color};">{net_margin:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="kpi-card-danger">
            <div class="kpi-title">TOTAL BLEEDING LOSSES</div>
            <div class="kpi-value" style="color: #FF4B4B;">${abs(total_loss):,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class="kpi-card-success" style="border-left-color: #6C757D;">
            <div class="kpi-title">AVG SHIPPING DAYS</div>
            <div class="kpi-value" style="color: #333333;">{avg_ship_days:.1f} Days</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- SECTION 2: VISUAL LEAK DETECTOR ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚠️ Discount vs. Profit Leakage")
    st.caption("Titik MERAH adalah transaksi rugi. Perhatikan lonjakan kerugian di atas diskon 20%.")
    
    # Menambahkan kategori status profit untuk pemetaan warna eksplisit
    df['profit_status'] = df['profit'].apply(lambda x: 'Loss' if x < 0 else 'Profit')
    
    fig_scatter = px.scatter(
        df, 
        x="discount", 
        y="profit", 
        color="profit_status",
        color_discrete_map={'Loss': '#FF4B4B', 'Profit': '#00C853'},
        hover_data=["sub_category", "sales"],
        opacity=0.7
    )
    # Garis ambang batas bahaya diskon
    fig_scatter.add_vline(x=0.2, line_dash="dash", line_color="#D32F2F", annotation_text="Danger Zone (>20%)")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_right:
    st.subheader("📊 Profitability by Sub-Category")
    st.caption("Kategori dengan batang MERAH menyumbang kerugian terbesar.")
    
    sub_summary = df.groupby('sub_category')['profit'].sum().reset_index().sort_values('profit')
    sub_summary['color'] = sub_summary['profit'].apply(lambda x: '#FF4B4B' if x < 0 else '#2E7D32')
    
    fig_bar = px.bar(
        sub_summary, 
        x='profit', 
        y='sub_category', 
        orientation='h',
        color='profit',
        color_continuous_scale=['#FF4B4B', '#E0E0E0', '#2E7D32']
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- SECTION 3: AUDIT TABLE FOR LOSSES ---
st.subheader("📋 Top Unprofitable Orders (Immediate Action Required)")
st.caption("Daftar transaksi yang menghasilkan margin negatif untuk dievaluasi oleh tim operasional.")

loss_orders = df[df['profit'] < 0][['order_id', 'order_date', 'category', 'sub_category', 'sales', 'discount', 'profit', 'shipping_days']].sort_values(by='profit', ascending=True)

st.dataframe(
    loss_orders.style.format({
        'sales': '${:,.2f}',
        'profit': '${:,.2f}',
        'discount': '{:.0%}'
    }), 
    use_container_width=True
)
