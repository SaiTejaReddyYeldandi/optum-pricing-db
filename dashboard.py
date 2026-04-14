import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px

# --- DB Connection ---
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PricingDB;"
    "Trusted_Connection=yes;"
)

@st.cache_data
def get_data(query):
    conn = pyodbc.connect(CONN_STR)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="Healthcare Pricing Dashboard", layout="wide")
st.title("Healthcare Pricing Dashboard")
st.caption("Pharmacy Pricing & Repricing System — Optum PULSE Ecosystem")

# --- KPIs ---
total_txns = get_data("SELECT COUNT(*) AS cnt FROM Transactions").iloc[0]['cnt']
total_revenue = get_data("SELECT SUM(Quantity * UnitPrice) AS rev FROM Transactions").iloc[0]['rev']
total_products = get_data("SELECT COUNT(*) AS cnt FROM Products").iloc[0]['cnt']
total_customers = get_data("SELECT COUNT(*) AS cnt FROM Customers").iloc[0]['cnt']

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{total_txns:,}")
col2.metric("Total Revenue", f"${total_revenue:,.0f}")
col3.metric("Total Products", f"{total_products:,}")
col4.metric("Total Customers", f"{total_customers:,}")

st.divider()

# --- Charts ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by Category")
    rev_data = get_data("""
        SELECT p.Category, SUM(t.Quantity * t.UnitPrice) AS TotalRevenue
        FROM Transactions t JOIN Products p ON t.ProductID = p.ProductID
        GROUP BY p.Category ORDER BY TotalRevenue DESC
    """)
    fig1 = px.bar(rev_data, x='Category', y='TotalRevenue',
                  color='Category', title="Revenue by Drug Category")
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Spend by Customer Tier")
    tier_data = get_data("""
        SELECT c.Tier, SUM(t.Quantity * t.UnitPrice) AS TotalSpend
        FROM Transactions t JOIN Customers c ON t.CustomerID = c.CustomerID
        GROUP BY c.Tier
    """)
    fig2 = px.pie(tier_data, names='Tier', values='TotalSpend',
                  title="Spend Distribution by Tier")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Repricing Simulator ---
st.subheader("Repricing Simulator")
st.write("Select a product and customer to simulate negotiated pricing.")

products = get_data("SELECT ProductID, ProductName, BasePrice FROM Products ORDER BY ProductName")
customers = get_data("SELECT CustomerID, CustomerName, Tier FROM Customers ORDER BY CustomerName")

col_a, col_b, col_c = st.columns(3)

with col_a:
    selected_product = st.selectbox("Select Product",
        options=products['ProductName'].tolist())

with col_b:
    selected_customer = st.selectbox("Select Customer",
        options=customers['CustomerName'].tolist())

with col_c:
    discount_pct = st.slider("Discount %", min_value=0, max_value=50, value=10)

base_price = products[products['ProductName'] == selected_product]['BasePrice'].values[0]
negotiated_price = round(base_price * (1 - discount_pct / 100), 2)
savings = round(base_price - negotiated_price, 2)

r1, r2, r3 = st.columns(3)
r1.metric("Base Price", f"${base_price}")
r2.metric("Negotiated Price", f"${negotiated_price}", delta=f"-${savings}")
r3.metric("Discount Savings", f"${savings}")

st.divider()

# --- Recent Transactions ---
st.subheader("Recent Transactions")
recent = get_data("""
    SELECT TOP 20
        p.ProductName, c.CustomerName, c.Tier,
        t.Quantity, t.UnitPrice,
        t.Quantity * t.UnitPrice AS TotalValue,
        t.TxnDate
    FROM Transactions t
    JOIN Products p ON t.ProductID = p.ProductID
    JOIN Customers c ON t.CustomerID = c.CustomerID
    ORDER BY t.TxnID DESC
""")
st.dataframe(recent, use_container_width=True)