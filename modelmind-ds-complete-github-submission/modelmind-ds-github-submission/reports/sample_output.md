# Sample Output Report

## Dataset

Motor health monitoring dataset with temperature, vibration, voltage, current, load, running hours, maintenance interval, and failure status.

## Detected Task

Classification

## Reason

The selected target column `failure_status` contains categorical labels: Normal and Failure.

## Recommended Models

1. Logistic Regression
2. Random Forest Classifier

## Selected Baseline

Random Forest Classifier

## Main Metric

Weighted F1-score

## Explanation

The failure-status dataset may contain class imbalance because failure cases are usually fewer than normal cases. F1-score is therefore more useful than accuracy alone. The Random Forest baseline is suitable because it can capture non-linear relationships between sensor readings and failure risk.

## Limitation

The prototype is a first-pass assistant. It requires domain validation before use in any real industrial environment.
