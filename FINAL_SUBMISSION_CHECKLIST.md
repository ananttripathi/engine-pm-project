# Final Submission Checklist – Engine Predictive Maintenance

Use this checklist to confirm all rubric criteria and to fill in links/screenshots for the report.

---

## 1. Data Registration (2 pts)
- [ ] Master folder and subfolder `data` created
- [ ] Data registered on Hugging Face dataset space (`ananttripathiak/engine-pm-data`)

## 2. Exploratory Data Analysis (3 pts)
- [ ] Data collection and background
- [ ] Data overview
- [ ] Univariate analysis
- [ ] Bivariate analysis
- [ ] Multivariate analysis
- [ ] Insights/observations based on EDA

## 3. Data Preparation (4 pts)
- [ ] Load dataset directly from Hugging Face data space
- [ ] Data cleaning and remove unnecessary columns
- [ ] Split into training and testing sets; save locally
- [ ] Upload train and test datasets back to Hugging Face data space

## 4. Model Building with Experimentation Tracking (6 pts)
- [ ] Load train and test from Hugging Face data space
- [ ] Define model and parameters (RF, AdaBoost, Gradient Boosting)
- [ ] Tune model with defined parameters (RandomizedSearchCV)
- [ ] Log all tuned parameters (MLflow)
- [ ] Evaluate model performance (accuracy, F1, ROC-AUC, classification report, confusion matrix)
- [ ] Register best model in Hugging Face model hub (`ananttripathiak/engine-pm-model`)

## 5. Model Deployment (12 pts)
- [ ] **Dockerfile** – defined with all configurations: `engine_pm_project/deployment/Dockerfile`
- [ ] **Load model from HF hub** – `app.py` loads `best_model.joblib` from `ananttripathiak/engine-pm-model`
- [ ] **Get inputs and save into dataframe** – `app.py` builds `input_df` from form inputs
- [ ] **Dependencies file** – `engine_pm_project/deployment/requirements.txt`
- [ ] **Hosting script** – `engine_pm_project/deployment/deploy_to_hf_spaces.py` pushes app to HF Spaces

## 6. Automated GitHub Actions Workflow (15 pts)
- [ ] **pipeline.yml** in GitHub repo: `.github/workflows/pipeline.yml`
- [ ] **YAML lists all ML steps**: checkout → set up Python → install deps → data registration → data preparation → model training
- [ ] **Push all files to GitHub** – repo contains notebook, scripts, deployment, workflow
- [ ] **End-to-end workflow automated** – runs on push to `main` and via `workflow_dispatch`
- [ ] **Updates push to main** – pushing code to `main` triggers the pipeline

**Note:** Add `HF_TOKEN` to GitHub repo **Secrets** for steps that use Hugging Face (data upload, prep upload, model upload). Pipeline still runs without it but will skip HF-dependent steps if data is not in repo.

## 7. Output Evaluation (8 pts)

### GitHub
- [ ] **Link to repository:** _________________________________________________
- [ ] **Screenshot: folder structure** (attach image)
- [ ] **Screenshot: executed workflow** (Actions tab, successful run) (attach image)

### Streamlit on Hugging Face
- [ ] **Link to HF Space:** https://huggingface.co/spaces/ananttripathiak/engine-pm-streamlit (or your Space URL)
- [ ] **Screenshot: Streamlit app** (attach image)

**To get the Space live:** Run `python engine_pm_project/deployment/deploy_to_hf_spaces.py` (with `HF_TOKEN` set), or create a new Space on HF, set SDK to Streamlit, and upload `app.py` and `requirements.txt`.

## 8. Actionable Insights and Recommendations (4 pts)

**Key takeaways for the business (add to your report):**

- **High recall for Maintenance:** The best model (Gradient Boosting) achieves ~97% recall for the Maintenance class, so most engines that need maintenance are flagged—reducing risk of missed failures.
- **Trade-off with false positives:** Many Normal engines are predicted as Maintenance (false positives). For preventive maintenance, this is often acceptable; operations can schedule extra inspections rather than miss failures.
- **Use of sensor data:** RPM, oil/coolant pressures and temperatures are predictive; monitoring these in real time supports proactive scheduling.
- **Recommendations:** (1) Deploy the model as a Streamlit app or API for field/workshop use. (2) Retrain periodically with new data to adapt to engine fleet changes. (3) Consider threshold tuning or cost-sensitive learning if false positives become costly. (4) Integrate with existing maintenance logs to track prediction accuracy over time.

## 9. Business Report Quality (6 pts)
- [ ] Adhere to the business report checklist (formatting, sections, clarity, references)

---

## File locations (quick reference)

| Item | Path |
|------|------|
| Dockerfile | `engine_pm_project/deployment/Dockerfile` |
| Dependencies | `engine_pm_project/deployment/requirements.txt` |
| Streamlit app (load model, inputs → dataframe) | `engine_pm_project/deployment/app.py` |
| Hosting script (push to HF Spaces) | `engine_pm_project/deployment/deploy_to_hf_spaces.py` |
| GitHub Actions workflow | `.github/workflows/pipeline.yml` |
| Data registration | `engine_pm_project/model_building/data_register.py` |
| Data preparation | `engine_pm_project/model_building/prep.py` |
| Model training | `engine_pm_project/model_building/train.py` |
