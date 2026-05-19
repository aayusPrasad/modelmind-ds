import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.cluster import KMeans


def _prepare_features(df: pd.DataFrame, target_column: str | None):
    if target_column and target_column in df.columns:
        X = df.drop(columns=[target_column])
        y = df[target_column]
    else:
        X = df.copy()
        y = None

    X = X.copy()

    for col in X.columns:
        if X[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(X[col]):
                X[col] = X[col].fillna(X[col].median())
            else:
                X[col] = X[col].fillna(X[col].mode()[0])

    X = pd.get_dummies(X, drop_first=True)

    return X, y


def run_baseline(df: pd.DataFrame, task_type: str, target_column: str | None):
    """Run a simple baseline experiment and return metrics."""
    X, y = _prepare_features(df, target_column)

    if task_type == "clustering":
        model = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = model.fit_predict(X)
        return {
            "best_model": "K-Means",
            "metric_name": "Cluster Count",
            "metric_value": int(len(set(clusters))),
            "note": "Clustering completed because no target column was selected."
        }

    if y is None:
        return {
            "best_model": "No model trained",
            "metric_name": "N/A",
            "metric_value": "N/A",
            "note": "Target column is required for supervised learning."
        }

    if task_type == "classification":
        if not pd.api.types.is_numeric_dtype(y):
            encoder = LabelEncoder()
            y = encoder.fit_transform(y.astype(str))

        stratify_value = y if len(set(y)) > 1 else None
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=stratify_value
        )

        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Random Forest Classifier": RandomForestClassifier(random_state=42)
        }

        results = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            results[name] = {
                "accuracy": round(accuracy_score(y_test, pred), 4),
                "f1_score": round(f1_score(y_test, pred, average="weighted"), 4)
            }

        best_model = max(results, key=lambda k: results[k]["f1_score"])

        return {
            "best_model": best_model,
            "metric_name": "Weighted F1-score",
            "metric_value": results[best_model]["f1_score"],
            "all_results": results,
            "note": "F1-score is preferred because industrial failure datasets can be imbalanced."
        }

    if task_type in ["regression", "time-series/regression"]:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42
        )

        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest Regressor": RandomForestRegressor(random_state=42)
        }

        results = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            results[name] = {
                "mae": round(mean_absolute_error(y_test, pred), 4),
                "r2_score": round(r2_score(y_test, pred), 4)
            }

        best_model = min(results, key=lambda k: results[k]["mae"])

        return {
            "best_model": best_model,
            "metric_name": "Mean Absolute Error",
            "metric_value": results[best_model]["mae"],
            "all_results": results,
            "note": "MAE is used because it is easy to interpret in real engineering units."
        }

    return {
        "best_model": "No safe baseline selected",
        "metric_name": "N/A",
        "metric_value": "N/A",
        "note": "The system could not map the dataset to a supported task."
    }
