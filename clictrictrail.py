import requests

url = "https://clinicaltrials.gov/api/v2/studies?query.term=diabetes&limit=5"
headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    studies = data.get("studies", [])
    for study in studies:
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        nct_id = identification.get("nctId", "N/A")
        title = identification.get("briefTitle", "N/A")
        print(f"ID: {nct_id}")
        print(f"Title: {title}")
        print("-" * 40)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")