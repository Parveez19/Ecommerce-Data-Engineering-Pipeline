import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    df.dropna(subset=["Description"], inplace=True)
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df.drop_duplicates(inplace=True)

    df.drop(columns=["CustomerID"], inplace=True)

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["InvoiceDate"] = df["InvoiceDate"].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df
