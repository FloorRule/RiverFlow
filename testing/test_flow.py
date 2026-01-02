import requests

WORKFLOW_ID = "bb116869-4cb6-4eb3-8d74-191415bdf340" #! <- replace with flow ID
WEBHOOK_URL = f"http://localhost:8000/hooks/{WORKFLOW_ID}"

payload = {
    "email": "test@example.com",
    "country": "IL",
    "age_list": [9, 10]
}

res = requests.post(WEBHOOK_URL, json=payload, timeout=35)

print("Status:", res.status_code)
print("Response:")
print(res.json())
