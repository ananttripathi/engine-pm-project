import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import joblib
import os
import mlflow
import mlflow.sklearn
from huggingface_hub import HfApi, create_repo
from huggingface_hub.utils import RepositoryNotFoundError

mlflow.set_tracking_uri("file:./mlruns")
mlflow.set_experiment("engine_predictive_maintenance")

def load_data():
    # Load train and test from Hugging Face data space (rubric); fallback to local
    try:
        from huggingface_hub import hf_hub_download
        Xtrain = pd.read_csv(hf_hub_download("ananttripathiak/engine-pm-data", "Xtrain.csv"))
        Xtest = pd.read_csv(hf_hub_download("ananttripathiak/engine-pm-data", "Xtest.csv"))
        ytrain = pd.read_csv(hf_hub_download("ananttripathiak/engine-pm-data", "ytrain.csv")).values.ravel()
        ytest = pd.read_csv(hf_hub_download("ananttripathiak/engine-pm-data", "ytest.csv")).values.ravel()
        print("Loaded from Hugging Face.")
    except Exception:
        base = "engine_pm_project/model_building"
        Xtrain = pd.read_csv(f"{base}/Xtrain.csv")
        Xtest = pd.read_csv(f"{base}/Xtest.csv")
        ytrain = pd.read_csv(f"{base}/ytrain.csv").values.ravel()
        ytest = pd.read_csv(f"{base}/ytest.csv").values.ravel()
        print("Loaded from local.")
    return Xtrain, Xtest, ytrain, ytest

Xtrain, Xtest, ytrain, ytest = load_data()
print(f"Training: {Xtrain.shape}, Test: {Xtest.shape}")

rf_pipeline = Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier(random_state=42))])
rf_params = {"clf__n_estimators": [100, 200], "clf__max_depth": [10, 20], "clf__min_samples_split": [2, 5]}
rf_search = RandomizedSearchCV(rf_pipeline, rf_params, n_iter=6, cv=3, scoring="f1", n_jobs=-1, random_state=42)
rf_search.fit(Xtrain, ytrain)
rf_best = rf_search.best_estimator_

with mlflow.start_run(run_name="random_forest"):
    mlflow.log_params(rf_search.best_params_)
    p_test = rf_best.predict(Xtest)
    mlflow.log_metrics({"test_accuracy": accuracy_score(ytest, p_test), "test_f1": f1_score(ytest, p_test, zero_division=0), "test_roc_auc": roc_auc_score(ytest, rf_best.predict_proba(Xtest)[:, 1])})
    joblib.dump(rf_best, "model_rf.joblib")
    mlflow.log_artifact("model_rf.joblib", artifact_path="model")

ada_pipeline = Pipeline([("scaler", StandardScaler()), ("clf", AdaBoostClassifier(random_state=42))])
ada_params = {"clf__n_estimators": [50, 100], "clf__learning_rate": [0.01, 0.1, 1.0]}
ada_search = RandomizedSearchCV(ada_pipeline, ada_params, n_iter=6, cv=3, scoring="f1", n_jobs=-1, random_state=42)
ada_search.fit(Xtrain, ytrain)
ada_best = ada_search.best_estimator_
with mlflow.start_run(run_name="adaboost"):
    mlflow.log_params(ada_search.best_params_)
    p_test = ada_best.predict(Xtest)
    mlflow.log_metrics({"test_accuracy": accuracy_score(ytest, p_test), "test_f1": f1_score(ytest, p_test, zero_division=0), "test_roc_auc": roc_auc_score(ytest, ada_best.predict_proba(Xtest)[:, 1])})
    joblib.dump(ada_best, "model_ada.joblib")
    mlflow.log_artifact("model_ada.joblib", artifact_path="model")

gb_pipeline = Pipeline([("scaler", StandardScaler()), ("clf", GradientBoostingClassifier(random_state=42))])
gb_params = {"clf__n_estimators": [100, 200], "clf__max_depth": [3, 6], "clf__learning_rate": [0.01, 0.1]}
gb_search = RandomizedSearchCV(gb_pipeline, gb_params, n_iter=6, cv=3, scoring="f1", n_jobs=-1, random_state=42)
gb_search.fit(Xtrain, ytrain)
gb_best = gb_search.best_estimator_
with mlflow.start_run(run_name="gradient_boosting"):
    mlflow.log_params(gb_search.best_params_)
    p_test = gb_best.predict(Xtest)
    mlflow.log_metrics({"test_accuracy": accuracy_score(ytest, p_test), "test_f1": f1_score(ytest, p_test, zero_division=0), "test_roc_auc": roc_auc_score(ytest, gb_best.predict_proba(Xtest)[:, 1])})
    joblib.dump(gb_best, "model_gb.joblib")
    mlflow.log_artifact("model_gb.joblib", artifact_path="model")

try:
    runs = mlflow.search_runs(experiment_names=["engine_predictive_maintenance"], order_by=["metrics.test_f1 DESC"], max_results=5)
    best_run = runs.iloc[0] if len(runs) > 0 else None
    best_name = best_run["tags.mlflow.runName"] if best_run is not None else "random_forest"
    if best_name == "adaboost":
        best_model = ada_best
    elif best_name == "gradient_boosting":
        best_model = gb_best
    else:
        best_model = rf_best
except Exception:
    rf_f1 = f1_score(ytest, rf_best.predict(Xtest), zero_division=0)
    ada_f1 = f1_score(ytest, ada_best.predict(Xtest), zero_division=0)
    gb_f1 = f1_score(ytest, gb_best.predict(Xtest), zero_division=0)
    cands = [("random_forest", rf_best, rf_f1), ("adaboost", ada_best, ada_f1), ("gradient_boosting", gb_best, gb_f1)]
    best_name, best_model = max(cands, key=lambda x: x[2])[:2]

joblib.dump(best_model, "best_model.joblib")
print(f"Best model: {best_name}")
print(classification_report(ytest, best_model.predict(Xtest), target_names=["Normal", "Maintenance"]))

api = HfApi(token=os.getenv("HF_TOKEN"))
repo_id = "ananttripathiak/engine-pm-model"
try:
    api.repo_info(repo_id=repo_id, repo_type="model")
except RepositoryNotFoundError:
    create_repo(repo_id=repo_id, repo_type="model", private=False)
api.upload_file(path_or_fileobj="best_model.joblib", path_in_repo="best_model.joblib", repo_id=repo_id, repo_type="model")
print(f"Model uploaded to {repo_id}")
