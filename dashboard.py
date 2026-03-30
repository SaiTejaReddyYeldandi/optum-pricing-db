import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc

st.set_page_config(page_title="Optum Pricing Dashboard", layout="wide")

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PricingDB;"
    "Trusted_Connection=yes;"
)

@st.cache_data
def run_query(sql):
    conn = pyodbc.connect(CONN_STR)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

st.title("Optum Pharmacy Pricing Dashboard")
st.markdown("PULSE / Repricing Assistant — Analytics View")

# KPI row
col1, col2, col3, col4 = st.columns(4)
total_txns  = run_query("SELECT COUNT(*) AS n FROM Transactions").iloc[0,0]
total_rev   = run_query("SELECT SUM(Quantity*UnitPrice) AS n FROM Transactions").iloc[0,0]
total_prods = run_query("SELECT COUNT(*) AS n FROM Products").iloc[0,0]
total_custs = run_query("SELECT COUNT(*) AS n FROM Customers").iloc[0,0]

col1.metric("Total Transactions", f"{total_txns:,}")
col2.metric("Total Revenue", f"${total_rev:,.0f}")
col3.metric("Products", total_prods)
col4.metric("Customers", total_custs)

st.divider()

# Revenue by category
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    df = run_query("""
        SELECT p.Category, SUM(t.Quantity * t.UnitPrice) AS Revenue
        FROM Transactions t JOIN Products p ON t.ProductID = p.ProductID
        GROUP BY p.Category ORDER BY Revenue DESC
    """)
    fig = px.bar(df, x="Category", y="Revenue", color="Category")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Spend by Customer Tier")
    df = run_query("""
        SELECT c.Tier, SUM(t.Quantity * t.UnitPrice) AS TotalSpend
        FROM Transactions t JOIN Customers c ON t.CustomerID = c.CustomerID
        GROUP BY c.Tier
    """)
    fig = px.pie(df, names="Tier", values="TotalSpend")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Repricing Simulator
st.subheader("Repricing Simulator")
st.markdown("Select a product and customer to calculate negotiated price")

products = run_query("SELECT ProductID, ProductName, BasePrice FROM Products ORDER BY ProductName")
customers = run_query("SELECT CustomerID, CustomerName, Tier FROM Customers ORDER BY CustomerName")

col1, col2, col3 = st.columns(3)
with col1:
    product = st.selectbox("Product", products["ProductName"].tolist())
with col2:
    customer = st.selectbox("Customer", customers["CustomerName"].tolist())
with col3:
    discount_pct = st.slider("Discount %", 0, 40, 10)

base_price = products[products["ProductName"] == product]["BasePrice"].values[0]
new_price = round(base_price * (1 - discount_pct / 100), 2)

st.metric("Base Price", f"${base_price}")
st.metric("Negotiated Price", f"${new_price}", delta=f"-{discount_pct}%")

st.divider()

# Top transactions
st.subheader("Recent Transactions")
df = run_query("""
    SELECT TOP 20
        p.ProductName, c.CustomerName, c.Tier,
        t.Quantity, t.UnitPrice,
        t.Quantity * t.UnitPrice AS TotalValue,
        CONVERT(VARCHAR, t.TxnDate, 23) AS TxnDate
    FROM Transactions t
    JOIN Products p ON t.ProductID = p.ProductID
    JOIN Customers c ON t.CustomerID = c.CustomerID
    ORDER BY t.TxnDate DESC
""")
st.dataframe(df, use_container_width=True)