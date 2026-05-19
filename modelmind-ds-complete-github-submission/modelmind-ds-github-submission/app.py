import streamlit as st
import pandas as pd

from core.profiler import profile_dataset, data_quality_score
from core.task_router import detect_task_type
from core.model_recommender import recommend_models
from core.model_runner import run_baseline
from core.explanation import generate_explanation


st.set_page_config(
    page_title="ModelMind-DS",
    page_icon="⚙️",
    layout="wide"
)

st.title("ModelMind-DS")
st.caption("Adaptive Data Science Workflow Assistant for Industrial Datasets")

st.markdown(
    """
    This prototype studies a dataset, creates a Dataset Passport, detects the likely data science task,
    recommends suitable models, runs a baseline experiment, and explains the selected workflow.
    """
)

uploaded_file = st.file_uploader("Upload a CSV dataset", type=["csv"])

st.info("For a quick demo, upload `sample_data/motor_health_sample.csv` from this repository.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("1. Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    profile = profile_dataset(df)
    quality = data_quality_score(profile)

    st.subheader("2. Dataset Passport")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", profile["rows"])
    col2.metric("Columns", profile["columns"])
    col3.metric("Duplicate Rows", profile["duplicate_rows"])
    col4.metric("Data Quality Score", quality)

    with st.expander("View full dataset profile"):
        st.json(profile)

    target_options = ["None"] + list(df.columns)
    target_column = st.selectbox("Select target column", target_options)

    selected_target = None if target_column == "None" else target_column

    st.subheader("3. Task Detection")
    task_type = detect_task_type(df, selected_target)
    st.success(f"Detected task type: {task_type}")

    st.subheader("4. Recommended Models")
    recommendations = recommend_models(task_type)

    for item in recommendations:
        st.markdown(f"**{item['model']}**")
        st.write(item["reason"])

    st.subheader("5. Baseline Experiment")
    if st.button("Run baseline model"):
        try:
            result = run_baseline(df, task_type, selected_target)

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Selected Model", result.get("best_model", "N/A"))
            col_b.metric("Metric", result.get("metric_name", "N/A"))
            col_c.metric("Value", result.get("metric_value", "N/A"))

            if "all_results" in result:
                st.write("All model results:")
                st.json(result["all_results"])

            st.subheader("6. Explanation")
            explanation = generate_explanation(task_type, recommendations, result)
            st.markdown(explanation)

        except Exception as e:
            st.error("The baseline could not be completed.")
            st.write(str(e))

else:
    st.subheader("Suggested Demo Flow")
    st.markdown(
        """
        1. Upload the sample motor-health dataset.
        2. Select `failure_status` as the target column.
        3. Check the detected task type.
        4. Run the baseline model.
        5. Read the generated explanation.
        """
    )

    st.subheader("Architecture")
    st.code(
        """
Dataset → Dataset Passport → Task Router → Model Recommender
        → Baseline Runner → Metrics + Explanation
        """,
        language="text"
    )
