import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from huggingface_hub import HfApi
import os

COLUMN_RENAME = {
    "Engine rpm": "Engine_RPM", "Lub oil pressure": "Lub_Oil_Pressure",
    "Fuel pressure": "Fuel_Pressure", "Coolant pressure": "Coolant_Pressure",
    "lub oil temp": "Lub_Oil_Temperature", "Coolant temp": "Coolant_Temperature",
    "Engine Condition": "Engine_Condition",
}
FEATURES = ["Engine_RPM", "Lub_Oil_Pressure", "Fuel_Pressure", "Coolant_Pressure", "Lub_Oil_Temperature", "Coolant_Temperature"]
TARGET = "Engine_Condition"

# Load dataset directly from Hugging Face data space (rubric); fallback to local if unavailable
try:
    from huggingface_hub import hf_hub_download
    path = hf_hub_download("ananttripathiak/engine-pm-data", "engine_data.csv", repo_type="dataset", token=os.getenv("HF_TOKEN"))
    df = pd.read_csv(path).rename(columns=COLUMN_RENAME)
    print("Loaded from Hugging Face.")
except Exception:
    for data_path in ["engine_pm_project/data/engine_data.csv", "engine_data.csv", "data/engine_data.csv"]:
        if os.path.exists(data_path):
            df = pd.read_csv(data_path).rename(columns=COLUMN_RENAME)
            print(f"Loaded from local: {data_path}")
            break
    else:
        raise FileNotFoundError("No data found. Upload engine_data.csv or register on HF.")

df = df[[c for c in df.columns if c in FEATURES + [TARGET]]].drop_duplicates()
if df.isna().any().any():
    df = df.fillna(df.median(numeric_only=True))
df[TARGET] = df[TARGET].astype(int)

X = df[FEATURES]
y = df[TARGET]
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

os.makedirs("engine_pm_project/model_building", exist_ok=True)
Xtrain.to_csv("engine_pm_project/model_building/Xtrain.csv", index=False)
Xtest.to_csv("engine_pm_project/model_building/Xtest.csv", index=False)
ytrain.to_csv("engine_pm_project/model_building/ytrain.csv", index=False)
ytest.to_csv("engine_pm_project/model_building/ytest.csv", index=False)
print(f"Train: {Xtrain.shape[0]}, Test: {Xtest.shape[0]}")

api = HfApi(token=os.getenv("HF_TOKEN"))
for f in ["Xtrain.csv", "Xtest.csv", "ytrain.csv", "ytest.csv"]:
    api.upload_file(path_or_fileobj=f"engine_pm_project/model_building/{f}", path_in_repo=f, repo_id="ananttripathiak/engine-pm-data", repo_type="dataset")
print("Train/test splits uploaded to Hugging Face.")
