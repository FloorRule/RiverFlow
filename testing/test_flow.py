import requests

WORKFLOW_ID = "81154394-47cb-40be-a6f5-86b642aadc59" #! <- replace with flow ID
WEBHOOK_URL = f"http://localhost:8000/hooks/{WORKFLOW_ID}"

payload = {
    "email": "test@example.com",
    "country": "IL",
    "age_list": [21, 10]
}

res = requests.post(WEBHOOK_URL, json=payload, timeout=35)

print("Status:", res.status_code)
print("Response:")
print(res.json())
