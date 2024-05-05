import pandas as pd


def one_hot_encode(
    df: pd.DataFrame,
    column: str,
    prefix: str,
) -> pd.DataFrame:

    df_ = df.copy()
    df_encoded = pd.get_dummies(df_[column], dtype="int")
    for col in df_encoded.columns:
        df_[f"{prefix}_{'_'.join(col.strip().lower().split())}"] = df_encoded[col]

    return df_.drop(columns=[column])
