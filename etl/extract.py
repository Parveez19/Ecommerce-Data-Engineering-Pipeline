from pathlib import Path
import pandas as pd
import logging

def extract_data(csv_path: str) -> pd.DataFrame:
    csv_file = Path(csv_path)

    if not csv_file.exists():
        logging.error(f"CSV file not found: {csv_file}")
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    df = pd.read_csv(csv_file, encoding="latin1")

    if df.empty:
        logging.warning("Extracted DataFrame is empty")

    logging.info(f"Extracted {len(df)} rows from {csv_file}")

    return df
