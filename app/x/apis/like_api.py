import requests

url = "http://localhost:5789/api/like"
headers = {"Authorization": "Bearer your-secure-token-here"}

data = {
    "cookie_label": "mualqahtani1",
    "tweet_url": "https://x.com/H_swilhy/status/2014494805686898908",
    "headless": False,
    "wait_after_ms": 2000
}

r = requests.post(url, headers=headers, json=data, timeout=600)
print(r.status_code, r.text)
