# GitHub repo setup – Engine Predictive Maintenance

Follow these steps to create a new GitHub repo and push this project.

---

## 1. Create the repo on GitHub

1. Go to **https://github.com/new**
2. Set:
   - **Repository name:** `engine-pm-project`
   - **Description:** (optional) e.g. *Interim project: MLOps pipeline for engine predictive maintenance*
   - **Visibility:** Public or Private
   - **Do not** tick “Add a README”, “Add .gitignore”, or “Choose a license” (you already have files locally).
3. Click **Create repository**.

---

## 2. Open terminal in the project folder

```bash
cd /Users/ananttripathi/Desktop/Interim_Submission
```

---

## 3. Initialize Git and add the remote

If this folder is **not** a git repo yet:

```bash
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/engine-pm-project.git
```

Replace `YOUR_USERNAME` with your GitHub username (and the repo name if you chose a different one).

---

## 4. Add, commit, and push

```bash
git add .
git status
git commit -m "Initial commit: Engine Predictive Maintenance interim notebook and report"
git push -u origin main
```

If GitHub asks for login, use a **Personal Access Token** as the password (Settings → Developer settings → Personal access tokens). Or use SSH: `git remote set-url origin git@github.com:YOUR_USERNAME/engine-pm-project.git` and push again.

---

## 5. Optional – use SSH instead of HTTPS

To avoid typing a token each time:

```bash
git remote set-url origin git@github.com:YOUR_USERNAME/engine-pm-project.git
git push -u origin main
```

(Requires SSH key added to your GitHub account.)

---

## What gets committed (and what doesn’t)

- **Committed:** Notebook (`.ipynb`), README, reports (`.md`, `.html`), `.gitignore`, `engine_data.csv`, `data/` (unless you add `data/` to `.gitignore`).
- **Ignored (see `.gitignore`):** `mlruns/`, `.ipynb_checkpoints/`, `*.joblib`, `.env`, Python cache.

To also avoid committing the `data/` folder (train/test CSVs), uncomment the `# data/` line in `.gitignore` and run `git add .` and `git commit` again.

---

## Hugging Face token (for dataset & model upload)

The notebook uploads data and the best model to Hugging Face. It needs a **token**, not a key. Set it on your machine only; **do not put the token in the repo or commit it**.

### 1. Get a token

1. Go to **https://huggingface.co/settings/tokens**
2. Sign in (or create an account).
3. Click **New token**, give it a name (e.g. `engine-pm-project`), choose **Write** (or full access).
4. Copy the token (starts with `hf_...`).

### 2. Use it when running the notebook

**Option A – Environment variable (recommended)**  
In Terminal, before starting Jupyter or running the notebook:

```bash
export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Then start Jupyter from that same terminal. The notebook will read `HF_TOKEN` automatically.

**Option B – One-time login (saves token on your machine)**  
In a notebook cell or Terminal:

```bash
pip install -q huggingface_hub
python -c "from huggingface_hub import login; login()"
```

Enter your token when asked. It is stored in `~/.cache/huggingface/token`.

### 3. Do not commit the token

- Do **not** add the token to the repo, README, or any file you push to GitHub.
- `.gitignore` already excludes `.env`; if you use a `.env` file for `HF_TOKEN`, keep it only on your computer and never commit it.

### 4. Store the token in GitHub (for Actions only – key stays safe)

If you want **GitHub Actions** (or other automation) to push to Hugging Face without ever putting the token in your code:

1. On GitHub, open your repo **engine-pm-project**.
2. Go to **Settings** → **Secrets and variables** → **Actions**.
3. Click **New repository secret**.
4. **Name:** `HF_TOKEN`  
   **Value:** paste your Hugging Face token (the one that starts with `hf_...`).
5. Click **Add secret**.

The token is stored **encrypted** by GitHub. It never appears in your repo, in logs, or in the UI after you save it. Only workflows that you define in the repo can use it, and they get it as an environment variable – so your key is not compromised.

**When you run the notebook on your own machine**, you still need to set the token locally (Option A or B above). GitHub Secrets are only available to workflows running on GitHub’s servers, not to your laptop.

**Using the token in GitHub Actions:** This repo includes a workflow (`.github/workflows/run-notebook.yml`) that runs the notebook on push to `main` or when you click "Run workflow" in the Actions tab. The workflow passes `HF_TOKEN` from your repo secret into the job, so when the notebook runs in Actions it will be able to upload to Hugging Face. Add the secret once (step 4 above); it will be used every time the workflow runs.

---

## Later: push updates

After changing the notebook or reports:

```bash
cd /Users/ananttripathi/Desktop/Interim_Submission
git add .
git commit -m "Describe your change"
git push
```
