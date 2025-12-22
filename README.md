let's get started with ecommerce etl pipeline

# E-commerce ETL Pipeline

This project demonstrates a simple ETL pipeline using Python and MySQL.

## Dataset
E-commerce transaction dataset from Kaggle.

## Steps
1. Load raw CSV data
2. Clean invalid records (negative quantity, cancelled orders, missing values)
3. Create derived column (TotalPrice)
4. Load cleaned data into MySQL using batch inserts

## Tech Stack
- Python (Pandas)
- MySQL
- SQL

## How to Run
1. Create MySQL database and table using `sql/ecommerce.sql`
2. Update DB credentials in `scripts/load_to_mysql.py`
3. Run:
```bash
python scripts/load_to_mysql.py





## SQL Analytics (Phase 2)

The following queries were used to analyze revenue distribution, product performance,
and time-based trends using MySQL.



 1. Total Revenue by Country

SELECT 
    Country,
    ROUND(SUM(TotalPrice), 2) AS total_revenue
FROM ecommerce_orders
WHERE Country IS NOT NULL
GROUP BY Country
ORDER BY total_revenue DESC;

2. Top 10 Products by Revenue (Excluding Non-Product SKUs)

SELECT 
    StockCode,
    Description,
    ROUND(SUM(TotalPrice), 2) AS product_revenue
FROM ecommerce_orders
WHERE StockCode NOT IN ('POST', 'DOT', 'M')
GROUP BY StockCode, Description
ORDER BY product_revenue DESC
LIMIT 10;

3. Daily Revenue Trend
SELECT 
    DATE(InvoiceDate) AS order_date,
    ROUND(SUM(TotalPrice), 2) AS daily_revenue
FROM ecommerce_orders
GROUP BY DATE(InvoiceDate)
ORDER BY order_date ASC;

4 — MONTHLY REVENUE TREND
SELECT
    YEAR(InvoiceDate) AS year,
    MONTH(InvoiceDate) AS month,
    ROUND(SUM(TotalPrice), 2) AS monthly_revenue
FROM ecommerce_orders
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY year, month;

5-Average Order Value
SELECT
    ROUND(AVG(invoice_revenue), 2) AS average_order_value
FROM (
    SELECT
        InvoiceNo,
        SUM(TotalPrice) AS invoice_revenue
    FROM ecommerce_orders
    GROUP BY InvoiceNo
) t;



data quality validation and findings


Duplicate record check:
Duplicate invoice–product combinations were detected and flagged for further business review, as duplicates may represent legitimate split quantities or data inconsistencies.

invalid unit price check:
A small number of records with zero or negative unit prices were detected and flagged as pricing anomalies.


# add indexes

CREATE INDEX idx_invoice_stock
ON ecommerce_orders (InvoiceNo, StockCode);

CREATE INDEX idx_invoicedate
ON ecommerce_orders (InvoiceDate);

CREATE INDEX idx_country
ON ecommerce_orders (Country);

EXPLAIN
SELECT InvoiceNo, StockCode, COUNT(*)
FROM ecommerce_orders
GROUP BY InvoiceNo, StockCode
HAVING COUNT(*) > 1;

## Phase 5 – ETL Pipeline (Completed)
- Built modular ETL (Extract, Transform, Load)
- Implemented idempotent raw-to-fact loading
- Batch inserts with MySQL
- Environment-based configuration
- Fact table: fact_sales

Docs: note completion of Phase 5 ETL pipeline

## Next Phase
- Implement incremental load using InvoiceDate watermark
