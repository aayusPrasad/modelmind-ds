from core.profiler import profile_dataset
from core.task_router import detect_task_type
from core.model_recommender import recommend_models
from core.model_runner import run_baseline
from core.explanation import generate_explanation
import pandas as pd


df = pd.read_csv("sample_data/motor_health_sample.csv")
target = "failure_status"

profile = profile_dataset(df)
task = detect_task_type(df, target)
recommendations = recommend_models(task)
result = run_baseline(df, task, target)
explanation = generate_explanation(task, recommendations, result)

print("Dataset Profile:")
print(profile)
print("\nDetected Task:", task)
print("\nBaseline Result:")
print(result)
print("\nExplanation:")
print(explanation)
