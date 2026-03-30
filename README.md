optum-pricing-db
Pharmacy pricing SQL Server DB — Optum PULSE/Repricing system
Built as part of a 30-day interview prep bootcamp targeting the Optum Data Analyst role (Dublin). This project directly mirrors the PULSE/Repricing Assistant ecosystem described in the Optum JD.
---
What This Project Does
A production-grade SQL Server database modelling a pharmacy pricing and repricing system with:
6 tables covering the full bid lifecycle
5 stored procedures for pricing operations
12 indexes including a covering index
3 analytical views
Audit trigger for every price change
Python ETL pipeline that loads 100,000+ rows with validation and logging
---
Project Structure
```
optum-pricing-db/
├── PricingDB_Complete.sql   # Full DB schema, data, procedures, views, trigger
├── etl.py                   # Python ETL pipeline (Faker + pyodbc + pandas)
├── etl.log                  # ETL run log showing 100k rows inserted
├── SQLQuery1_OPTUM.sql      # Original dev query file
└── README.md                # This file
```
---
Database Schema
Table	Rows	Description
Products	524	Pharmacy drugs with base prices
Customers	224	Insurance companies with tier + region
Pricing	24	Negotiated prices per customer/product
Transactions	100,030	All pricing transactions
Bids	24	Bid history with won/lost status
PriceAuditLog	1+	Auto-logged on every price change
---
Tech Stack
SQL Server 2025 (Developer Edition)
SSMS 22
Python 3.13 — pandas, pyodbc, faker
Git + GitHub
---
Day-by-Day Build Log
Day 1 — SQL Server Foundations
Commit: `Day 1-2: PricingDB schema, tables, stored procedures, indexes`
What was built:
Installed SQL Server 2025 Developer Edition
Installed SSMS 22
Connected SSMS to localhost using Windows Authentication
Created PricingDB database
Created 6 tables: Products, Customers, Bids, Pricing, Transactions, PriceAuditLog
Inserted sample data: 8 products (real pharmacy drugs), 8 customers (insurance companies)
Wrote 5 core queries: SELECT, JOIN, GROUP BY, window functions (RANK), CTE
Key SQL learned:
`CREATE DATABASE` / `USE`
`IDENTITY(1,1)` for auto-increment primary keys
`FOREIGN KEY REFERENCES` for relational integrity
`RANK() OVER (ORDER BY ...)` window function
CTE with `WITH CustomerSpend AS (...)`
---
Day 2 — Stored Procedures + Indexes
Commit: `Day 1-2: PricingDB schema, tables, stored procedures, indexes`
What was built:
5 stored procedures:
`usp_InsertPricing` — inserts a new pricing record
`usp_GetTopBids` — returns top N bids by value
`usp_GetDiscount` — calculates discount % for a customer/product
`usp_BidWinRate` — bid win rate per customer
`usp_UpdatePrice` — updates price and writes to audit log
12 indexes:
Clustered PKs on all tables (auto-created)
Non-clustered on all foreign keys
Covering index on Pricing(ProductID, CustomerID) INCLUDE(NegotiatedPrice, EffectiveDate, ExpiryDate)
Key SQL learned:
`CREATE PROCEDURE` with input parameters
`EXEC usp_ProcedureName @param`
`CREATE INDEX` vs `CREATE INDEX ... INCLUDE()`
Execution plans to verify index usage
---
Day 3 — Views + Audit Trigger
Commit: `Day 1-3: Complete PricingDB - tables, stored procedures, indexes, views, audit trigger`
What was built:
3 views:
`vw_MonthlyPricingSummary` — revenue by month/product
`vw_CustomerTierAnalysis` — spend analysis by customer tier
`vw_BidWinRate` — win rate by product/category
Audit trigger `trg_PriceAudit`:
Fires automatically on every UPDATE to Pricing table
Logs old price, new price, timestamp to PriceAuditLog
Uses `inserted` and `deleted` magic tables
Key SQL learned:
`CREATE VIEW AS SELECT ...`
`CREATE TRIGGER ... AFTER UPDATE`
`inserted` and `deleted` tables inside triggers
`SET NOCOUNT ON` to suppress row count messages
---
Day 4 — Python ETL Pipeline
Commit: `Day 4: Python ETL - 100k rows loaded, validation, bulk insert, audit logging`
What was built:
`etl.py` — full ETL pipeline:
Generates 500 products, 200 customers, 100,000 transactions using Faker
Validates each dataset: null check, duplicate check
Bulk inserts using `cursor.fast_executemany = True`
Logs every step to `etl.log`
ETL run result:
500 products in 0.09s
200 customers in 0.03s
100,000 transactions in 7s
0 nulls, 0 duplicates
Libraries used:
```
pip install pandas pyodbc faker
```
Connection string used:
```python
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PricingDB;"
    "Trusted_Connection=yes;"
)
```
---
GitHub Commands Used
Setup
```bash
# Check git is installed
git --version

# Clone the repo
git clone https://github.com/SaiTejaReddyYeldandi/optum-pricing-db.git

# Navigate into repo
cd optum-pricing-db
```
Daily workflow
```bash
# Stage all changes
git add .

# Commit with message
git commit -m "Your message here"

# Push to GitHub
git push
```
Fix: rejected push (remote has changes you don't have locally)
```bash
# This happened on Day 4 push
git pull --rebase
git push
```
`pull --rebase` fetches remote changes and puts your local commits on top cleanly. Use this whenever push is rejected.
Copy a file into repo folder (Windows)
```bash
copy "C:\Users\91852\Downloads\filename.sql" "C:\path\to\optum-pricing-db\"
```
List files in folder (Windows CMD — not ls)
```bash
dir
```
---
SSMS Connection Settings
```
Server name:     localhost
Authentication:  Windows Authentication
Trust Server Certificate: ✅ checked
→ Click Connect
```
---
Installation Steps (for reference)
Download SQL Server 2025 Developer Edition from microsoft.com
Run installer — choose default instance `MSSQLSERVER`
Download SSMS 22 from aka.ms/ssmsfullsetup
Install SSMS — core components only, no extra workloads needed
Open SSMS → connect to localhost → Windows Authentication
Run `PricingDB_Complete.sql` to build entire database from scratch
---
Interview Talking Points
"Tell me about a complex SQL problem you solved"
Built a pharmacy pricing database modelling Optum's PULSE/Repricing ecosystem. Designed stored procedures for bid win rate analysis and price audit logging. Added a covering index on the Pricing table that eliminated a full table scan on the most common query pattern — negotiated price lookup by product and customer.
"Describe your Python ETL experience"
Built an ETL pipeline using pandas and pyodbc that generates and bulk-loads 100,000 transaction rows in under 10 seconds. Includes data validation (null checks, duplicate detection) and structured logging. Uses `fast_executemany=True` for high-throughput bulk insert.
"What is a covering index?"
A covering index includes all columns a query needs in the index itself, so SQL Server never has to go back to the base table. For example: `CREATE INDEX IX_Pricing_Cover ON Pricing(ProductID, CustomerID) INCLUDE(NegotiatedPrice, EffectiveDate, ExpiryDate)` — a query selecting those columns for a given product/customer is satisfied entirely from the index.
---
30-day bootcamp | Optum Data Analyst — Dublin | Sai Teja Reddy Yeldandi
