import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    df = df.dropna(subset=["InvoiceNo", "InvoiceDate", "Quantity", "UnitPrice", "Description"])

    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])

    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    df = df.drop_duplicates(subset=["InvoiceNo", "StockCode"])

    return df
