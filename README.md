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