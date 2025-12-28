import pandas as pd
from dotenv import load_dotenv
import logging
import os

load_dotenv()

def extract_data(s3_path: str) -> pd.DataFrame:
    logging.info(f"Extracting data from: {s3_path}")
    
    try:
        df = pd.read_csv(s3_path, encoding="latin1")

        if df.empty:
            logging.warning("Extracted DataFrame is empty")

        logging.info(f"Extracted {len(df)} rows")
        return df

    except Exception as e:
        logging.error(f"Error reading from S3: {e}")
        raise

actual_path = os.getenv("DB_s3")
my_dataframe = extract_data(actual_path)