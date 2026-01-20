import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

print("⏳ بدء عملية النشر...")
start_time = time.time()

session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

headers = {
    "Authorization": "Bearer your-secure-token-here",
    "Content-Type": "application/json"
}

data = {
    "cookies_url": "http://127.0.0.1/up/xx.json",
    "text": "تغريدة جديدة",
    "media_url": "https://example.com/video.mp4",
    "headless": False
}

try:
    response = session.post(
        "http://localhost:5000/api/post", #وضع ip السيرفر
        headers=headers,
        json=data,
        timeout=(30, 600)
    )

    response.raise_for_status()
    print("✅ تم النشر بنجاح")
    print(response.json())

except Exception as e:
    print("❌ خطأ:", e)

finally:
    session.close()
    print(f"⏱️ الزمن الكلي: {time.time() - start_time:.2f} ثانية")
