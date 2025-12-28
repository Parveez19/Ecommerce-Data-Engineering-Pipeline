import os
import urllib.parse 
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

load_dotenv()

def load_data(df: pd.DataFrame):
    
    user = os.getenv("DB_USER")
    raw_password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")

    safe_password = urllib.parse.quote_plus(raw_password) if raw_password else ""

    db_url = f"mysql+mysqlconnector://{user}:{safe_password}@{host}:{port}/{name}"

    engine = create_engine(db_url, pool_pre_ping=True)

    try:
       
        df.to_sql(
            name='ecommerce_sales', 
            con=engine, 
            if_exists='append', 
            index=False,
            chunksize=1000  
        )
        print(" Success: Data successfully loaded to MySQL!")
        
    except Exception as e:
        print(f" Database Error: {e}")
        raise