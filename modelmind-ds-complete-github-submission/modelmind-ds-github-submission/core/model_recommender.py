def recommend_models(task_type: str) -> list[dict]:
    """Recommend baseline models based on task type."""
    recommendations = {
        "classification": [
            {
                "model": "Logistic Regression",
                "reason": "Simple, interpretable baseline for binary or multiclass classification."
            },
            {
                "model": "Random Forest Classifier",
                "reason": "Handles non-linear relationships and mixed feature behavior well."
            }
        ],
        "regression": [
            {
                "model": "Linear Regression",
                "reason": "Fast baseline for continuous target prediction."
            },
            {
                "model": "Random Forest Regressor",
                "reason": "Useful when sensor patterns are non-linear."
            }
        ],
        "clustering": [
            {
                "model": "K-Means",
                "reason": "Groups similar records when no target column is available."
            }
        ],
        "time-series/regression": [
            {
                "model": "Random Forest Regressor",
                "reason": "Can act as a strong baseline after time-based feature engineering."
            },
            {
                "model": "ARIMA/Prophet",
                "reason": "Future extension for pure forecasting datasets."
            }
        ],
        "unknown": [
            {
                "model": "Manual Review Required",
                "reason": "The dataset structure is not enough to safely infer the task."
            }
        ]
    }

    return recommendations.get(task_type, recommendations["unknown"])
