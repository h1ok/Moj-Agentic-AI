import requests

url = "http://localhost:5789/api/reply"
headers = {"Authorization": "Bearer your-secure-token-here"}

data = {
    "cookie_label": "mualqahtani1",
    "tweet_url": "https://x.com/H_swilhy/status/2014494805686898908",
    "reply_text": "مرحبا 👋",
    "headless": False,
    "wait_after_ms": 5000
}

r = requests.post(url, headers=headers, json=data, timeout=600)
print(r.status_code, r.text)
