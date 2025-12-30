import pandas as pd
import logging

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
