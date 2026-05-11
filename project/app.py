# Nassau Candy Distributor — Profitability & Margin Analytics Dashboard


# 📌 Full Streamlit Application Code (app.py)

# =========================================================
# NASSAU CANDY DISTRIBUTOR DASHBOARD
# =========================================================

# =========================
# IMPORT LIBRARIES
# =========================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go   

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Nassau Candy Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }

    .stMetric {
        background-color: blue;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }

    h1 {
        color: #1f4e79;
    }

    h2 {
        color: #1f4e79;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================

@st.cache_data

def load_data():
    df = pd.read_csv("processed_nassau_candy_analysis.csv")

    df['Order Date'] = pd.to_datetime(df['Order Date'])

    return df


df = load_data()

# =========================
# SIDEBAR
# =========================

st.sidebar.title("📌 Dashboard Filters")

# Date Filter

start_date = st.sidebar.date_input(
    "Start Date",
    df['Order Date'].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df['Order Date'].max()
)

# Division Filter

division_filter = st.sidebar.multiselect(
    "Select Division",
    options=df['Division'].unique(),
    default=df['Division'].unique()
)

# Margin Slider

margin_threshold = st.sidebar.slider(
    "Margin Threshold (%)",
    min_value=0,
    max_value=100,
    value=10
)

# Product Search

product_search = st.sidebar.text_input(
    "Search Product"
)

# =========================
# FILTER DATA
# =========================

filtered_df = df[
    (df['Order Date'] >= pd.to_datetime(start_date)) &
    (df['Order Date'] <= pd.to_datetime(end_date)) &
    (df['Division'].isin(division_filter))
]

if product_search:
    filtered_df = filtered_df[
        filtered_df['Product Name']
        .str.contains(product_search, case=False)
    ]

# =========================
# HEADER
# =========================

st.title("📊 Nassau Candy Distributor Analytics Dashboard")

st.markdown(
    """
    Advanced profitability and margin intelligence dashboard
    for business performance optimization.
    """
)

# =========================
# KPI SECTION
# =========================

st.subheader("📌 Business KPI Overview")
# st.write(filtered_df['Sales'].sum())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"${filtered_df['Sales'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${filtered_df['Gross Profit'].sum():,.0f}"
    )

with col3:
    avg_margin = filtered_df['Gross Margin %'].mean()

    st.metric(
        "Average Margin",
        f"{avg_margin:.2f}%"
    )

with col4:
    st.metric(
        "Units Sold",
        f"{filtered_df['Units'].sum():,.0f}"
    )

# =========================================================
# MODULE 1 — PRODUCT PROFITABILITY DASHBOARD
# =========================================================

st.markdown("---")

st.header("📊 Module 1 — Product Profitability Dashboard")

# Top Products

top_products = (
    filtered_df.groupby('Product Name')['Gross Profit']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

bottom_products = (
    filtered_df.groupby('Product Name')['Gross Profit']
    .sum()
    .sort_values(ascending=True)
    .head(10)
    .reset_index()
)

margin_leaderboard = (
    filtered_df.groupby('Product Name')['Gross Margin %']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        top_products,
        x='Gross Profit',
        y='Product Name',
        orientation='h',
        title='Top 10 Profitable Products'
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.bar(
        bottom_products,
        x='Gross Profit',
        y='Product Name',
        orientation='h',
        title='Bottom 10 Products'
    )

    st.plotly_chart(fig, use_container_width=True)

# Margin Leaderboard

fig = px.bar(
    margin_leaderboard,
    x='Gross Margin %',
    y='Product Name',
    orientation='h',
    title='Top Margin Products'
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# MODULE 2 — DIVISION DASHBOARD
# =========================================================

st.markdown("---")

st.header("📊 Module 2 — Division Performance Dashboard")

division_df = (
    filtered_df.groupby('Division')
    .agg({
        'Sales':'sum',
        'Gross Profit':'sum',
        'Gross Margin %':'mean'
    })
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        division_df,
        x='Division',
        y=['Sales', 'Gross Profit'],
        barmode='group',
        title='Revenue vs Profit Comparison'
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        division_df,
        names='Division',
        values='Gross Profit',
        title='Division Profit Contribution'
    )

    st.plotly_chart(fig, use_container_width=True)

# Margin Comparison

fig = px.box(
    filtered_df,
    x='Division',
    y='Gross Margin %',
    title='Division Margin Distribution'
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# MODULE 3 — COST DIAGNOSTICS
# =========================================================

st.markdown("---")

st.header("📊 Module 3 — Cost Diagnostics")

# Scatter Plot

fig = px.scatter(
    filtered_df,
    x='Cost',
    y='Sales',
    color='Division',
    size='Gross Profit',
    hover_data=['Product Name'],
    title='Cost vs Sales Analysis'
)

st.plotly_chart(fig, use_container_width=True)

# Margin Risk Detection

risk_df = filtered_df[
    filtered_df['Gross Margin %'] < margin_threshold
]

st.subheader("⚠️ Margin Risk Products")

st.dataframe(
    risk_df[
        [
            'Product Name',
            'Division',
            'Sales',
            'Gross Profit',
            'Gross Margin %'
        ]
    ].sort_values(by='Gross Margin %')
)

# Cost Heavy Products

st.subheader("💰 Cost Heavy Products")

cost_heavy = (
    
    filtered_df.groupby(
        ['Product Name', 'Division']
    )
    
    .agg({
        'Cost':'sum',
        'Sales':'sum',
        'Gross Profit':'sum'
    })
    
    .reset_index()
    
    .sort_values(
        by='Cost',
        ascending=False
    )
    
    .head(10)
)

st.dataframe(cost_heavy)

# =========================================================
# MODULE 4 — PARETO DASHBOARD
# =========================================================

st.markdown("---")

st.header("📊 Module 4 — Pareto & Dependency Analysis")

pareto_df = (
    filtered_df.groupby('Product Name')['Gross Profit']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

pareto_df['Cumulative Profit'] = (
    pareto_df['Gross Profit'].cumsum()
)

pareto_df['Cumulative %'] = (
    pareto_df['Cumulative Profit']
    /
    pareto_df['Gross Profit'].sum()
) * 100

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=pareto_df.index,
        y=pareto_df['Cumulative %'],
        mode='lines+markers',
        name='Cumulative Profit %'
    )
)

fig.add_hline(
    y=80,
    line_dash='dash',
    line_color='red'
)

fig.update_layout(
    title='Pareto Analysis — Profit Contribution',
    xaxis_title='Products',
    yaxis_title='Cumulative Profit %'
)

st.plotly_chart(fig, use_container_width=True)

# Dependency Risk

st.subheader("📌 Dependency Risk Analysis")

num_products_80 = (
    pareto_df[pareto_df['Cumulative %'] <= 80]
    .shape[0]
)

st.info(
    f"Top {num_products_80} products contribute nearly 80% of total profit."
)

# =========================================================
# EXTRA INDUSTRY LEVEL FEATURES
# =========================================================

st.markdown("---")

st.header("📈 Advanced Business Intelligence")

# Monthly Revenue Trend

filtered_df['Month'] = (
    pd.to_datetime(filtered_df['Order Date'])
    .dt.to_period('M')
    .astype(str)
)

monthly_sales = (
    filtered_df.groupby('Month')['Sales']
    .sum()
    .reset_index()
)

fig = px.line(
    monthly_sales,
    x='Month',
    y='Sales',
    title='Monthly Revenue Trend'
)

st.plotly_chart(fig, use_container_width=True)

# Regional Performance

if 'Region' in filtered_df.columns:

    regional_sales = (
        filtered_df.groupby('Region')['Sales']
        .sum()
        .reset_index()
    )

    fig = px.bar(
        regional_sales,
        x='Region',
        y='Sales',
        title='Regional Revenue Performance'
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# BUSINESS RECOMMENDATIONS
# =========================================================

st.markdown("---")

st.header("📌 Strategic Recommendations")

st.success(
    """
    ✔ Reprice low-margin high-sales products.

    ✔ Reduce manufacturing cost for cost-heavy products.

    ✔ Promote high-margin premium products.

    ✔ Review low-performing products for discontinuation.

    ✔ Diversify profit dependency across more products.
    """
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")



