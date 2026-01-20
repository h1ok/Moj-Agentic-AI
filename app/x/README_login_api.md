# X / Twitter Login API – Python Client

## 📌 الوصف
هذا المشروع يحتوي على سكربت Python بسيط لإرسال طلب API إلى سيرفر محلي مسؤول عن:
- تسجيل الدخول إلى حساب X (Twitter)
- حفظ الكوكيز باسم الحساب
- إرجاع نتيجة العملية (نجاح / فشل + مسار ملف الكوكيز)

السكربت مناسب للاستخدام في الأتمتة (Automation) أو كجزء من نظام Back-end.

---

## 🧱 المتطلبات
- Python 3.8 أو أحدث
- مكتبة requests

### تثبيت المتطلبات
```bash
pip install requests
```

- سيرفر API يعمل على العنوان:
```
http://127.0.0.1:5000
```

---

## 🔐 الحماية
يستخدم الـ API آلية Bearer Token للحماية.
يجب أن تكون قيمة TOKEN مطابقة للقيمة المعرفة داخل السيرفر.

---

## 📂 كود العميل (Client)

```python
import requests

BASE_URL = "http://127.0.0.1:5000"
TOKEN = "change-me-token"

payload = {
    "username": "user@example.com",
    "password": "your_password",
    "headless": False
}

r = requests.post(
    f"{BASE_URL}/api/login",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=300
)

print("Status:", r.status_code)
print(r.json())
```

---

## 🧩 شرح المتغيرات

| المتغير | الوصف |
|------|------|
| BASE_URL | عنوان سيرفر الـ API |
| TOKEN | مفتاح التحقق (Bearer Token) |
| username | اسم المستخدم أو البريد |
| password | كلمة المرور |
| headless | تشغيل المتصفح بدون واجهة (True / False) |

---

## ⚙️ إعدادات اختيارية

### تحديد مجلد حفظ الكوكيز
```python
"cookies_dir": "cookies"
```

### استخدام Proxy
```python
"proxy": {
    "server": "http://proxy:port",
    "username": "proxy_user",
    "password": "proxy_pass"
}
```

---

## 📤 مثال استجابة ناجحة
```json
{
  "success": true,
  "username": "user@example.com",
  "cookie_path": "cookies/user.json",
  "duration_sec": 42.3
}
```

---

## 📤 مثال استجابة فاشلة
```json
{
  "success": false,
  "username": "user@example.com",
  "reason": "login_failed",
  "cookie_saved": false
}
```

---

## ⏱️ المهلة الزمنية
تم تعيين مهلة الطلب إلى 300 ثانية لأن عملية تسجيل الدخول عبر Playwright قد تستغرق وقتًا.

---
