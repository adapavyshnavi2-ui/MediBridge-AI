import requests
import time
import os

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
            "sort": "relevance",
            "min_date": "",
            "max_date": "",
            "date_type": "pdat"
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()


def get_job_result(poll_url):

    url = "https://anakin.io" + poll_url

    headers = {
        "X-API-Key": API_KEY
    }

    for i in range(30):  # increased from 10 to 30

        print(f"Checking attempt {i+1}")

        response = requests.get(url, headers=headers)

        data = response.json()

        print(data)

        if data.get("status") == "completed":
            return data

        if data.get("status") == "failed":
            return data

        time.sleep(3)  # slightly longer wait

    return data
