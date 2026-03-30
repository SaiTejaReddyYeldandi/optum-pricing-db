import pandas as pd
import pyodbc
import logging
from faker import Faker
import random
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# DB connection
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PricingDB;"
    "Trusted_Connection=yes;"
)

fake = Faker()
random.seed(42)

def get_connection():
    return pyodbc.connect(CONN_STR)

def validate_data(df, table_name):
    log.info(f"Validating {table_name}...")
    # Null check
    nulls = df.isnull().sum().sum()
    if nulls > 0:
        log.warning(f"{nulls} null values found in {table_name}")
    # Duplicate check
    dupes = df.duplicated().sum()
    if dupes > 0:
        log.warning(f"{dupes} duplicate rows found in {table_name}")
    log.info(f"Validation complete: {len(df)} rows, {nulls} nulls, {dupes} dupes")
    return df.dropna().drop_duplicates()

def generate_products(n=500):
    log.info(f"Generating {n} products...")
    categories = ['Cholesterol','Diabetes','Blood Pressure',
                  'Antibiotic','Gastric','Mental Health','Pain Relief']
    drugs = ['Lipitor','Metformin','Lisinopril','Atorvastatin',
             'Amoxicillin','Omeprazole','Sertraline','Amlodipine',
             'Ibuprofen','Paracetamol','Aspirin','Warfarin']
    doses = ['5mg','10mg','20mg','50mg','100mg','250mg','500mg']
    rows = []
    for _ in range(n):
        rows.append({
            'ProductName': f"{random.choice(drugs)} {random.choice(doses)}",
            'Category':    random.choice(categories),
            'BasePrice':   round(random.uniform(5.0, 150.0), 2)
        })
    return pd.DataFrame(rows)

def generate_customers(n=200):
    log.info(f"Generating {n} customers...")
    tiers = ['Platinum','Gold','Silver']
    regions = ['Northeast','Southeast','Midwest','South','West','National']
    rows = []
    for _ in range(n):
        rows.append({
            'CustomerName': fake.company(),
            'Tier':         random.choice(tiers),
            'Region':       random.choice(regions)
        })
    return pd.DataFrame(rows)

def generate_transactions(product_ids, customer_ids, n=100000):
    log.info(f"Generating {n} transactions...")
    rows = []
    start_date = datetime(2024, 1, 1)
    for _ in range(n):
        pid = random.choice(product_ids)
        cid = random.choice(customer_ids)
        rows.append({
            'ProductID':  pid,
            'CustomerID': cid,
            'Quantity':   random.randint(10, 2000),
            'UnitPrice':  round(random.uniform(5.0, 145.0), 2),
            'TxnDate':    start_date + timedelta(days=random.randint(0, 450))
        })
    return pd.DataFrame(rows)

def bulk_insert(df, table, conn):
    cursor = conn.cursor()
    cursor.fast_executemany = True
    cols = ','.join(df.columns)
    placeholders = ','.join(['?' for _ in df.columns])
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    data = [tuple(row) for row in df.itertuples(index=False)]
    cursor.executemany(sql, data)
    conn.commit()
    log.info(f"Inserted {len(df)} rows into {table}")

def run_etl():
    log.info("=== ETL STARTED ===")
    conn = get_connection()
    cursor = conn.cursor()

    # Products
    products_df = validate_data(generate_products(500), 'Products')
    bulk_insert(products_df, 'Products', conn)
    cursor.execute("SELECT ProductID FROM Products")
    product_ids = [r[0] for r in cursor.fetchall()]

    # Customers
    customers_df = validate_data(generate_customers(200), 'Customers')
    bulk_insert(customers_df, 'Customers', conn)
    cursor.execute("SELECT CustomerID FROM Customers")
    customer_ids = [r[0] for r in cursor.fetchall()]

    # Transactions
    txn_df = validate_data(
        generate_transactions(product_ids, customer_ids, 100000),
        'Transactions'
    )
    bulk_insert(txn_df, 'Transactions', conn)

    conn.close()
    log.info("=== ETL COMPLETE ===")

if __name__ == "__main__":
    run_etl()