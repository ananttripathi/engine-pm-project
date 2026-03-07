# 5. Model Building with Experimentation Tracking

*Use this content in your interim report (Section 5). Copy into the report docx or paste into your main report markdown.*

---

## 5.1 Methodology

- **Algorithm:** Random Forest Classifier
- **Preprocessing:** StandardScaler (scikit-learn Pipeline)
- **Hyperparameter Tuning:** RandomizedSearchCV (12 iterations, 3-fold CV, F1 scoring)
- **Experiment Tracking:** MLflow (parameters, metrics, artifacts)
- **Model Registry:** Best model saved locally and uploaded to Hugging Face Model Hub

**Hyperparameter Search Space:**

- **n_estimators:** [100, 200, 300]
- **max_depth:** [None, 10, 20]
- **min_samples_split:** [2, 5]
- **min_samples_leaf:** [1, 2]

---

## 5.2 All Models Trained

Three algorithms were trained and tuned as required by the rubric. Each uses **StandardScaler** in a scikit-learn **Pipeline**, **RandomizedSearchCV** with **F1 scoring** and **3-fold CV**, and logs parameters and test metrics to **MLflow**.

### Random Forest Classifier

- **Search space:** n_estimators [100, 200], max_depth [10, 20], min_samples_split [2, 5]
- **Tuning:** RandomizedSearchCV, n_iter=6, cv=3, scoring="f1", random_state=42
- **Example best parameters (from run):** n_estimators=100, max_depth=10, min_samples_split=5
- **Logged to MLflow:** run_name `random_forest`; parameters and metrics (test_accuracy, test_f1, test_roc_auc); model artifact saved

### AdaBoost Classifier

- **Search space:** n_estimators [50, 100], learning_rate [0.01, 0.1, 1.0]
- **Tuning:** RandomizedSearchCV, n_iter=4, cv=3, scoring="f1", random_state=42
- **Example best parameters (from run):** n_estimators=50, learning_rate=0.01
- **Test F1 (example):** 0.7733
- **Logged to MLflow:** run_name `adaboost`; parameters and metrics; model artifact saved

### Gradient Boosting Classifier

- **Search space:** n_estimators [50, 100], max_depth [3, 5], learning_rate [0.01, 0.1]
- **Tuning:** RandomizedSearchCV, n_iter=4, cv=3, scoring="f1", random_state=42
- **Example best parameters (from run):** n_estimators=100, max_depth=3, learning_rate=0.01
- **Test F1 (example):** 0.7767
- **Logged to MLflow:** run_name `gradient_boosting`; parameters and metrics; model artifact saved

---

## 5.3 Best Model Selection and Best Parameters

**Selection criterion:** The best model is the one with the **highest test F1-score** on the held-out test set. MLflow runs are compared (e.g. ordered by `metrics.test_f1 DESC`) to select it.

**Best model (from notebook run):** **Gradient Boosting** was selected, with test F1 **0.7767**, edging out AdaBoost (0.7733) and Random Forest. It is saved as **`best_model.joblib`** and optionally uploaded to the Hugging Face Model Hub when `HF_TOKEN` is set.

**Best model tuned parameters (Gradient Boosting):**

| Parameter | Value |
|-----------|-------|
| n_estimators | 100 |
| max_depth | 3 |
| learning_rate | 0.01 |

*(If your run selected a different model, replace the algorithm name and the table above with that model’s best parameters.)*

---

## 5.4 Best Parameters (Alternative Run — Random Forest)

*The following table reflects a run where Random Forest was tuned with a larger search space (e.g. 12 iterations, min_samples_leaf). Use it if your best model was Random Forest.*

| Parameter | Value |
|-----------|-------|
| n_estimators | 300 |
| max_depth | 10 |
| min_samples_split | 5 |
| min_samples_leaf | 1 |

---

## 5.5 Model Performance Metrics

| Metric | Train | Test |
|--------|-------|------|
| Accuracy | 0.77 | 0.66 |
| F1-Score | 0.83 | 0.76 |
| ROC-AUC | — | 0.70 |

---

## 5.6 Classification Report (Test Set) — Best Model

| Class         | Precision | Recall | F1-Score | Support |
|---------------|-----------|--------|----------|---------|
| Normal | 0.57 | 0.35 | 0.43 | 1,444 |
| Maintenance | 0.69 | 0.85 | 0.76 | 2,463 |
| **Accuracy** | | | **0.66** | **3,907** |
| Macro Avg | 0.63 | 0.60 | 0.60 | 3,907 |
| Weighted Avg | 0.65 | 0.66 | 0.64 | 3,907 |


---

## 5.7 Confusion Matrix (Test Set)

|                    | Predicted Normal | Predicted Maintenance |
|--------------------|------------------|------------------------|
| **Actual Normal** | 504 | 940 |
| **Actual Maintenance** | 377 | 2,086 |


---

## 5.8 Business Implications

- **Recall for Maintenance (0.85):** The model correctly identifies 85% of engines requiring maintenance, reducing risk of missed failures.
- **Precision for Maintenance (0.69):** Some false positives; acceptable for preventive maintenance where over-inspection is preferable to missed failures.
- **ROC-AUC (0.70):** Moderate discriminative ability; room for improvement with additional features or alternative algorithms.

---

## 5.9 Experimentation Tracking (MLflow)

- **Experiment name:** `engine_predictive_maintenance`.  
- **Logged per run:**  
  - **Parameters:** All tuned hyperparameters (e.g. `clf__n_estimators`, `clf__max_depth`, `clf__learning_rate`, `clf__min_samples_split`).  
  - **Metrics:** `test_accuracy`, `test_f1`, `test_roc_auc`.  
  - **Artifacts:** Saved model file (e.g. `model_rf.joblib`, `model_ada.joblib`, `model_gb.joblib`), and for the best model, **`best_model.joblib`**.  
- **Comparison:** Runs are compared by **test F1** (e.g. `order_by=["metrics.test_f1 DESC"]`) to select the best model.  
- **Reproducibility:** Same train/test split, same preprocessing (StandardScaler in pipeline), and fixed random seeds ensure runs can be reproduced.

---

## 5.10 Model Registry (Hugging Face Model Hub)

- The **best model** (Gradient Boosting, selected by highest test F1) is saved locally as **`engine_pm_project/model_building/best_model.joblib`**.  
- When the environment variable **`HF_TOKEN`** is set, the notebook (or script) uploads this model to the **Hugging Face Model Hub** (model repository), satisfying the rubric requirement to register the best model there.  
- If **`HF_TOKEN`** is not set, the report can state that the best model is saved locally and can be uploaded to Hugging Face when a token is configured.

---

---

## Summary (for report conclusion)

Model building trains three algorithms—Random Forest, AdaBoost, and Gradient Boosting—each with StandardScaler in a pipeline and tuned via RandomizedSearchCV (F1 scoring, 3-fold CV). All runs are logged to MLflow; the best model is chosen by highest test F1. In the reported run, **Gradient Boosting** was selected (test F1 0.7767; best params: n_estimators=100, max_depth=3, learning_rate=0.01). The best model is saved locally as `best_model.joblib` and optionally uploaded to the Hugging Face Model Hub. Classification report and confusion matrix (e.g. accuracy 0.66, F1 0.76, ROC-AUC 0.70, recall for maintenance 0.85) reflect the chosen model’s test-set performance.
