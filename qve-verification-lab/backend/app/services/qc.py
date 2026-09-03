import numpy as np, pandas as pd
def qc_dataframe(df):
    numeric=df.select_dtypes(include="number")
    missing=int(df.isna().sum().sum())
    dup=int(df.duplicated().sum())
    nonfinite=int((~np.isfinite(numeric.to_numpy())).sum()) if len(numeric.columns) else 0
    return {"status":"PASS" if missing==0 and dup==0 and nonfinite==0 else "WARNING",
            "sample_count":len(df),"missing_values":missing,"duplicate_rows":dup,
            "nonfinite_numeric_values":nonfinite,
            "checks":{"columns":list(df.columns),"numeric_columns":list(numeric.columns)}}
