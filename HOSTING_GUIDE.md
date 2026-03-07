# How to Host Your Engine Predictive Maintenance Project

Step-by-step guide: what to upload where, which tokens you need, and how to run everything.

---

## 0. What Spaces/Repos Do You Need? (Created Automatically)

You need **one Hugging Face Space** (the Streamlit app). The other two are **repos** (model + dataset), not Spaces.

| On Hugging Face | Type | Name | Who creates it |
|-----------------|------|------|-----------------|
| **Streamlit app** | **Space** | `ananttripathiak/engine-pm-streamlit` | **Automatically** by `deploy_to_hf_spaces.py` (or by GitHub Actions when the deploy step runs). |
| **Model** | Model repo | `ananttripathiak/engine-pm-model` | **Automatically** by `train.py` when it uploads the model (or by GitHub Actions when the train step runs). |
| **Dataset** | Dataset repo | `ananttripathiak/engine-pm-data` | **Automatically** by `data_register.py` when it uploads data (or by GitHub Actions when the data registration step runs). |

**You do not need to manually create any Space or repo.** As long as `HF_TOKEN` is set (in your terminal or in GitHub Secrets), running the pipeline or the individual scripts will create each repo/Space if it doesn’t exist.

**Via GitHub Actions:** When you push to `main` and `HF_TOKEN` is in repo Secrets, the workflow runs and:
- **Data Registration** → creates the dataset repo (if missing) and uploads data (if `engine_data.csv` is in the repo).
- **Model Training** → creates the model repo (if missing) and uploads `best_model.joblib`.
- **Deploy** → creates the **Space** (if missing) and uploads `app.py` and `requirements.txt`.

So: **one Space** (the app) is created/updated by the deploy step; the other two are **repos** created by the data and train steps.

---

## 1. What You Need Before Starting

| Item | Where | Purpose |
|------|--------|--------|
| **Hugging Face account** | [huggingface.co](https://huggingface.co) | Model hub, dataset, and Streamlit Space |
| **GitHub account** | [github.com](https://github.com) | Code repo and (optional) GitHub Actions |
| **HF access token** | Hugging Face → Settings → Access Tokens | One token for: model hub, datasets, Spaces |

---

## 2. The One Token You Need: `HF_TOKEN`

- **What it is:** A Hugging Face access token with **write** permission.
- **Where to create it:**
  1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
  2. Click **New token**.
  3. Name it (e.g. `engine-pm-deploy`), type **Write**.
  4. Copy the token (starts with `hf_...`). You won’t see it again.

- **Where to use it:**

| Place | How to set | When it’s used |
|-------|------------|----------------|
| **Your computer (terminal)** | `export HF_TOKEN=hf_xxxxxxxxxxxx` | Running notebook, `deploy_to_hf_spaces.py`, or `train.py` |
| **GitHub repo Secrets** | Repo → Settings → Secrets and variables → Actions → New repository secret → Name: `HF_TOKEN`, Value: your token | GitHub Actions (data register, prep, train, deploy) |
| **Hugging Face Space** | Space → Settings → Repository secrets → New secret → Name: `HF_TOKEN`, Value: your token | **Only if** your model repo `ananttripathiak/engine-pm-model` is **private**. The Space runs `app.py` and needs the token to download the model. |

**Important:** Never commit the token in code or in a file you push to Git. Use env vars or secrets only.

---

## 3. What to Upload Where

### A. Hugging Face Model Hub (model only)

- **Repo:** `ananttripathiak/engine-pm-model`
- **What to upload:** One file: **`best_model.joblib`**
- **How:**
  - **Option 1 – From notebook/script:** After training, run the cell or script that uploads the model (e.g. `train.py` or the notebook cell that uses `HfApi().upload_file(...)` to `ananttripathiak/engine-pm-model`). Ensure `HF_TOKEN` is set in that environment.
  - **Option 2 – Manual:** Go to [huggingface.co/ananttripathiak/engine-pm-model](https://huggingface.co/ananttripathiak/engine-pm-model), create the repo if needed, then upload `best_model.joblib` in the Files tab.

The Streamlit app (`app.py`) loads this file by name: `best_model.joblib`.

---

### B. Hugging Face Space (Streamlit app)

- **Space:** `ananttripathiak/engine-pm-streamlit`
- **What to upload:**  
  - **`app.py`** (your Streamlit app)  
  - **`requirements.txt`** (dependencies, must include `plotly`)  
  - **`README.md`** (Space card; the deploy script can create it)

- **How – Recommended (from your project folder):**

```bash
cd /Users/ananttripathi/Desktop/Interim_Submission
export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
python engine_pm_project/deployment/deploy_to_hf_spaces.py
```

This creates the Space if it doesn’t exist and uploads `app.py`, `requirements.txt`, and `README.md` from `engine_pm_project/deployment/`.

- **If the model repo is private:** In the Space [Settings](https://huggingface.co/spaces/ananttripathiak/engine-pm-streamlit/settings) → **Repository secrets**, add a secret named **`HF_TOKEN`** with the same token value. The Space will use it to download the model at runtime.

- **Live app URL:**  
  **https://huggingface.co/spaces/ananttripathiak/engine-pm-streamlit**

---

### C. Hugging Face Dataset (for pipeline; optional for hosting the app)

- **Repo:** `ananttripathiak/engine-pm-data`
- **What:** Raw data and/or train/test splits (e.g. `engine_data.csv`, `Xtrain.csv`, `Xtest.csv`, `ytrain.csv`, `ytest.csv`) if you use the full ML pipeline.
- **Needed for:** Data registration, prep, and training scripts (and GitHub Actions). **Not** required only to host and run the Streamlit app; the app only needs the **model** on the model hub and the **Space** files.

---

### D. GitHub (code and optional CI/CD)

- **Repo:** `engine-pm-project` (or your fork)
- **What to push:** Your full project (notebook, `engine_pm_project/` with model_building + deployment, `.github/workflows/`, README, etc.). Do **not** push `best_model.joblib` or `.env` if you use one; keep them in `.gitignore`.
- **Token for push:** Use your GitHub account (HTTPS + password/Personal Access Token, or SSH key). No need for a separate “hosting” token unless you use GitHub Actions with HF.
- **GitHub Actions:** If you use `.github/workflows/pipeline.yml`, add **`HF_TOKEN`** in the repo **Secrets** (Settings → Secrets and variables → Actions) so the workflow can upload data/model and run the deploy script.

---

## 4. Minimal Steps to Get the App Live (no GitHub Actions)

1. **Train and save the model** (notebook or `train.py`), then upload **`best_model.joblib`** to the model hub repo **`ananttripathiak/engine-pm-model`** (with `HF_TOKEN` set).
2. **Set token:**  
   `export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
3. **Deploy the Space:**  
   `python engine_pm_project/deployment/deploy_to_hf_spaces.py`
4. **If the model repo is private:** Add **`HF_TOKEN`** as a **Repository secret** in the Space settings.
5. Open: **https://huggingface.co/spaces/ananttripathiak/engine-pm-streamlit**

---

## 5. Quick Reference: Tokens and Secrets

| Token / Secret | Where to create | Where to set | Used for |
|----------------|------------------|--------------|----------|
| **HF_TOKEN** | Hugging Face → Settings → Access Tokens (Write) | Terminal: `export HF_TOKEN=...` | Upload model, datasets, deploy Space from your machine |
| **HF_TOKEN** (GitHub) | Same HF token | GitHub → Repo → Settings → Secrets → Actions | GitHub Actions: data register, prep, train, deploy |
| **HF_TOKEN** (Space secret) | Same HF token | HF Space → Settings → Repository secrets | App downloading model when model repo is private |

One HF token is enough for all three; just store it in each place where that environment runs (your machine, GitHub Secrets, Space secrets).

---

## 6. Checklist to “Carry”

- [ ] HF account; HF token (Write) created and saved somewhere safe.
- [ ] Model uploaded to **ananttripathiak/engine-pm-model** (`best_model.joblib`).
- [ ] `HF_TOKEN` set in terminal, then `python engine_pm_project/deployment/deploy_to_hf_spaces.py` run.
- [ ] If model repo is private: **HF_TOKEN** added as Repository secret in the Space.
- [ ] (Optional) Code pushed to GitHub; **HF_TOKEN** added in repo Secrets if using Actions.
- [ ] App opened at: **https://huggingface.co/spaces/ananttripathiak/engine-pm-streamlit**
