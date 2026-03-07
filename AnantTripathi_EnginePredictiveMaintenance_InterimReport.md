# Interim Project Report
## Engine Predictive Maintenance – MLOps Pipeline

**Learner Name:** Anant Tripathi  
**Project Name:** Engine Predictive Maintenance  
**Date:** February 2026

![Title Page – Predictive Maintenance for Engine Condition Classification](title_page.png)

---

## 1. Executive Summary

This interim report presents the progress of an end-to-end MLOps pipeline for **Engine Predictive Maintenance**. The pipeline automates data registration, exploratory data analysis, data preparation, and model building with experimentation tracking. The system classifies engine conditions (Normal vs. Maintenance Required) using sensor data and deploys the trained model for real-time predictions.

---

## 2. Data Registration

### 2.1 Methodology

A master folder structure is created with a `data` subfolder. The raw engine sensor dataset is registered on the Hugging Face Dataset Hub at `ananttripathiak/engine-maintenance-dataset` using the `data_register.py` script. This enables version control, reproducibility, and seamless integration with downstream pipeline steps.

### 2.2 Implementation

- **Master folder:** `engine_maintenance_project/`
- **Data subfolder:** `engine_maintenance_project/data/`
- **Dataset:** `engine_data.csv` (19,535 rows × 7 columns)
- **Hugging Face Repo:** [ananttripathiak/engine-maintenance-dataset](https://huggingface.co/datasets/ananttripathiak/engine-maintenance-dataset)

### 2.3 Business Implication

Centralized data registration reduces manual errors, ensures consistency across experiments, and supports collaboration. Version-controlled datasets enable audit trails and reproducibility for compliance and quality assurance.

---

## 3. Exploratory Data Analysis

### 3.1 Data Collection and Background

The dataset consists of engine sensor readings collected from equipment in operation. Each row represents a snapshot of key physical measurements—RPM, oil pressure, fuel pressure, coolant pressure, oil and coolant temperatures—along with an **Engine_Condition** label (Normal vs. Maintenance Required). This data supports predictive maintenance: by learning patterns that precede failures, we can build models to flag engines before they break down. The same dataset is registered on Hugging Face for reproducibility and version control.

### 3.2 Data Overview

| Metric | Value |
|--------|-------|
| Rows | 19,535 |
| Columns | 7 (6 features + 1 target) |
| Missing Values | None |
| Data Types | All numerical (int64: Engine_RPM, target; float64: pressures, temperatures) |

**Features:** Engine_RPM, Lub_Oil_Pressure, Fuel_Pressure, Coolant_Pressure, Lub_Oil_Temperature, Coolant_Temperature  
**Target:** Engine_Condition (0: Normal, 1: Maintenance Required)

Basic statistics (min, max, mean, std, quartiles) confirm ranges consistent with engine sensor data. The target is imbalanced (e.g. ~63% Maintenance, ~37% Normal), which motivates stratified splits and F1-based evaluation.

### 3.3 Univariate Analysis

- **Target distribution:** A bar chart of Engine_Condition shows class counts (Normal vs. Maintenance). The imbalance supports using stratified sampling and metrics such as F1.
- **Feature distributions:** Histograms and summary statistics (mean, std, skewness) describe each numeric feature. Ranges and central tendency are documented; some features show skew or long tails (e.g. Coolant_Temperature with high max and positive skew). For tree-based models we proceed with raw features; scaling is applied in the pipeline for consistency.
- **Observation:** Class imbalance and feature skewness inform preprocessing and model choice (stratified splits, F1, and tree-based algorithms that handle mixed scales).

*Refer to notebook: target bar chart, histograms per feature, and feature statistics.*

### 3.4 Bivariate Analysis

Bivariate analysis compares each feature across the two target classes (Normal vs. Maintenance) to identify which sensors are most discriminative.

- **Box plots:** Features plotted by Engine_Condition show differences in median, spread, and outliers between classes. All six sensor features are compared side by side.
- **Violin plots:** First a subset of four features, then **all six features** in a 2×3 grid. Violins show full distribution shape and density by class, making overlap and separation visible (e.g. temperatures and pressures often differ between Normal and Maintenance).
- **Strip plots:** Point clouds for Lub_Oil_Temperature and Coolant_Temperature by condition (on a sample) illustrate overlap and spread of individual readings.
- **Grouped bar chart:** Mean of each feature by Engine_Condition gives a direct numeric comparison; the chart highlights which sensors differ most between classes.
- **Mean table:** Mean feature values by class are printed for exact numeric comparison.

**Business insight:** Features that separate the two classes (e.g. pressures, temperatures, RPM) are strong candidates for the model. Real-time monitoring of these sensors can support proactive maintenance scheduling.

*Refer to notebook: box plots, violin plots (subset and all 6), strip plots, grouped bar chart, and mean-by-class table.*

### 3.5 Multivariate Analysis

Multivariate analysis examines correlations between features and with the target, and how multiple variables relate together.

- **Correlation matrix:** A heatmap of pairwise correlations (including the target) shows linear relationships. Strong correlations between some features may suggest redundancy; tree-based models can still use multiple signals effectively.
- **Scatter plots by condition:**  
  - Lub_Oil_Temperature vs. Coolant_Temperature and Engine_RPM vs. Lub_Oil_Pressure (colored by Engine_Condition) show how two dimensions separate the classes.  
  - An additional 2×2 grid of scatter plots covers: Fuel_Pressure vs. Coolant_Pressure; Coolant_Temperature vs. Coolant_Pressure; Engine_RPM vs. Coolant_Temperature; Lub_Oil_Pressure vs. Lub_Oil_Temperature. Together these reveal which feature pairs help distinguish Normal from Maintenance.
- **Feature–target correlation:** A table and a **horizontal bar chart** of the absolute correlation of each feature with Engine_Condition quantify which features are most linearly associated with the target. Engine_RPM typically shows the strongest (negative) correlation with maintenance need.
- **Pair plot:** A pair plot on a sample (e.g. Engine_RPM, Lub_Oil_Temperature, Coolant_Temperature) with KDE on the diagonal and scatter off-diagonal, colored by condition, summarizes joint structure and separation.

**Observation:** Features with higher correlation to the target and clearer separation in scatter plots support the feasibility of a classifier. Lower RPM combined with abnormal pressure/temperature patterns may indicate fault conditions.

*Refer to notebook: correlation heatmap, scatter pairs (initial two + 2×2 grid), feature–target correlation bar chart, and pair plot.*

### 3.6 EDA Insights and Observations

1. **Data quality:** All features are numeric; no missing values. Duplicates are dropped in data preparation.
2. **Target balance:** Engine_Condition is imbalanced (e.g. Maintenance ~63%, Normal ~37%). Stratified train/test splits and F1-score are used for tuning and evaluation.
3. **Univariate:** Feature distributions show different ranges and skewness; the target bar chart confirms imbalance.
4. **Bivariate:** Box and violin plots by condition show clear separation for several sensors; mean values by class and strip/bar visuals identify the most predictive features.
5. **Multivariate:** Correlation matrix and scatter plots show relationships between features and with the target; the feature–target correlation bar chart and pair plot support model and feature choices.
6. **Recommendations applied:** Stratified train/test split; all six sensor features retained; tree-based models (Random Forest, AdaBoost, Gradient Boosting); F1 and ROC-AUC monitored.

---

## 4. Data Preparation

### 4.1 Methodology

- Load data from Hugging Face or local file
- Clean: rename columns, drop duplicates, handle missing values (median imputation)
- Split: 80% train, 20% test, stratified by target
- Save locally and upload train/test splits to Hugging Face dataset repo

### 4.2 Results

| Split | Size |
|-------|------|
| Train | 15,628 |
| Test | 3,907 |

Train and test datasets saved as `data/train.csv` and `data/test.csv` and uploaded to the Hugging Face dataset repository.

### 4.3 Business Implication

Proper data preparation ensures model generalizability. Stratified splitting preserves class distribution, and versioned datasets support reproducible model retraining.

---

## 5. Model Building with Experimentation Tracking

### 5.1 Methodology

- **Algorithm:** Random Forest Classifier
- **Preprocessing:** StandardScaler (scikit-learn Pipeline)
- **Hyperparameter Tuning:** RandomizedSearchCV (12 iterations, 3-fold CV, F1 scoring)
- **Experiment Tracking:** MLflow (parameters, metrics, artifacts)
- **Model Registry:** Best model saved locally and uploaded to Hugging Face Model Hub

**Hyperparameter Search Space:**
- n_estimators: [100, 200, 300]
- max_depth: [None, 10, 20]
- min_samples_split: [2, 5]
- min_samples_leaf: [1, 2]

### 5.2 Best Parameters

| Parameter | Value |
|-----------|-------|
| n_estimators | 300 |
| max_depth | 10 |
| min_samples_split | 5 |
| min_samples_leaf | 1 |

### 5.3 Model Performance Metrics

| Metric | Train | Test |
|--------|-------|------|
| Accuracy | 0.77 | 0.66 |
| F1-Score | 0.83 | 0.76 |
| ROC-AUC | — | 0.70 |

### 5.4 Classification Report (Test Set)

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Normal | 0.57 | 0.35 | 0.43 | 1,444 |
| Maintenance | 0.69 | 0.85 | 0.76 | 2,463 |
| **Accuracy** | | | **0.66** | **3,907** |
| Macro Avg | 0.63 | 0.60 | 0.60 | 3,907 |
| Weighted Avg | 0.65 | 0.66 | 0.64 | 3,907 |

### 5.5 Confusion Matrix (Test Set)

|  | Predicted Normal | Predicted Maintenance |
|--|------------------|------------------------|
| **Actual Normal** | 504 | 940 |
| **Actual Maintenance** | 377 | 2,086 |

### 5.6 Business Implications

- **Recall for Maintenance (0.85):** The model correctly identifies 85% of engines requiring maintenance, reducing risk of missed failures.
- **Precision for Maintenance (0.69):** Some false positives; acceptable for preventive maintenance where over-inspection is preferable to missed failures.
- **ROC-AUC (0.70):** Moderate discriminative ability; room for improvement with additional features or alternative algorithms.

---

## 6. Conclusion

The interim pipeline successfully implements:
1. **Data Registration** on Hugging Face
2. **Comprehensive EDA** with univariate, bivariate, and multivariate analysis
3. **Data Preparation** with train/test splits and versioning
4. **Model Building** with Random Forest, hyperparameter tuning, MLflow tracking, and Hugging Face model registration

The model achieves a test F1-score of 0.76 and ROC-AUC of 0.70, with strong recall for the maintenance class. The pipeline is ready for deployment and GitHub Actions automation in the final submission.

---

## Appendix

*Raw code, full model logs, and extended outputs are available in the accompanying HTML notebook: `AnantTripathi_EnginePredictiveMaintenance_Notebook.html`.*

---

*Page 1 of 1*
