E-commerce ETL Pipeline
Overview

This project implements an end-to-end E-commerce ETL pipeline, progressing from raw CSV ingestion to analytical querying and optimized storage.
The focus is on data quality, modular ETL design, schema-on-read analytics, and performance optimization.

The pipeline evolves across phases to reflect real-world data engineering practices, not one-off scripts.

Dataset

Public E-commerce transaction dataset (Kaggle)

Contains invoice-level transactional data:

Products

Quantities

Prices

Customers

Countries

Timestamps

Architecture (High Level)
Raw CSV
  ↓
Python ETL (Extract → Transform → Load)
  ↓
MySQL (Operational Analytics)
  ↓
Processed Data in S3
  ↓
Athena (Schema-on-Read Analytics)
  ↓
Partitioned Data (Year / Month)

Phase 1 — Core ETL (Python → MySQL)
Objectives

Build a modular, repeatable ETL pipeline

Enforce data quality rules

Load clean data into a relational store for analytics

ETL Steps

Extract

Load raw CSV using Pandas

Transform

Remove invalid records:

Negative or zero quantity

Cancelled invoices

Missing critical fields

Create derived column:

TotalPrice = Quantity × UnitPrice

Normalize schema and datatypes

Load

Batch inserts into MySQL

Idempotent raw-to-fact loading

Fact table: fact_sales

Tech Stack

Python (Pandas)

MySQL

SQL

How to Run
# Create schema
mysql < sql/ecommerce.sql

# Update DB credentials
vim scripts/load_to_mysql.py

# Run ETL
python scripts/load_to_mysql.py

Phase 2 — SQL Analytics (MySQL)

Analytical queries were written to validate data quality and extract business insights.

Revenue by Country
SELECT 
    Country,
    ROUND(SUM(TotalPrice), 2) AS total_revenue
FROM ecommerce_orders
WHERE Country IS NOT NULL
GROUP BY Country
ORDER BY total_revenue DESC;

Top 10 Products by Revenue
SELECT 
    StockCode,
    Description,
    ROUND(SUM(TotalPrice), 2) AS product_revenue
FROM ecommerce_orders
WHERE StockCode NOT IN ('POST', 'DOT', 'M')
GROUP BY StockCode, Description
ORDER BY product_revenue DESC
LIMIT 10;

Daily Revenue Trend
SELECT 
    DATE(InvoiceDate) AS order_date,
    ROUND(SUM(TotalPrice), 2) AS daily_revenue
FROM ecommerce_orders
GROUP BY DATE(InvoiceDate)
ORDER BY order_date;

Monthly Revenue Trend
SELECT
    YEAR(InvoiceDate) AS year,
    MONTH(InvoiceDate) AS month,
    ROUND(SUM(TotalPrice), 2) AS monthly_revenue
FROM ecommerce_orders
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
ORDER BY year, month;

Average Order Value
SELECT
    ROUND(AVG(invoice_revenue), 2) AS average_order_value
FROM (
    SELECT
        InvoiceNo,
        SUM(TotalPrice) AS invoice_revenue
    FROM ecommerce_orders
    GROUP BY InvoiceNo
) t;

Data Quality Validation

Duplicate invoice-product combinations

Detected and flagged

May represent legitimate split quantities or upstream inconsistencies

Invalid pricing

Zero or negative unit prices identified

Flagged as pricing anomalies for downstream handling

Indexing & Query Optimization

Indexes added to improve analytical performance:

CREATE INDEX idx_invoice_stock
ON ecommerce_orders (InvoiceNo, StockCode);

CREATE INDEX idx_invoicedate
ON ecommerce_orders (InvoiceDate);

CREATE INDEX idx_country
ON ecommerce_orders (Country);


Validation using EXPLAIN confirmed reduced scan cost for aggregation queries.

Phase 3 — Cloud Analytics (S3 + Athena)
Objectives

Move from database-bound analytics to schema-on-read

Query large datasets directly from S3

Key Concepts Implemented

External tables in Athena

CSV ingestion using OpenCSVSerde

Explicit schema alignment

Timestamp casting at query time

Phase 4 — Partitioning (Athena Optimization)

Processed data was reorganized into a partitioned S3 layout:

Processed/
 └── year=2011/
     └── month=07/
         └── data.csv

Benefits

Reduced data scanned per query

Lower Athena query cost

Faster execution using partition pruning

Partitions were registered using:

MSCK REPAIR TABLE ecommerce_sales_partitioned;

Phase 5 — ETL Pipeline Refinement (Completed)

Modular ETL design

Idempotent raw-to-fact loading

Batch inserts

Environment-based configuration

Fact table modeling (fact_sales)