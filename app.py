import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Advanced Sales KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Advanced Sales KPI Dashboard")
st.markdown("Interactive KPI Analysis with Multiple Filters")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

product_filter = st.sidebar.multiselect(
    "Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Order_Date"].min(), df["Order_Date"].max())
)

min_sales = st.sidebar.slider(
    "Minimum Sales",
    int(df["Sales"].min()),
    int(df["Sales"].max()),
    int(df["Sales"].min())
)

# Apply Filters
filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Product"].isin(product_filter)) &
    (df["Sales"] >= min_sales)
]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Order_Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["Order_Date"] <= pd.to_datetime(end_date))
    ]

# KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = filtered_df["Order_ID"].nunique()
avg_profit = filtered_df["Profit"].mean()

# KPI Cards
st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Orders", total_orders)
col4.metric("Quantity Sold", total_quantity)
col5.metric("Avg Profit", f"₹{avg_profit:,.0f}")

st.divider()

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    sales_by_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales_by_category,
        x="Category",
        y="Sales",
        title="Sales by Category",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    profit_by_category = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        profit_by_category,
        values="Profit",
        names="Category",
        title="Profit Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# Charts Row 2
col3, col4 = st.columns(2)

with col3:
    sales_trend = (
        filtered_df.groupby("Order_Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        sales_trend,
        x="Order_Date",
        y="Sales",
        markers=True,
        title="Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:
    top_products = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_products,
        x="Product",
        y="Sales",
        title="Top 10 Products"
    )

    st.plotly_chart(fig, use_container_width=True)

# Scatter Plot
st.subheader("Profit vs Sales")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_name="Product"
)

st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Sales Dataset")

st.dataframe(filtered_df, use_container_width=True)

# Download Button
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_sales_data.csv",
    "text/csv"
)

# Footer
st.markdown("---")
st.markdown("Developed with Streamlit & Plotly")