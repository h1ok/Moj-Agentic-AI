# 🧩 X Profile Editor (Flask + Playwright)

أداة ويب + API لتعديل بروفايل حساب **X (Twitter سابقًا)** تلقائيًا باستخدام Playwright.

يدعم النظام:

- تعديل الاسم (Name)
- تعديل البايو (Bio)
- تعديل الموقع الجغرافي (Location)
- تعديل الموقع الإلكتروني (Website)
- رفع صورة البروفايل (Avatar)
- رفع صورة الهيدر (Banner)
- التشغيل عبر واجهة ويب
- التشغيل عبر API خارجي

---

# 🚀 المتطلبات

- Python 3.9+
- Google Chrome أو Chromium
- Playwright
- Flask

---

# 📦 التثبيت

داخل مجلد المشروع نفذ:

pip install flask playwright requests  
playwright install

---

# ▶️ تشغيل السيرفر

python app_profile_editor_v3.py

بعد التشغيل افتح المتصفح:

http://127.0.0.1:5789

---

# 🔐 إنشاء ملف المصادقة (auth.json)

أنشئ ملف التخزين من Playwright:

playwright codegen --save-storage=auth.json https://x.com

- سجل دخولك يدويًا مرة واحدة
- أغلق المتصفح
- سيتم إنشاء ملف auth.json

استخدم هذا الملف دائمًا في الواجهة أو API.

---

# 🌐 واجهة الويب

من الواجهة يمكنك:

- رفع auth.json
- إدخال الاسم والبايو والموقع
- رفع الصور أو وضع روابط مباشرة
- اختيار وضع المتصفح (مرئي / مخفي)
- تنفيذ التعديل بزر واحد

---

# ⚙️ استخدام الـ API

Endpoint:

POST /api/profile

---

# 🔑 التوثيق (Authorization)

كل طلب API يحتاج Header:

Authorization: Bearer your-secure-token-here

---

# 📡 مثال API بدون صور

import requests

url = "http://127.0.0.1:5789/api/profile"  
headers = {"Authorization": "Bearer your-secure-token-here"}  

files = {"cookies_file": open("auth.json", "rb")}  

data = {
    "name": "سيدي ابو عساف",
    "bio": "مرحبا",
    "location": "الرياض",
    "website": "https://google.com",
    "headless": "0"
}

r = requests.post(url, headers=headers, files=files, data=data, timeout=600)  
print(r.status_code, r.text)

---

# 🖼️ مثال API مع الصور

files = {
    "cookies_file": open("auth.json", "rb"),
    "avatar_file": open("avatar.jpg", "rb"),
    "banner_file": open("banner.jpg", "rb"),
}

---

# 🧪 فحص حالة السيرفر

GET /api/health

---

# ✅ جاهز للإنتاج

- دعم عربي + إنجليزي
- API Token Protection
- واجهة ويب + API
- رفع ملفات وصور
- معالجة الأخطاء
