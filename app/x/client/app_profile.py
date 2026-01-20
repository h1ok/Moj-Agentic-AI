
import os
import re
import uuid
import mimetypes
import tempfile
from pathlib import Path
from typing import Optional, List, Tuple
from functools import wraps

import requests
from flask import Flask, request, render_template_string, redirect, url_for, flash, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me")

API_TOKENS = {
    "your-secure-token-here": "admin",
}

def require_api_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "")
        if not token:
            return jsonify({"error": "Missing Authorization header"}), 401
        if token.startswith("Bearer "):
            token = token[7:]
        if token not in API_TOKENS:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated

HTML = """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>X Profile Editor | تعديل البروفايل</title>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    :root{--primary:#1DA1F2;--bg1:#e8f5fe;--bg2:#f8f9fa;--text:#343a40;--muted:#6c757d;--border:#dee2e6;--white:#fff;--shadow:0 4px 16px rgba(0,0,0,.12);--shadow2:0 2px 8px rgba(0,0,0,.08)}
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Tajawal',system-ui,-apple-system,sans-serif;background:linear-gradient(135deg,var(--bg1),var(--bg2));min-height:100vh;padding:20px;color:var(--text)}
    .container{max-width:900px;margin:0 auto}
    .header{background:var(--white);padding:28px 30px;border-radius:16px;box-shadow:var(--shadow);border-top:4px solid var(--primary);text-align:center;margin-bottom:18px}
    .header h1{font-size:28px;font-weight:800;margin-bottom:6px}
    .header p{color:var(--muted)}
    .card{background:var(--white);padding:26px;border-radius:16px;box-shadow:var(--shadow2);margin-bottom:16px}
    .messages{list-style:none;margin-bottom:12px}
    .messages li{padding:14px 16px;border-radius:10px;background:#e8f5fe;border:1px solid var(--primary);margin-bottom:8px}
    .messages li.error{background:#fee;border-color:#fcc;color:#a00}
    .form-group{margin-bottom:18px}
    label{display:block;font-weight:600;margin-bottom:8px}
    input[type="text"], input[type="url"], input[type="file"], textarea, select{width:100%;padding:12px 14px;border:2px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;outline:none;transition:.2s;background:var(--white)}
    textarea{min-height:100px;resize:vertical;line-height:1.7}
    input:focus, textarea:focus, select:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(29,161,242,.12)}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
    .hint{margin-top:6px;color:var(--muted);font-size:12px;line-height:1.5}
    .btn{width:100%;border:none;cursor:pointer;padding:14px 16px;border-radius:12px;font-weight:800;font-size:16px;color:var(--white);background:linear-gradient(135deg,var(--primary),#0d8bd9);box-shadow:0 6px 18px rgba(29,161,242,.28);transition:.2s;margin-top:6px}
    .btn:hover{transform:translateY(-1px);box-shadow:0 10px 22px rgba(29,161,242,.32)}
    .small{font-size:12px;color:var(--muted);margin-top:10px}
    code{background:#f1f3f5;border:1px solid var(--border);padding:2px 6px;border-radius:6px}
    @media (max-width:780px){.row{grid-template-columns:1fr}.header h1{font-size:22px}}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🧩 X Profile Editor</h1>
      <p>تعديل الاسم والبايو والموقع + رفع صورة البروفايل والهيدر عبر Playwright</p>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <ul class="messages">
          {% for cat, m in messages %}
            <li class="{{cat}}">{{m}}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}

    <div class="card">
      <form method="POST" enctype="multipart/form-data">
        <div class="form-group">
          <label>📁 ملف الكوكيز (storage_state.json)</label>
          <input type="file" name="cookies_file" accept=".json" required />
          <div class="hint">يفضل ملف مولّد من Playwright عبر: <code>playwright codegen --save-storage=auth.json https://x.com</code></div>
        </div>

        <div class="row">
          <div class="form-group">
            <label>👤 الاسم (Name)</label>
            <input type="text" name="name" placeholder="مثال: mu alqahtani" />
          </div>
          <div class="form-group">
            <label>📍 الموقع الجغرافي (Location)</label>
            <input type="text" name="location" placeholder="مثال: الرياض" />
          </div>
        </div>

        <div class="form-group">
          <label>📝 النبذة (Bio)</label>
          <textarea name="bio" placeholder="اكتب البايو هنا..."></textarea>
        </div>

        <div class="form-group">
          <label>🌐 الموقع الإلكتروني (Website) (اختياري)</label>
          <input type="url" name="website" placeholder="https://example.com" />
        </div>

        <div class="row">
          <div class="form-group">
            <label>🖼️ صورة البروفايل (Avatar) - رابط (اختياري)</label>
            <input type="url" name="avatar_url" placeholder="https://example.com/avatar.jpg" />
          </div>
          <div class="form-group">
            <label>📤 أو ارفع صورة البروفايل (Avatar)</label>
            <input type="file" name="avatar_file" accept="image/*" />
          </div>
        </div>

        <div class="row">
          <div class="form-group">
            <label>🧱 صورة الهيدر (Banner) - رابط (اختياري)</label>
            <input type="url" name="banner_url" placeholder="https://example.com/banner.jpg" />
          </div>
          <div class="form-group">
            <label>📤 أو ارفع صورة الهيدر (Banner)</label>
            <input type="file" name="banner_file" accept="image/*" />
          </div>
        </div>

        <div class="form-group">
          <label>👁️ وضع المتصفح</label>
          <select name="headless">
            <option value="0">مرئي (أفضل للتجربة)</option>
            <option value="1">مخفي Headless</option>
          </select>
        </div>

        <button type="submit" class="btn">✅ تنفيذ تعديل البروفايل</button>
        <p class="small">API: <code>POST /api/profile</code> مع <code>Authorization: Bearer your-secure-token-here</code></p>
      </form>
    </div>
  </div>
</body>
</html>
"""

def is_url(s: str) -> bool:
    return bool(re.match(r"^https?://", (s or "").strip(), re.I))

def guess_ext(content_type: Optional[str], url: str) -> str:
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if ext:
            return ext
    p = Path(url.split("?")[0])
    return p.suffix if p.suffix else ".bin"

def download_to_temp(url: str, folder: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, stream=True, timeout=120, headers=headers, allow_redirects=True)
    r.raise_for_status()
    ext = guess_ext(r.headers.get("Content-Type"), url)
    out_path = os.path.join(folder, f"media_{uuid.uuid4().hex}{ext}")
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)
    return out_path

def _file_inputs_in_edit_dialog(page):
    loc = page.locator("#layers input[type='file']")
    if loc.count() > 0:
        return loc
    return page.locator("input[type='file']")

def _try_click_by_patterns(page, patterns: List[str]) -> bool:
    for pat in patterns:
        try:
            btn = page.get_by_role("button", name=re.compile(pat, re.I))
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=8000)
                return True
        except Exception:
            pass
    return False

def _try_click_banner_button(page) -> bool:
    patterns = [
        r"Add banner photo", r"Add header photo", r"Header photo", r"Banner",
        r"إضافة.*(صورة|صوره).*(غلاف|بانر|بنر|هيدر|رأس|عنوان)",
        r"(صورة|صوره).*(غلاف|بانر|بنر|هيدر|رأس|عنوان)"
    ]
    return _try_click_by_patterns(page, patterns)

def _try_click_avatar_button(page) -> bool:
    patterns = [
        r"Add avatar photo", r"Add profile photo", r"Profile photo", r"Avatar",
        r"إضافة.*(صورة|صوره).*(الملف|بروفايل|شخصية|شخصيه)",
        r"(صورة|صوره).*(الملف|بروفايل|شخصية|شخصيه)"
    ]
    return _try_click_by_patterns(page, patterns)

def _handle_crop_if_any(page):
    names = ["Apply","Save","Done","Next","تطبيق","حفظ","تم","التالي","إنهاء","قص","تأكيد"]
    for n in names:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(n)}$", re.I))
            if b.count() > 0 and b.first.is_visible():
                b.first.click(timeout=6000)
                page.wait_for_timeout(600)
                return True
        except Exception:
            pass
    for sel in ["[data-testid='applyButton']", "[data-testid='ocfApplyButton']"]:
        try:
            el = page.locator(sel)
            if el.count() > 0 and el.first.is_visible():
                el.first.click(timeout=6000)
                page.wait_for_timeout(600)
                return True
        except Exception:
            pass
    return False

def _ensure_logged_in_or_raise(page):
    page.wait_for_timeout(1000)
    for txt in ["Log in", "تسجيل الدخول", "Login"]:
        try:
            if page.get_by_role("link", name=re.compile(txt, re.I)).count() > 0:
                raise RuntimeError("لم يتم تسجيل الدخول بالكوكيز. استخدم storage_state مولّد من Playwright عبر --save-storage.")
        except Exception:
            continue

def _fill_first_match(page, candidates: List[Tuple[str, str]], value: str):
    if not value:
        return
    last_err = None
    for kind, sel in candidates:
        try:
            if kind == "css":
                loc = page.locator(sel)
                if loc.count() > 0:
                    loc.first.fill(value, timeout=8000)
                    return
            elif kind == "role":
                loc = page.get_by_role("textbox", name=re.compile(sel, re.I))
                if loc.count() > 0:
                    loc.first.fill(value, timeout=8000)
                    return
        except Exception as e:
            last_err = e
    if last_err:
        raise last_err

def update_profile_on_x(
    storage_state_path: str,
    name: str,
    bio: str,
    location: str,
    website: str,
    avatar_path: Optional[str],
    banner_path: Optional[str],
    headless: bool,
):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=headless)
        context = browser.new_context(storage_state=storage_state_path)
        page = context.new_page()

        page.goto("https://x.com/home", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        _ensure_logged_in_or_raise(page)

        page.get_by_test_id("AppTabBar_Profile_Link").click(timeout=30_000)
        page.wait_for_timeout(1500)

        page.get_by_test_id("editProfileButton").click(timeout=30_000)
        page.wait_for_timeout(1500)

        # ===== رفع الصور =====
        inputs = _file_inputs_in_edit_dialog(page)

        if banner_path:
            _try_click_banner_button(page)
            page.wait_for_timeout(400)
            if inputs.count() >= 1:
                inputs.nth(0).set_input_files(banner_path)
            else:
                page.locator("input[type='file']").first.set_input_files(banner_path)
            page.wait_for_timeout(1200)
            _handle_crop_if_any(page)

        if avatar_path:
            _try_click_avatar_button(page)
            page.wait_for_timeout(400)
            if inputs.count() >= 2:
                inputs.nth(1).set_input_files(avatar_path)
            elif inputs.count() == 1:
                inputs.first.set_input_files(avatar_path)
            else:
                page.locator("input[type='file']").first.set_input_files(avatar_path)
            page.wait_for_timeout(1200)
            _handle_crop_if_any(page)

        # ===== تعبئة الحقول (حل strict-mode) =====
        if name:
            _fill_first_match(page, [
                ("css", "input[name='displayName']"),
                ("role", r"^Name\b"),
                ("role", r"^الاسم\b"),
            ], name)

        if bio:
            try:
                loc = page.locator("textarea[name='description'], textarea")
                if loc.count() > 0:
                    loc.first.fill(bio, timeout=8000)
                else:
                    _fill_first_match(page, [("role", r"^Bio\b"), ("role", r"^النبذة|^نبذة|^نبذه")], bio)
            except Exception:
                _fill_first_match(page, [("role", r"^Bio\b"), ("role", r"^النبذة|^نبذة|^نبذه")], bio)

        if location:
            _fill_first_match(page, [
                ("css", "input[name='location']"),
                ("role", r"الموقع الجغرافي"),
                ("role", r"^Location\b"),
            ], location)

        if website:
            _fill_first_match(page, [
                ("css", "input[name='url']"),
                ("role", r"الموقع الإلكتروني"),
                ("role", r"(Website|URL|Link)\b"),
            ], website)

        page.get_by_test_id("Profile_Save_Button").click(timeout=30_000)
        page.wait_for_timeout(2500)

        context.close()
        browser.close()

def _save_uploaded(file_storage, dst_path: str):
    file_storage.save(dst_path)
    return dst_path

def process_profile_request(req, tmp_dir: str):
    if not (req.content_type and "multipart/form-data" in req.content_type):
        return False, "Invalid content type"

    cookies = req.files.get("cookies_file")
    if not cookies:
        return False, "ارفع ملف الكوكيز (storage_state.json)"

    cookies_path = os.path.join(tmp_dir, "storage_state.json")
    cookies.save(cookies_path)

    name = (req.form.get("name") or "").strip()
    bio = (req.form.get("bio") or "").strip()
    location = (req.form.get("location") or "").strip()
    website = (req.form.get("website") or "").strip()
    headless = (req.form.get("headless") == "1")

    avatar_url = (req.form.get("avatar_url") or "").strip()
    banner_url = (req.form.get("banner_url") or "").strip()
    avatar_file = req.files.get("avatar_file")
    banner_file = req.files.get("banner_file")

    avatar_path = None
    banner_path = None

    if avatar_file and avatar_file.filename:
        avatar_path = os.path.join(tmp_dir, avatar_file.filename)
        _save_uploaded(avatar_file, avatar_path)
    elif avatar_url and is_url(avatar_url):
        avatar_path = download_to_temp(avatar_url, tmp_dir)

    if banner_file and banner_file.filename:
        banner_path = os.path.join(tmp_dir, banner_file.filename)
        _save_uploaded(banner_file, banner_path)
    elif banner_url and is_url(banner_url):
        banner_path = download_to_temp(banner_url, tmp_dir)

    try:
        update_profile_on_x(
            storage_state_path=cookies_path,
            name=name,
            bio=bio,
            location=location,
            website=website,
            avatar_path=avatar_path,
            banner_path=banner_path,
            headless=headless,
        )
        return True, "تم تعديل البروفايل (أو تمت المحاولة) ✅"
    except Exception as e:
        return False, f"فشل تعديل البروفايل: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(HTML)

    with tempfile.TemporaryDirectory() as tmp_dir:
        ok, msg = process_profile_request(request, tmp_dir)
        flash(msg, "error" if not ok else "success")
    return redirect(url_for("index"))

@app.route("/api/profile", methods=["POST"])
@require_api_token
def api_profile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        ok, msg = process_profile_request(request, tmp_dir)
        if ok:
            return jsonify({"success": True, "message": msg}), 200
        return jsonify({"success": False, "error": msg}), 400

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "X Profile Editor", "version": "1.3"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5789"))
    app.run(host="0.0.0.0", port=port, debug=True)
