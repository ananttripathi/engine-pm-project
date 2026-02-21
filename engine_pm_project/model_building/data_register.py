from huggingface_hub import HfApi, create_repo
from huggingface_hub.utils import RepositoryNotFoundError
import os

repo_id = "ananttripathiak/engine-pm-data"
repo_type = "dataset"
api = HfApi(token=os.getenv("HF_TOKEN"))

try:
    api.repo_info(repo_id=repo_id, repo_type=repo_type)
    print(f"Repo '{repo_id}' already exists. Using it.")
except RepositoryNotFoundError:
    create_repo(repo_id=repo_id, repo_type=repo_type, private=False)
    print(f"Repo '{repo_id}' created.")

api.upload_folder(
    folder_path="engine_pm_project/data",
    repo_id=repo_id,
    repo_type=repo_type,
)
print("Data folder uploaded to Hugging Face.")
