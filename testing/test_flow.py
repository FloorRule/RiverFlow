import requests

WORKFLOW_ID = "e99cc1ec-2bce-4d39-9ed3-70a92b1b396a" #! <- replace with flow ID
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
