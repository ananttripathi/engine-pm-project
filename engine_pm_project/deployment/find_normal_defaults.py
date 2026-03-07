"""Find one row that model predicts as clearly Normal (min maintenance prob)."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from huggingface_hub import hf_hub_download
import joblib
import pandas as pd

FEATURES = ["Engine_RPM", "Lub_Oil_Pressure", "Fuel_Pressure", "Coolant_Pressure", "Lub_Oil_Temperature", "Coolant_Temperature"]

def main():
    from datasets import load_dataset
    ds = load_dataset("ananttripathiak/engine-pm-data", token=os.getenv("HF_TOKEN"))
    X = ds["train"].to_pandas()[FEATURES]
    path = hf_hub_download(repo_id="ananttripathiak/engine-pm-model", filename="best_model.joblib", repo_type="model", token=os.getenv("HF_TOKEN"))
    model = joblib.load(path)
    proba = model.predict_proba(X)
    maint = proba[:, 1]
    best_idx = maint.argmin()
    row = X.iloc[best_idx]
    print("Values with LOWEST maintenance probability:")
    for k in FEATURES:
        v = row[k]
        print(f"  {k}: {v}")
    print(f"\nMaintenance prob: {maint[best_idx]:.2%}")

if __name__ == "__main__":
    main()
