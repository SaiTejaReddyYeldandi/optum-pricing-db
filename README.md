# optum-pricing-db

> Pharmacy pricing SQL Server DB — Optum PULSE/Repricing system

Built as part of a 30-day interview prep bootcamp targeting the **Optum Data Analyst role (Dublin)**. This project directly mirrors the PULSE/Repricing Assistant ecosystem described in the Optum JD — stored procedures, ETL pipelines, 100k+ row datasets, and a live Streamlit dashboard with a Repricing Simulator.

**Live dashboard:** `python -m streamlit run dashboard.py` → localhost:8501

---

## What This Project Does

A production-grade SQL Server database modelling a pharmacy pricing and repricing system with:

- 6 tables covering the full bid lifecycle
- 5 stored procedures for pricing operations
- 12 indexes including a covering index
- 3 analytical views
- Audit trigger on every price change
- Python ETL pipeline loading 100,000+ rows with validation and logging
- Streamlit dashboard with live KPIs, charts, and Repricing Simulator

---

## Project Structure

```
optum-pricing-db/
├── PricingDB_Complete.sql   # Full DB — schema, data, procedures, views, trigger
├── etl.py                   # Python ETL pipeline (Faker + pyodbc + pandas)
├── etl.log                  # ETL run log — 100k rows in 7 seconds
├── dashboard.py             # Streamlit dashboard — live pricing analytics
├── SQLQuery1_OPTUM.sql      # Original dev query file
└── README.md                # This file
```

---

## Database Schema

| Table | Rows | Description |
|---|---|---|
| Products | 524 | Pharmacy drugs with base prices |
| Customers | 224 | Insurance companies with tier + region |
| Pricing | 24 | Negotiated prices per customer/product |
| Transactions | 100,030 | All pricing transactions |
| Bids | 24 | Bid history with won/lost status |
| PriceAuditLog | 1+ | Auto-logged on every price change via trigger |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Database | SQL Server 2025 Developer Edition |
| SQL Client | SSMS 22 |
| ETL | Python 3.13 — pandas, pyodbc, faker |
| Dashboard | Streamlit, Plotly |
| Version Control | Git, GitHub |

---

## Dashboard

**KPIs:** 100,030 transactions · $7.5B revenue · 524 products · 224 customers

**Charts:**
- Revenue by Category (bar chart)
- Spend by Customer Tier (pie chart)
- Repricing Simulator — select product + customer + discount % → live negotiated price
- Recent Transactions table (live from SQL Server)

**Run:**
```bash
python -m streamlit run dashboard.py
```

---

## Day-by-Day Build Log

### Day 1 — SQL Server Foundations
**Commit:** `Day 1-2: PricingDB schema, tables, stored procedures, indexes`

**What was built:**
- Installed SQL Server 2025 Developer Edition + SSMS 22
- Connected SSMS to `localhost` using Windows Authentication
- Created `PricingDB` database
- Created 6 tables: Products, Customers, Bids, Pricing, Transactions, PriceAuditLog
- Inserted sample data: 8 pharmacy products, 8 insurance customers
- Wrote 5 core queries: SELECT, JOIN, GROUP BY, window functions, CTE

**Key SQL concepts:**
```sql
-- Auto-increment primary key
ProductID INT PRIMARY KEY IDENTITY(1,1)

-- Foreign key
ProductID INT FOREIGN KEY REFERENCES Products(ProductID)

-- Window function
RANK() OVER (ORDER BY SUM(Quantity * UnitPrice) DESC) AS SpendRank

-- CTE
WITH CustomerSpend AS (
  SELECT CustomerName, SUM(Quantity * UnitPrice) AS TotalSpend
  FROM Transactions t JOIN Customers c ON t.CustomerID = c.CustomerID
  GROUP BY CustomerName
)
SELECT * FROM CustomerSpend
WHERE TotalSpend > (SELECT AVG(TotalSpend) FROM CustomerSpend)
```

---

### Day 2 — Stored Procedures + Indexes
**Commit:** `Day 1-2: PricingDB schema, tables, stored procedures, indexes`

**What was built:**
- 5 stored procedures: usp_InsertPricing, usp_GetTopBids, usp_GetDiscount, usp_BidWinRate, usp_UpdatePrice
- 12 indexes: clustered PKs + non-clustered on all FKs + covering index on Pricing

**Key SQL concepts:**
```sql
-- Stored procedure
CREATE PROCEDURE usp_GetDiscount @ProductID INT, @CustomerID INT
AS BEGIN
  SELECT p.BasePrice, pr.NegotiatedPrice,
    ROUND((p.BasePrice - pr.NegotiatedPrice) / p.BasePrice * 100, 2) AS DiscountPct
  FROM Pricing pr
  JOIN Products p  ON pr.ProductID  = p.ProductID
  JOIN Customers c ON pr.CustomerID = c.CustomerID
  WHERE pr.ProductID = @ProductID AND pr.CustomerID = @CustomerID
END

-- Covering index — eliminates table scan
CREATE INDEX IX_Pricing_Cover
ON Pricing(ProductID, CustomerID)
INCLUDE (NegotiatedPrice, EffectiveDate, ExpiryDate)
```

---

### Day 3 — Views + Audit Trigger
**Commit:** `Day 1-3: Complete PricingDB - tables, stored procedures, indexes, views, audit trigger`

**What was built:**
- 3 views: vw_MonthlyPricingSummary, vw_CustomerTierAnalysis, vw_BidWinRate
- Audit trigger `trg_PriceAudit` — auto-logs every price change

**Key SQL concepts:**
```sql
-- Trigger using inserted/deleted magic tables
CREATE TRIGGER trg_PriceAudit ON Pricing AFTER UPDATE
AS BEGIN
  SET NOCOUNT ON;
  INSERT INTO PriceAuditLog(PricingID, OldPrice, NewPrice)
  SELECT i.PricingID, d.NegotiatedPrice, i.NegotiatedPrice
  FROM inserted i JOIN deleted d ON i.PricingID = d.PricingID
  WHERE i.NegotiatedPrice <> d.NegotiatedPrice
END
```

---

### Day 4 — Python ETL Pipeline
**Commit:** `Day 4: Python ETL - 100k rows loaded, validation, bulk insert, audit logging`

**What was built:**
- `etl.py` — generates 500 products, 200 customers, 100,000 transactions
- Validates: null check + duplicate check per table
- Bulk inserts using `cursor.fast_executemany = True`
- Full run log saved to `etl.log`

**ETL results:**
```
Inserted 500 rows into Products      — 0 nulls, 0 dupes
Inserted 200 rows into Customers     — 0 nulls, 0 dupes
Inserted 100000 rows into Transactions — 0 nulls, 0 dupes
Total time: 7 seconds
```

**Install + run:**
```bash
pip install pandas pyodbc faker
python etl.py
```

**Connection string:**
```python
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PricingDB;"
    "Trusted_Connection=yes;"
)
```

---

### Day 5 — Streamlit Dashboard
**Commit:** `Day 5: Streamlit dashboard - live pricing KPIs, charts, repricing simulator`

**What was built:**
- Live dashboard pulling data directly from SQL Server
- KPI row: total transactions, total revenue, products, customers
- Revenue by Category bar chart (Plotly)
- Spend by Customer Tier pie chart (Plotly)
- Repricing Simulator — dropdown + slider → live negotiated price calculation
- Recent transactions table (top 20, live)

**Install + run:**
```bash
pip install streamlit plotly
python -m streamlit run dashboard.py
# Opens at http://localhost:8501
```

---

## Full Setup From Scratch

1. Download SQL Server 2025 Developer Edition — microsoft.com/sql-server
2. Run installer — default instance `MSSQLSERVER`
3. Download SSMS 22 — aka.ms/ssmsfullsetup
4. Install SSMS — core components only, no extra workloads
5. Open SSMS and connect:
```
Server name:     localhost
Authentication:  Windows Authentication
Trust Server Certificate: ✅ checked
```
6. Open `PricingDB_Complete.sql` → press F5 — builds entire database
7. Install Python dependencies and run:
```bash
pip install pandas pyodbc faker streamlit plotly
python etl.py
python -m streamlit run dashboard.py
```

---

## GitHub Commands Reference

```bash
# Check git version
git --version

# Clone repo
git clone https://github.com/SaiTejaReddyYeldandi/optum-pricing-db.git
cd optum-pricing-db

# Daily workflow
git add .
git commit -m "your message"
git pull --rebase
git push

# Delete a file
del filename.md
git add .
git commit -m "Remove duplicate file"
git push

# Copy file into repo (Windows)
copy "C:\Users\91852\Downloads\file.sql" "C:\path\to\optum-pricing-db\"

# List files (Windows — not ls)
dir
```

**Why `git pull --rebase`?**
When you edit files on the GitHub website AND locally, they get out of sync. `pull --rebase` fetches remote changes and places your local commits cleanly on top. Use it every time push is rejected with "fetch first" error.

---

## Interview Talking Points

**"Tell me about a complex SQL problem you solved"**
Built a pharmacy pricing database modelling Optum's PULSE/Repricing ecosystem. Designed stored procedures for bid win rate analysis and price audit logging. Added a covering index on the Pricing table that eliminated a full table scan on the most common query — negotiated price lookup by product and customer.

**"Describe your Python ETL experience"**
Built an ETL pipeline using pandas and pyodbc that bulk-loads 100,000 transaction rows in 7 seconds. Includes data validation (null checks, duplicate detection) and structured logging. Uses `fast_executemany=True` for high-throughput bulk insert.

**"What is a covering index?"**
A covering index includes all columns a query needs in the index itself — SQL Server never touches the base table. Example: `CREATE INDEX IX_Pricing_Cover ON Pricing(ProductID, CustomerID) INCLUDE(NegotiatedPrice, EffectiveDate, ExpiryDate)` — fully satisfied from the index, zero table scan.

**"What does the Streamlit dashboard do?"**
It connects live to SQL Server and shows pricing KPIs, revenue by drug category, spend by customer tier, and a Repricing Simulator — select a product and customer, set a discount %, and it calculates the negotiated price in real time. Same concept as the PULSE Repricing Assistant.

**"What is the audit trigger for?"**
Every price update to the Pricing table automatically captures old price, new price, and timestamp into PriceAuditLog — no manual logging needed. Full price change history for compliance and analytics.

---

*30-day bootcamp | Optum Data Analyst — Dublin | Sai Teja Reddy Yeldandi*
