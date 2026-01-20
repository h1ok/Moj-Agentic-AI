import requests

BASE_URL = "http://127.0.0.1:5000"
TOKEN = "change-me-token"

payload = {
    "username": "user@example.com",
    "password": "your_password",
    "headless": False
}

response = requests.post(
    f"{BASE_URL}/api/login",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=300
)

print("Status:", response.status_code)
print(response.json())
