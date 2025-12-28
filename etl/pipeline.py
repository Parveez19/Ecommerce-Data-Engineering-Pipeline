from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data
from dotenv import load_dotenv
import os

load_dotenv()

def run_pipeline():
    RAW_DATA_PATH = os.getenv("DB_s3")
    df= extract_data(RAW_DATA_PATH)
    df = transform_data(df)
    load_data(df)

if __name__ == "__main__":
    run_pipeline()
    # print("ETL pipeline completed successfully")

