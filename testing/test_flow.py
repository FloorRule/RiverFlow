import requests

WORKFLOW_ID = "73f0a49e-5fb7-46be-929b-f016efbbc19b" #! <- replace with flow ID
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
