#!/usr/bin/env python3
"""Hosting script: Push deployment files to Hugging Face Spaces."""
import os
from pathlib import Path

def main():
    token = os.getenv("HF_TOKEN")
    if not token:
        print("Set HF_TOKEN to push to Hugging Face Spaces.")
        return
    try:
        from huggingface_hub import HfApi, create_repo
        from huggingface_hub.utils import RepositoryNotFoundError
    except ImportError:
        print("Install: pip install huggingface_hub")
        return
    api = HfApi(token=token)
    space_id = "ananttripathiak/engine-pm-streamlit"
    deploy_dir = Path(__file__).resolve().parent
    try:
        api.repo_info(repo_id=space_id, repo_type="space")
        print(f"Space '{space_id}' exists. Updating.")
    except RepositoryNotFoundError:
        create_repo(repo_id=space_id, repo_type="space", space_sdk="streamlit", private=False)
        print(f"Space '{space_id}' created.")
    for local_name, path_in_repo in [("app.py", "app.py"), ("requirements.txt", "requirements.txt")]:
        path = deploy_dir / local_name
        if path.exists():
            api.upload_file(path_or_fileobj=str(path), path_in_repo=path_in_repo, repo_id=space_id, repo_type="space")
            print(f"Uploaded {path_in_repo}")
    readme = """---
title: Engine Predictive Maintenance
emoji: \u2699
sdk: streamlit
sdk_version: "1.28.0"
app_file: app.py
pinned: false
---
# Engine Predictive Maintenance
Predict engine condition (Normal vs Maintenance Required) from sensor readings.
"""
    (deploy_dir / "README.md").write_text(readme)
    api.upload_file(path_or_fileobj=str(deploy_dir / "README.md"), path_in_repo="README.md", repo_id=space_id, repo_type="space")
    print(f"Done. Open: https://huggingface.co/spaces/{space_id}")

if __name__ == "__main__":
    main()

