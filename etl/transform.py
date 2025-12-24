import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove cancelled invoices
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Remove invalid quantities and prices
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # Drop rows with missing descriptions
    df = df.dropna(subset=["Description"])

    # Create derived column
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    # Remove duplicates
    df = df.drop_duplicates()

    # Convert InvoiceDate to datetime (keep as datetime)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df
