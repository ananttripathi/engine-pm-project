#!/usr/bin/env python3
"""
Hosting script: Push all deployment files to Hugging Face Spaces.
Final submission: Define a hosting script that can push all the deployment files into the Hugging Face space.

Usage:
  export HF_TOKEN=your_token
  python deploy_to_hf_spaces.py

This creates or updates a Space (e.g. ananttripathiak/engine-pm-streamlit) with:
  - Dockerfile (container runs Streamlit)
  - app.py (Streamlit app)
  - requirements.txt (dependencies)
  - README.md (Space card; sdk: docker)
"""

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
        create_repo(repo_id=space_id, repo_type="space", space_sdk="docker", private=False)
        print(f"Space '{space_id}' created (Docker SDK).")

    # Push deployment files (Docker Space: Dockerfile + app + requirements)
    files_to_upload = [
        ("Dockerfile", "Dockerfile"),
        ("app.py", "app.py"),
        ("requirements.txt", "requirements.txt"),
    ]
    readme = """---
title: Engine Predictive Maintenance
emoji: 🔧
sdk: docker
app_port: 8501
pinned: false
---
# Engine Predictive Maintenance
Predict engine condition (Normal vs Maintenance Required) from sensor readings.
"""
    (deploy_dir / "README.md").write_text(readme)
    files_to_upload.append(("README.md", "README.md"))

    for local_name, path_in_repo in files_to_upload:
        path = deploy_dir / local_name
        if path.exists():
            api.upload_file(
                path_or_fileobj=str(path),
                path_in_repo=path_in_repo,
                repo_id=space_id,
                repo_type="space",
            )
            print(f"Uploaded {path_in_repo}")
        else:
            print(f"Skip (not found): {path}")

    print(f"Done. Open: https://huggingface.co/spaces/{space_id}")


if __name__ == "__main__":
    main()
