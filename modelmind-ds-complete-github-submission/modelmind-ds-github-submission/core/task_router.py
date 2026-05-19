import warnings
import pandas as pd


def detect_task_type(df: pd.DataFrame, target_column: str | None) -> str:
    """
    Detect the likely data science task.

    Logic:
    - No target column -> clustering
    - Date/time columns + numeric target -> time-series candidate
    - Numeric target with many unique values -> regression
    - Categorical or low-cardinality target -> classification
    """
    if target_column is None or target_column == "None":
        return "clustering"

    if target_column not in df.columns:
        return "unknown"

    target = df[target_column]
    unique_count = target.nunique(dropna=True)

    datetime_candidates = []
    for col in df.select_dtypes(include=["object", "category"]).columns:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            converted = pd.to_datetime(df[col], errors="coerce")
        if converted.notna().mean() > 0.8:
            datetime_candidates.append(col)

    if len(datetime_candidates) > 0 and pd.api.types.is_numeric_dtype(target):
        return "time-series/regression"

    if pd.api.types.is_numeric_dtype(target):
        if unique_count <= 10:
            return "classification"
        return "regression"

    return "classification"
