# Rubric Checklist – Engine PM Interim Notebook

| Section | Requirement | Status in Engine_PM_Interim_Notebook.ipynb |
|--------|-------------|--------------------------------------------|
| **Data Registration (6 pts)** | Create a master folder and create a subfolder "data" | ✅ `engine_pm_project` + `engine_pm_project/data` |
| | Register the data on the Hugging Face dataset space | ✅ `data_register.py` uploads folder to HF |
| **Exploratory Data Analysis (10 pts)** | Data collection and background | ✅ Added |
| | Data overview | ✅ Added |
| | Univariate analysis | ✅ Added |
| | Bivariate analysis | ✅ Added |
| | Multivariate analysis | ✅ Added |
| | Insights/observations based on EDA | ✅ Added |
| **Data Preparation (10 pts)** | Load the dataset **directly from the Hugging Face data space** | ✅ prep.py loads from HF first (hf_hub_download), fallback local |
| | Perform data cleaning and remove unnecessary columns | ✅ In prep.py |
| | Split into train/test and save locally | ✅ In prep.py |
| | Upload train and test back to Hugging Face | ✅ In prep.py |
| **Model Building with Experimentation Tracking (8 pts)** | Load train and test **from the Hugging Face data space** | ✅ train.py loads from HF first, fallback local |
| | Define a model and parameters | ✅ RF + AdaBoost + GB, param grids |
| | Tune the model | ✅ RandomizedSearchCV |
| | Log all tuned parameters | ✅ MLflow |
| | Evaluate model performance | ✅ Metrics + classification report |
| | Register best model in Hugging Face model hub | ✅ |
| | Use allowed algorithms (DT, Bagging, RF, AdaBoost, GB, XGBoost) | ✅ Random Forest + AdaBoost + Gradient Boosting |
| **Business Report Quality (6 pts)** | Adhere to business report checklist | ✅ Clear sections and headings |

**Summary:** All rubric items are addressed. Data Preparation and Model Building load from Hugging Face first (then local fallback). EDA is included.
