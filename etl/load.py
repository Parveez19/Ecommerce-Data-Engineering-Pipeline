import os
import logging
import urllib.parse
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def load_to_s3(df: pd.DataFrame, s3_path: str):
  
    try:
        logging.info(f"Writing processed data to {s3_path}")
        df.to_csv(s3_path, index=False)
        logging.info("Success: Processed data written to S3")
    except Exception as e:
        logging.error(f" S3 Upload Error: {e}")
        raise

def load_to_mysql(df: pd.DataFrame):
    
    user = os.getenv("DB_USER")
    raw_password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")

    safe_password = urllib.parse.quote_plus(raw_password) if raw_password else ""

    db_url = f"mysql+mysqlconnector://{user}:{safe_password}@{host}:{port}/{name}"
    
    engine = create_engine(db_url, pool_pre_ping=True)

    try:
        logging.info("Loading data to MySQL...")
        df.to_sql(
            name='ecommerce_sales', 
            con=engine, 
            if_exists='append', 
            index=False,
            chunksize=1000  
        )
        logging.info("Success: Data successfully loaded to MySQL!")
        
    except Exception as e:
        logging.error(f"Database Error: {e}")
        raise
    finally:
        engine.dispose()