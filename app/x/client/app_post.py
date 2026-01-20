import os
import re
import uuid
import time
import mimetypes
import tempfile
from pathlib import Path
from typing import Optional
from functools import wraps

import requests
from flask import Flask, request, render_template_string, redirect, url_for, flash, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

app = Flask(__name__)
app.secret_key = "change-me"

# API Configuration
API_TOKENS = {
    "your-secure-token-here": "admin",  # استبدل هذا بـ token آمن
}

def require_api_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({"error": "Missing Authorization header"}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        if token not in API_TOKENS:
            return jsonify({"error": "Invalid token"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>X Poster | أداة النشر الذكية</title>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary-blue: #1DA1F2;
      --dark-blue: #0d8bd9;
      --light-blue: #e8f5fe;
      --gray-50: #f8f9fa;
      --gray-100: #e9ecef;
      --gray-200: #dee2e6;
      --gray-300: #ced4da;
      --gray-600: #6c757d;
      --gray-800: #343a40;
      --white: #ffffff;
      --shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: 'Tajawal', system-ui, -apple-system, sans-serif;
      background: linear-gradient(135deg, var(--light-blue) 0%, var(--gray-50) 100%);
      min-height: 100vh;
      padding: 20px;
    }
    
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
    
    .header {
      background: var(--white);
      padding: 30px;
      border-radius: 16px;
      box-shadow: var(--shadow-lg);
      margin-bottom: 30px;
      text-align: center;
      border-top: 4px solid var(--primary-blue);
    }
    
    .header h1 {
      color: var(--gray-800);
      font-size: 32px;
      font-weight: 700;
      margin-bottom: 8px;
    }
    
    .header .subtitle {
      color: var(--gray-600);
      font-size: 16px;
      font-weight: 400;
    }
    
    .card {
      background: var(--white);
      padding: 35px;
      border-radius: 16px;
      box-shadow: var(--shadow-lg);
      margin-bottom: 20px;
    }
    
    .form-group {
      margin-bottom: 24px;
    }
    
    label {
      display: block;
      color: var(--gray-800);
      font-weight: 500;
      margin-bottom: 8px;
      font-size: 15px;
    }
    
    input[type="text"],
    input[type="url"],
    input[type="file"],
    textarea,
    select {
      width: 100%;
      padding: 12px 16px;
      border: 2px solid var(--gray-200);
      border-radius: 10px;
      font-size: 15px;
      font-family: inherit;
      transition: all 0.3s ease;
      background: var(--white);
    }
    
    input[type="text"]:focus,
    input[type="url"]:focus,
    textarea:focus,
    select:focus {
      outline: none;
      border-color: var(--primary-blue);
      box-shadow: 0 0 0 3px rgba(29, 161, 242, 0.1);
    }
    
    input[type="file"] {
      padding: 10px;
      cursor: pointer;
    }
    
    textarea {
      resize: vertical;
      min-height: 120px;
      line-height: 1.6;
    }
    
    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }
    
    .hint {
      color: var(--gray-600);
      font-size: 13px;
      margin-top: 6px;
      line-height: 1.4;
    }
    
    button[type="submit"] {
      width: 100%;
      background: linear-gradient(135deg, var(--primary-blue) 0%, var(--dark-blue) 100%);
      color: var(--white);
      padding: 16px 24px;
      border: none;
      border-radius: 12px;
      font-size: 18px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 4px 12px rgba(29, 161, 242, 0.3);
      margin-top: 10px;
    }
    
    button[type="submit"]:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(29, 161, 242, 0.4);
    }
    
    button[type="submit"]:active {
      transform: translateY(0);
    }
    
    .messages {
      list-style: none;
      margin-bottom: 20px;
    }
    
    .messages li {
      padding: 16px 20px;
      background: var(--light-blue);
      border: 1px solid var(--primary-blue);
      border-radius: 10px;
      color: var(--gray-800);
      margin-bottom: 10px;
      animation: slideIn 0.3s ease;
    }
    
    .messages li.error {
      background: #fee;
      border-color: #fcc;
      color: #c33;
    }
    
    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateY(-10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    .api-info {
      background: var(--gray-50);
      padding: 20px;
      border-radius: 12px;
      border-right: 4px solid var(--primary-blue);
      margin-top: 20px;
    }
    
    .api-info h3 {
      color: var(--gray-800);
      font-size: 18px;
      margin-bottom: 12px;
    }
    
    .api-info code {
      background: var(--white);
      padding: 3px 8px;
      border-radius: 4px;
      color: var(--dark-blue);
      font-size: 13px;
      border: 1px solid var(--gray-200);
    }
    
    .api-info pre {
      background: var(--white);
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      margin-top: 12px;
      border: 1px solid var(--gray-200);
      font-size: 12px;
    }
    
    .api-section {
      margin-bottom: 20px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--gray-200);
    }
    
    .api-section:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }
    
    @media (max-width: 768px) {
      .row {
        grid-template-columns: 1fr;
      }
      
      .header h1 {
        font-size: 24px;
      }
      
      .card {
        padding: 20px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🚀 X Poster</h1>
      <p class="subtitle">أداة ذكية لنشر التغريدات مع الميديا بسهولة</p>
    </div>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class="messages">
          {% for m in messages %}
            <li>{{m}}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <div class="card">
      <form method="POST" enctype="multipart/form-data">
        <div class="form-group">
          <label>📁 ملف الكوكيز (storage_state.json)</label>
          <input type="file" name="cookies_file" accept=".json" required />
          <div class="hint">ارفع ملف الكوكيز المحفوظ من متصفحك</div>
        </div>

        <div class="form-group">
          <label>✍️ نص التغريدة</label>
          <textarea name="text" placeholder="اكتب تغريدتك هنا..." required></textarea>
        </div>

        <div class="row">
          <div class="form-group">
            <label>🔗 رابط ميديا (اختياري)</label>
            <input type="url" name="media_url" placeholder="https://example.com/image.jpg" />
            <div class="hint">سيتم تنزيل الملف ورفعه تلقائياً</div>
          </div>
          <div class="form-group">
            <label>📤 أو ارفع ملف ميديا</label>
            <input type="file" name="media_file" />
            <div class="hint">صورة أو فيديو من جهازك</div>
          </div>
        </div>

        <div class="form-group">
          <label>👁️ وضع المتصفح</label>
          <select name="headless">
            <option value="0">عرض المتصفح (مرئي)</option>
            <option value="1">إخفاء المتصفح (Headless)</option>
          </select>
        </div>

        <button type="submit">🚀 نشر التغريدة الآن</button>
      </form>
    </div>

    <div class="card api-info">
      <h3>📡 استخدام API</h3>
      
      <div class="api-section">
        <p style="color: var(--gray-600); margin-bottom: 12px;">
          <strong>Endpoint:</strong> <code>POST /api/post</code>
        </p>
        <p style="color: var(--gray-600); margin-bottom: 12px;">
          <strong>Authentication:</strong> <code>Authorization: Bearer your-secure-token-here</code>
        </p>
      </div>

      <div class="api-section">
        <p style="color: var(--gray-800); font-weight: 500; margin-bottom: 10px;">📋 الطريقة الأولى: رابط الكوكيز JSON</p>
        <pre>curl -X POST http://localhost:5000/api/post \
  -H "Authorization: Bearer your-secure-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "cookies_url": "https://example.com/storage_state.json",
    "text": "تغريدة من API",
    "media_url": "https://example.com/image.jpg",
    "headless": true
  }'</pre>
      </div>

      <div class="api-section">
        <p style="color: var(--gray-800); font-weight: 500; margin-bottom: 10px;">📤 الطريقة الثانية: رفع ملف مباشر</p>
        <pre>curl -X POST http://localhost:5000/api/post \
  -H "Authorization: Bearer your-secure-token-here" \
  -F "cookies_file=@storage_state.json" \
  -F "text=تغريدة من API" \
  -F "media_file=@image.jpg" \
  -F "headless=1"</pre>
      </div>

      <div class="api-section">
        <p style="color: var(--gray-800); font-weight: 500; margin-bottom: 10px;">🐍 مثال Python</p>
        <pre>import requests

headers = {
    "Authorization": "Bearer your-secure-token-here",
    "Content-Type": "application/json"
}

data = {
    "cookies_url": "https://example.com/storage_state.json",
    "text": "تغريدة جديدة",
    "media_url": "https://example.com/image.jpg",
    "headless": True
}

response = requests.post(
    "http://localhost:5000/api/post",
    headers=headers,
    json=data
)

print(response.json())</pre>
      </div>
    </div>
  </div>
</body>
</html>
"""

def is_url(s: str) -> bool:
    return bool(re.match(r"^https?://", (s or "").strip(), re.I))

def guess_ext_from_url_or_ct(url: str, content_type: Optional[str]) -> str:
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if ext:
            return ext
    path = Path(url.split("?")[0])
    if path.suffix:
        return path.suffix
    return ".bin"

def download_to_temp(url: str, folder: str) -> str:
    """تنزيل ملف من رابط URL إلى مجلد مؤقت"""
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, stream=True, timeout=120, headers=headers, allow_redirects=True)
    r.raise_for_status()
    ext = guess_ext_from_url_or_ct(url, r.headers.get("Content-Type"))
    out_path = os.path.join(folder, f"media_{uuid.uuid4().hex}{ext}")
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)
    return out_path

def download_cookies_json(url: str, folder: str) -> str:
    """تنزيل ملف JSON الكوكيز من رابط"""
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, timeout=60, headers=headers, allow_redirects=True)
    r.raise_for_status()
    
    # التحقق من أنه JSON صالح
    try:
        r.json()
    except Exception:
        raise ValueError("الرابط لا يحتوي على JSON صالح")
    
    cookies_path = os.path.join(folder, "storage_state.json")
    with open(cookies_path, "wb") as f:
        f.write(r.content)
    
    return cookies_path

def _pick_composer_file_input(page):
    locator = page.locator('#layers input[type="file"][data-testid="fileInput"]')
    if locator.count() > 0:
        return locator.first

    locator = page.locator('#layers input[type="file"]')
    if locator.count() > 0:
        return locator.first

    locator = page.locator('input[type="file"][data-testid="fileInput"]')
    if locator.count() > 0:
        return locator.first

    return page.locator('input[type="file"]').first

def _wait_media_uploaded(page, timeout_ms: int = 180_000):
    deadline = time.time() + (timeout_ms / 1000.0)

    remove_btn = page.locator('#layers [aria-label="Remove"], #layers [aria-label="Remove media"], #layers [data-testid*="remove"]')
    progress = page.locator('#layers [role="progressbar"], #layers progress, #layers [data-testid*="progress"]')

    page.wait_for_timeout(800)

    while time.time() < deadline:
        if remove_btn.count() > 0:
            if progress.count() == 0:
                return True

            try:
                if progress.is_visible():
                    page.wait_for_timeout(500)
                    continue
                return True
            except Exception:
                return True

        preview = page.locator('#layers [data-testid="attachments"], #layers [data-testid*="attachment"], #layers img, #layers video')
        if preview.count() > 0 and progress.count() == 0:
            return True

        page.wait_for_timeout(500)

    raise TimeoutError("انتهت مهلة انتظار رفع الميديا.")

def post_to_x(storage_state_path: str, text: str, media_path: Optional[str], headless: bool):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=headless
        )

        context = browser.new_context(storage_state=storage_state_path)
        page = context.new_page()

        page.goto("https://x.com/home", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        page.get_by_test_id("SideNav_NewTweet_Button").click()
        page.wait_for_timeout(1500)

        textbox = page.get_by_role("textbox", name="Post text")
        textbox.wait_for(state="visible", timeout=20_000)

        if media_path:
            file_input = _pick_composer_file_input(page)
            file_input.wait_for(state="attached", timeout=20_000)
            file_input.set_input_files(media_path)
            _wait_media_uploaded(page, timeout_ms=180_000)

        textbox.fill(text)

        page.get_by_test_id("tweetButton").click()
        page.wait_for_timeout(2500)

        context.close()
        browser.close()

def process_post_request(request_obj, tmp_dir):
    """معالجة طلب النشر (مشترك بين Web UI و API)"""
    if request_obj.content_type and 'multipart/form-data' in request_obj.content_type:
        cookies = request_obj.files.get("cookies_file")
        text = request_obj.form.get("text", "").strip()
        headless = request_obj.form.get("headless") == "1"
        media_url = request_obj.form.get("media_url", "").strip()
        media_file = request_obj.files.get("media_file")
    else:
        return None, "Invalid content type"

    if not cookies:
        return None, "ارفع ملف الكوكيز JSON"

    cookies_path = os.path.join(tmp_dir, "storage_state.json")
    cookies.save(cookies_path)

    if not text:
        return None, "اكتب نص التغريدة"

    media_path = None
    if media_file and media_file.filename:
        media_path = os.path.join(tmp_dir, media_file.filename)
        media_file.save(media_path)
    elif media_url and is_url(media_url):
        try:
            media_path = download_to_temp(media_url, tmp_dir)
        except Exception as e:
            return None, f"فشل تنزيل الميديا: {e}"

    try:
        post_to_x(cookies_path, text, media_path, headless=headless)
        return True, "تمت محاولة النشر بنجاح ✅"
    except Exception as e:
        return None, f"فشل النشر: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(HTML)

    with tempfile.TemporaryDirectory() as tmp_dir:
        success, message = process_post_request(request, tmp_dir)
        flash(message)

    return redirect(url_for("index"))

@app.route("/api/post", methods=["POST"])
@require_api_token
def api_post():
    """
    API Endpoint للنشر على X
    
    يدعم طريقتين:
    
    1) JSON body مع روابط:
    {
        "cookies_url": "https://example.com/storage_state.json",
        "text": "نص التغريدة",
        "media_url": "https://example.com/image.jpg",  (اختياري)
        "headless": true
    }
    
    2) multipart/form-data مع ملفات:
        - cookies_file: ملف JSON
        - text: نص التغريدة
        - media_file: ملف ميديا (اختياري)
        - headless: 0 أو 1
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        # تحديد نوع الطلب
        is_json = request.is_json
        
        if is_json:
            # الطريقة الأولى: JSON مع روابط
            data = request.get_json()
            
            cookies_url = data.get("cookies_url", "").strip()
            text = data.get("text", "").strip()
            media_url = data.get("media_url", "").strip()
            headless = data.get("headless", True)
            
            if not cookies_url:
                return jsonify({
                    "success": False,
                    "error": "يجب تقديم cookies_url"
                }), 400
            
            if not is_url(cookies_url):
                return jsonify({
                    "success": False,
                    "error": "cookies_url يجب أن يكون رابط صالح"
                }), 400
            
            if not text:
                return jsonify({
                    "success": False,
                    "error": "يجب تقديم نص التغريدة"
                }), 400
            
            # تنزيل ملف الكوكيز
            try:
                cookies_path = download_cookies_json(cookies_url, tmp_dir)
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": f"فشل تنزيل ملف الكوكيز: {str(e)}"
                }), 400
            
            # تنزيل الميديا إن وُجدت
            media_path = None
            if media_url and is_url(media_url):
                try:
                    media_path = download_to_temp(media_url, tmp_dir)
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "error": f"فشل تنزيل الميديا: {str(e)}"
                    }), 400
            
            # تنفيذ النشر
            try:
                post_to_x(cookies_path, text, media_path, headless=headless)
                return jsonify({
                    "success": True,
                    "message": "تمت محاولة النشر بنجاح ✅"
                }), 200
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": f"فشل النشر: {str(e)}"
                }), 500
        
        else:
            # الطريقة الثانية: multipart/form-data
            success, message = process_post_request(request, tmp_dir)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": message
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "error": message
                }), 400

@app.route("/api/health", methods=["GET"])
def health_check():
    """فحص حالة API"""
    return jsonify({
        "status": "healthy",
        "service": "X Poster API",
        "version": "2.0"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5789, debug=True)
