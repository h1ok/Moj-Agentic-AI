import requests

url = "http://127.0.0.1:5789/api/profile"
headers = {"Authorization": "Bearer your-secure-token-here"}

files = {
    "cookies_file": open("xx1.json", "rb"),
}

data = {
    "name": "",
    "bio": "مرحبا",
    "location": "الرياض",
    "website": "https://google.com",
    "avatar_url": "https://tweetdelete.net/resources/wp-content/uploads/2024/04/craig-whitehead-lbekri_riMg-unsplash.jpg",
    "banner_url": "https://example.com/banner.jpg",
    "headless": "0",
}

r = requests.post(url, headers=headers, files=files, data=data, timeout=600)
print(r.status_code, r.text)
