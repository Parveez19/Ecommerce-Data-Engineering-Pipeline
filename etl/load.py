import mysql.connector
from etl.config import DB_CONFIG

def load_data(df):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO fact_sales
    (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, Country, TotalPrice)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    data_list = df.astype(object).values.tolist()
    batch_size = 5000

    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i+batch_size]
        cursor.executemany(insert_query, batch)
        conn.commit()
        print(f"Inserted: {i + len(batch)} rows")

    cursor.close()
    conn.close()
