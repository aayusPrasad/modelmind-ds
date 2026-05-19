# ModelMind-DS: Adaptive Data Science Workflow Assistant

ModelMind-DS is a lightweight prototype for ABB EngineeredX 2.0.

It helps a user upload a dataset, understand the dataset structure, detect the likely data science task, recommend suitable models, run baseline experiments, and generate an explainable summary of the chosen workflow.

## Problem Statement

Design and evaluate data science language models that can adapt to different data science models.

## Why this project is relevant

In industrial environments, teams often work with different kinds of datasets:

- Motor health and predictive maintenance data
- Energy usage and load forecasting data
- Quality inspection data
- Process optimization data
- Sensor anomaly detection data

A single fixed machine learning model cannot handle all these cases. ModelMind-DS acts as an adaptive controller that studies the dataset first and then routes the problem to a suitable data science workflow.

## Main Features

- Dataset profiling
- Missing value and data-type inspection
- Automatic task detection
- Model recommendation
- Baseline model training
- Metric-based evaluation
- Simple explanation of the decision process
- Streamlit-based demo interface

## Supported Task Types

| Task Type | Detection Signal | Suggested Models |
|---|---|---|
| Regression | Numeric target column | Linear Regression, Random Forest Regressor |
| Classification | Categorical or low-cardinality target | Logistic Regression, Random Forest Classifier |
| Clustering | No target column selected | K-Means |
| Time Series | Date/time column detected | Future extension: ARIMA/Prophet/LSTM |
| Anomaly Detection | Sensor/maintenance data with rare failure patterns | Future extension: Isolation Forest |

## Repository Structure

```text
modelmind-ds/
├── app.py
├── demo_cli.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/
│   ├── profiler.py
│   ├── task_router.py
│   ├── model_recommender.py
│   ├── model_runner.py
│   └── explanation.py
├── sample_data/
│   └── motor_health_sample.csv
├── assets/
│   └── architecture.txt
└── reports/
    └── sample_output.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/modelmind-ds.git
cd modelmind-ds
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate it

For Windows:

```bash
venv\Scripts\activate
```

For Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
streamlit run app.py
```

## Quick CLI Test

```bash
python demo_cli.py
```

## Demo Dataset

A sample industrial motor-health dataset is included in:

```text
sample_data/motor_health_sample.csv
```

It contains fields such as temperature, vibration, voltage, current, load, running hours, and failure status.

## Example Use Case

For a motor-health dataset, the system can detect that the target column `failure_status` is categorical. It then treats the problem as a classification task and recommends models such as Logistic Regression and Random Forest Classifier.

The system evaluates the models using accuracy, precision, recall, F1-score, and confusion matrix.

## Current Limitation

This is a prototype. It does not replace an expert data scientist. It focuses on creating a reliable first-pass workflow and explanation. Final deployment would require domain validation, model monitoring, and industrial safety checks.

## Future Scope

- Add support for time-series forecasting
- Add anomaly detection using Isolation Forest
- Add model card generation
- Add SHAP-based explainability
- Add LLM-generated natural language reports
- Add MLflow tracking for experiments

## Author

Prepared as a student prototype for ABB EngineeredX 2.0.
