from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_to_s3, load_to_mysql
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():
    PROCESSED_S3_PATH = os.getenv("PROCESSED_S3_PATH")
    RAW_DATA_PATH = os.getenv("RAW_S3_PATH")
    df_raw = extract_data(RAW_DATA_PATH)
    df_clean = transform_data(df_raw)

    load_to_s3(df_clean, PROCESSED_S3_PATH)
    load_to_mysql(df_clean)

if __name__ == "__main__":
    run_pipeline()









