import warnings
import pandas as pd


def profile_dataset(df: pd.DataFrame) -> dict:
    """Create a simple Dataset Passport."""
    profile = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_columns": list(df.select_dtypes(include=["int64", "float64"]).columns),
        "categorical_columns": list(df.select_dtypes(include=["object", "category", "bool"]).columns),
        "datetime_columns": [],
        "duplicate_rows": int(df.duplicated().sum()),
    }

    for col in df.select_dtypes(include=["object", "category"]).columns:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            converted = pd.to_datetime(df[col], errors="coerce")
        if converted.notna().mean() > 0.8:
            profile["datetime_columns"].append(col)

    return profile


def data_quality_score(profile: dict) -> float:
    """Return a simple quality score from 0 to 100."""
    total_cells = profile["rows"] * profile["columns"]
    if total_cells == 0:
        return 0.0

    missing_total = sum(profile["missing_values"].values())
    missing_ratio = missing_total / total_cells
    duplicate_penalty = min(profile["duplicate_rows"] / max(profile["rows"], 1), 1)

    score = 100 - (missing_ratio * 60) - (duplicate_penalty * 40)
    return round(max(score, 0), 2)
