import pandas as pd

def extract_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv("./data.csv", encoding="latin1")
    return df
