# Databricks Notebook (or local script)
# Title: ClinicalTrials.gov API (v2) to DataFrame for LLM Deer Flow

import requests
import pandas as pd

# --- Config ---
query = "lung cancer"
limit = 1000 # How many studies to retrieve

# --- API Request ---
url = f"https://clinicaltrials.gov/api/v2/studies?query.term={query}&pageSize={limit}"
response = requests.get(url)

if response.status_code != 200:
    print("❌ Failed to fetch data. Status:", response.status_code)
    print("Response:", response.text)
else:
    data = response.json()
    studies = data.get("studies", [])

    # --- Extract Relevant Fields ---
    trials_list = []
    for study in studies:
        section = study.get("protocolSection", {})
        id_module = section.get("identificationModule", {})
        status_module = section.get("statusModule", {})
        conditions_module = section.get("conditionsModule", {})
        design_module = section.get("designModule", {})

        trial = {
            "nct_id": study.get("nctId"),
            "title": id_module.get("briefTitle"),
            "status": status_module.get("overallStatus"),
            "conditions": conditions_module.get("conditions", []),
            "phase": design_module.get("phase"),
        }
        trials_list.append(trial)

    # --- Convert to DataFrame ---
    df_trials = pd.DataFrame(trials_list)
    print(df_trials)  # works in Databricks

    # If using locally:
    # print(df_trials.head())
