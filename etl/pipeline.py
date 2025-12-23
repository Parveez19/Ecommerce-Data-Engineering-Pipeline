from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

def run_pipeline():
    RAW_DATA_PATH = "data/raw/data.csv"
    df= extract_data(RAW_DATA_PATH)
    df = transform_data(df)
    load_data(df)

if __name__ == "__main__":
    run_pipeline()
    print("ETL pipeline completed successfully")

