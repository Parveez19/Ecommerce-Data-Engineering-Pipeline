import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv('data.csv', encoding="latin1")

# compute total price
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# data cleaning
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]
df.dropna(subset=["Description"], inplace=True)
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df.drop_duplicates(inplace=True)

# remove CustomerID (not needed)
df.drop(columns=["CustomerID"], inplace=True)

# convert invoice date to str
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['InvoiceDate'] = df['InvoiceDate'].dt.strftime('%Y-%m-%d %H:%M:%S')

# connect
conn = mysql.connector.connect(
    host= os.getenv('DB_HOST'),
    user= os.getenv('DB_USER'),
    password= os.getenv('PASSWORD') ,
    database= os.getenv('DB_NAME')
)

cursor = conn.cursor()

# correct insert query (8 columns)
insert_query = """
INSERT INTO ecommerce_orders 
(InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, Country, TotalPrice)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# convert df to list of tuples
data_list = df.astype(object).values.tolist()


batch_size = 5000

for i in range(0, len(data_list), batch_size):
    batch = data_list[i:i+batch_size]
    cursor.executemany(insert_query, batch)
    conn.commit()
    print(f"Inserted: {i + len(batch)} rows")


cursor.close()
conn.close()
