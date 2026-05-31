import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANAKIN_API_KEY")

def get_medical_context(symptoms):

    url = "https://anakin.io/v1/wire/task"

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "action_id": "pm_search_articles",
        "params": {
            "query": symptoms,
            "max_results": 3,
            "page": 1,
            "sort": "",
            "min_date": "",
            "max_date": "",
            "date_type": ""
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()
