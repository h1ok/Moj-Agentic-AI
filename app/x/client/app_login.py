from playwright.sync_api import sync_playwright
import random
import time
import csv
from datetime import datetime
from pathlib import Path
import re


class TwitterLoginAdvanced:

    def create_stealth_firefox_context(self, browser, proxy_config=None):
        """إنشاء سياق Firefox مع إعدادات متقدمة"""
        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "locale": "ar-SA",
            "timezone_id": "Asia/Riyadh",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "extra_http_headers": {
                "Accept-Language": "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "TE": "trailers"
            }
        }

        if proxy_config:
            context_options["proxy"] = {
                "server": proxy_config["server"],
                "username": proxy_config.get("username"),
                "password": proxy_config.get("password")
            }

        return browser.new_context(**context_options)

    def inject_firefox_stealth(self, page):
        """سكريبتات إخفاء خاصة بـ Firefox"""
        stealth_js = """
        () => {
            delete Object.getPrototypeOf(navigator).webdriver;

            if (navigator.getBattery) {
                const originalGetBattery = navigator.getBattery;
                navigator.getBattery = function() {
                    return originalGetBattery.call(navigator).then((battery) => {
                        Object.defineProperty(battery, 'charging', { value: true });
                        Object.defineProperty(battery, 'chargingTime', { value: 0 });
                        Object.defineProperty(battery, 'dischargingTime', { value: Infinity });
                        Object.defineProperty(battery, 'level', { value: 0.85 + Math.random() * 0.1 });
                        return battery;
                    });
                };
            }

            if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
                const originalEnumerateDevices = navigator.mediaDevices.enumerateDevices;
                navigator.mediaDevices.enumerateDevices = function() {
                    return originalEnumerateDevices.call(navigator.mediaDevices).then((devices) => {
                        return devices.concat([
                            { deviceId: "default", kind: "audioinput", label: "Default - Microphone", groupId: "abc123" },
                            { deviceId: "communications", kind: "audiooutput", label: "Communications - Speakers", groupId: "def456" }
                        ]);
                    });
                };
            }

            const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel(R) UHD Graphics 630';
                return originalGetParameter.call(this, parameter);
            };

            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {
                const context = this.getContext('2d');
                if (context) {
                    const imageData = context.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        imageData.data[i] = imageData.data[i] + Math.floor(Math.random() * 3) - 1;
                    }
                    context.putImageData(imageData, 0, 0);
                }
                return originalToDataURL.apply(this, arguments);
            };

            Object.defineProperty(window.performance, 'timing', {
                get: () => ({
                    connectEnd: performance.timeOrigin + 10 + Math.random() * 50,
                    connectStart: performance.timeOrigin + 5 + Math.random() * 30,
                    domainLookupEnd: performance.timeOrigin + 8 + Math.random() * 40,
                    domainLookupStart: performance.timeOrigin + 3 + Math.random() * 20,
                    fetchStart: performance.timeOrigin + 2 + Math.random() * 10,
                    navigationStart: performance.timeOrigin,
                    redirectEnd: 0,
                    redirectStart: 0,
                    requestStart: performance.timeOrigin + 12 + Math.random() * 60,
                    responseEnd: performance.timeOrigin + 200 + Math.random() * 100,
                    responseStart: performance.timeOrigin + 150 + Math.random() * 80,
                    secureConnectionStart: performance.timeOrigin + 7 + Math.random() * 35,
                    unloadEventEnd: 0,
                    unloadEventStart: 0
                })
            });
        }
        """
        page.add_init_script(stealth_js)

    def human_actions(self, page):
        """إجراءات بشرية طبيعية"""
        for _ in range(random.randint(3, 6)):
            x = random.randint(100, 1800)
            y = random.randint(100, 1000)
            page.mouse.move(x, y, steps=random.randint(10, 30))
            time.sleep(random.uniform(0.2, 0.5))

        page.evaluate("window.scrollTo({top: Math.random() * 200, behavior: 'smooth'});")
        time.sleep(random.uniform(1, 2))

    def type_like_human(self, element, text):
        """كتابة بشرية طبيعية"""
        element.click()
        time.sleep(random.uniform(0.5, 1.5))

        for char in text:
            element.type(char, delay=random.randint(80, 200))
            if random.random() < 0.01:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.type(wrong_char, delay=random.randint(50, 100))
                time.sleep(random.uniform(0.1, 0.3))
                element.press('Backspace')
                time.sleep(random.uniform(0.1, 0.2))

            if random.random() < 0.15:
                time.sleep(random.uniform(0.3, 1.0))

    def check_login_success(self, page):
        """فحص متعدد للتأكد من نجاح تسجيل الدخول"""
        print("🔍 فحص نجاح تسجيل الدخول...")

        time.sleep(5)

        current_url = page.url
        print(f"📍 الرابط الحالي: {current_url}")

        checks = []

        if "home" in current_url or current_url.startswith("https://x.com/home"):
            checks.append(True)
            print("   ✓ الرابط يحتوي على /home")
        elif "login" not in current_url and "flow" not in current_url:
            checks.append(True)
            print("   ✓ الرابط لا يحتوي على login/flow")
        else:
            checks.append(False)
            print("   ✗ الرابط لا يزال في صفحة تسجيل الدخول")

        try:
            tweet_button = page.locator('[data-testid="SideNav_NewTweet_Button"]')
            if tweet_button.is_visible(timeout=3000):
                checks.append(True)
                print("   ✓ وجد زر التغريدة الجديدة")
            else:
                checks.append(False)
        except Exception:
            checks.append(False)
            print("   ✗ لم يجد زر التغريدة")

        cookies = page.context.cookies()
        auth_token_found = any(cookie.get('name') == 'auth_token' for cookie in cookies)
        if auth_token_found:
            checks.append(True)
            print("   ✓ وجد auth_token في الكوكيز")
        else:
            checks.append(False)
            print("   ✗ لم يجد auth_token")

        try:
            account_menu = page.locator('[data-testid="AppTabBar_Profile_Link"]')
            if account_menu.is_visible(timeout=3000):
                checks.append(True)
                print("   ✓ وجد قائمة الحساب")
            else:
                checks.append(False)
        except Exception:
            checks.append(False)
            print("   ✗ لم يجد قائمة الحساب")

        success_count = sum(checks)
        print(f"\n📊 نتيجة الفحص: {success_count}/4 فحوصات نجحت")

        return success_count >= 2

    @staticmethod
    def _safe_cookie_filename(username: str) -> str:
        """يحوّل اسم المستخدم إلى اسم ملف آمن: username.json (وإن كان username ينتهي بـ .json يتركه)"""
        u = (username or "").strip()
        if not u:
            return "unknown.json"
        # إزالة @ لو كانت موجودة
        if u.startswith("@"):
            u = u[1:]
        # اسم ملف آمن
        u = re.sub(r'[\\/:*?"<>|\s]+', "_", u)
        if not u.lower().endswith(".json"):
            u = f"{u}.json"
        return u

    def login_twitter(self, username, password, proxy_config=None, cookies_dir="cookies"):
        """تسجيل دخول متقدم + حفظ الكوكيز باسم الحساب"""
        cookies_dir = Path(cookies_dir)
        cookies_dir.mkdir(parents=True, exist_ok=True)
        cookie_path = cookies_dir / self._safe_cookie_filename(username)

        with sync_playwright() as p:
            browser = p.firefox.launch(
                headless=False,
                firefox_user_prefs={
                    "toolkit.telemetry.enabled": False,
                    "toolkit.telemetry.unified": False,
                    "toolkit.telemetry.archive.enabled": False,
                    "webgl.disabled": False,
                    "dom.webdriver.enabled": False,
                    "useAutomationExtension": False,
                    "privacy.donottrackheader.enabled": True,
                    "intl.accept_languages": "ar-SA, ar, en-US, en",
                    "network.prefetch-next": False,
                    "network.dns.disablePrefetch": True,
                    "network.predictor.enabled": False,
                }
            )

            context = self.create_stealth_firefox_context(browser, proxy_config)
            page = context.new_page()
            self.inject_firefox_stealth(page)

            try:
                print(f"\n{'='*60}\n👤 الحساب: {username}\n{'='*60}")
                print("🔄 الانتقال إلى صفحة تسجيل الدخول...")
                page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded")
                time.sleep(random.uniform(3, 5))

                self.human_actions(page)

                print("✍️ إدخال اسم المستخدم...")
                username_input = page.locator('input[autocomplete="username"]')
                username_input.wait_for(state="visible", timeout=15000)
                self.type_like_human(username_input, username)

                time.sleep(random.uniform(1.5, 3))

                print("👆 النقر على زر التالي...")
                try:
                    next_button = page.get_by_role("button", name="Next")
                    next_button.click()
                except Exception:
                    next_button = page.locator('button:has-text("Next")')
                    if not next_button.is_visible():
                        next_button = page.locator('button:has-text("التالي")')
                    next_button.first.click()

                time.sleep(random.uniform(3, 5))

                # فحص التحقق الإضافي
                try:
                    verification_input = page.locator('input[data-testid="ocfEnterTextTextInput"]')
                    if verification_input.is_visible(timeout=3000):
                        print("⚠️ يطلب تحقق إضافي!")
                        print("💡 أدخل المعلومات يدوياً في المتصفح...")
                        #input("⏸️ اضغط Enter بعد الإدخال...")
                except Exception:
                    pass

                print("🔐 إدخال كلمة المرور...")
                password_input = page.locator('input[type="password"]')
                password_input.wait_for(state="visible", timeout=15000)
                self.type_like_human(password_input, password)

                time.sleep(random.uniform(2, 4))

                print("🚀 تسجيل الدخول...")
                try:
                    login_button = page.locator('button[data-testid="LoginForm_Login_Button"]')
                    login_button.click()
                except Exception:
                    login_button = page.get_by_role("button", name="Log in")
                    if not login_button.is_visible():
                        login_button = page.get_by_role("button", name="تسجيل الدخول")
                    login_button.click()

                print("⏳ انتظار اكتمال تسجيل الدخول...")
                time.sleep(8)

                if self.check_login_success(page):
                    print("\n✅ تم تسجيل الدخول بنجاح!")

                    print("\n📂 فتح تاب جديد...")
                    new_page = context.new_page()
                    self.inject_firefox_stealth(new_page)

                    print("🌐 الانتقال إلى x.com...")
                    new_page.goto("https://x.com", wait_until="domcontentloaded")

                    print("⏳ الانتظار 30 ثانية...")
                    for i in range(30, 0, -5):
                        print(f"   ⏱️  {i} ثانية متبقية...")
                        time.sleep(5)

                    print(f"\n💾 حفظ الكوكيز في: {cookie_path}")
                    context.storage_state(path=str(cookie_path))
                    print("✅ تم حفظ الجلسة!")

                    cookies = context.cookies()
                    print(f"📦 تم حفظ {len(cookies)} كوكي")

                    auth_cookie = next((c for c in cookies if c.get('name') == 'auth_token'), None)
                    if auth_cookie:
                        print(f"🔑 auth_token موجود: {auth_cookie.get('value','')[:20]}...")

                    browser.close()
                    return True
                else:
                    print("\n❌ فشل تسجيل الدخول")
                    page.screenshot(path=f"login_failed_{self._safe_cookie_filename(username).replace('.json','')}.png", full_page=True)
                    print("📸 تم حفظ screenshot للفشل")

                    print("\n⏸️ إذا كنت مسجل دخول فعلياً:")
                    #choice = input("   اكتب 'نعم' لحفظ الكوكيز أو Enter للإغلاق: ")

                    if choice.lower() in ['نعم', 'yes', 'y']:
                        print("\n💾 حفظ الكوكيز...")

                        new_page = context.new_page()
                        self.inject_firefox_stealth(new_page)
                        new_page.goto("https://x.com", wait_until="domcontentloaded")

                        print("⏳ انتظار 30 ثانية...")
                        for i in range(30, 0, -5):
                            print(f"   ⏱️  {i} ثانية...")
                            time.sleep(5)

                        context.storage_state(path=str(cookie_path))
                        print(f"✅ تم حفظ الجلسة في: {cookie_path}")

                        browser.close()
                        return True

                    browser.close()
                    return False

            except Exception as e:
                print(f"\n❌ خطأ: {e}")
                try:
                    page.screenshot(path=f"error_{self._safe_cookie_filename(username).replace('.json','')}.png", full_page=True)
                    print("📸 تم حفظ screenshot للخطأ")
                except Exception:
                    pass

                print("\n⏸️ سيبقى المتصفح مفتوحاً للتحقق...")
                #input("اضغط Enter للإغلاق...")
                browser.close()
                return False


def load_accounts(csv_path: str):
    """قراءة accounts.csv بصيغة: username,password (مع تجاهل الصفوف الفارغة)"""
    accounts = []
    p = Path(csv_path)
    if not p.exists():
        raise FileNotFoundError(f"لم يتم العثور على الملف: {csv_path}")

    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        # يدعم أيضاً أسماء أعمدة بديلة إن وجدت
        for i, row in enumerate(reader, start=2):
            if not row:
                continue
            u = (row.get("username") or row.get("user") or row.get("email") or "").strip()
            pw = (row.get("password") or row.get("pass") or row.get("pwd") or "").strip()
            if not u or not pw:
                continue
            accounts.append({"username": u, "password": pw})

    return accounts


def append_problem_account(problem_csv: str, username: str, password: str, reason: str):
    """إضافة حساب إلى ملف مشاكل (يُنشأ تلقائياً مع هيدر)."""
    p = Path(problem_csv)
    is_new = not p.exists()
    with p.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["username", "password", "reason", "timestamp"])
        writer.writerow([username, password, reason, datetime.now().isoformat(timespec="seconds")])


# الاستخدام
if __name__ == "__main__":
    bot = TwitterLoginAdvanced()

    print("=" * 60)
    print("🔐 بوت تسجيل الدخول إلى Twitter/X (قراءة الحسابات من accounts.csv)")
    print("=" * 60)
    print("\n⚠️ تأكد من تشغيل VPN قبل البدء\n")

    ACCOUNTS_CSV = "accounts.csv"      # ضع ملفك هنا
    COOKIES_DIR = "cookies"           # سيتم حفظ الكوكيز داخله باسم كل حساب

    PROXY_CONFIG = None

    accounts = load_accounts(ACCOUNTS_CSV)
    if not accounts:
        print(f"⚠️ لا توجد حسابات في {ACCOUNTS_CSV} (تأكد أن الملف يحتوي username,password).")
        raise SystemExit(0)

    print(f"📄 تم تحميل {len(accounts)} حساب/حسابات من {ACCOUNTS_CSV}\n")

    ok = 0
    fail = 0

    PROBLEM_CSV = "problem_accounts.csv"  # سيتم إنشاء هذا الملف للحسابات التي فشلت

    for idx, acc in enumerate(accounts, start=1):
        username = acc["username"]
        password = acc["password"]
        print(f"\n🧾 ({idx}/{len(accounts)}) بدء حساب: {username}")

        success = bot.login_twitter(username, password, PROXY_CONFIG, cookies_dir=COOKIES_DIR)

        # تحقق من وجود ملف الكوكيز حتى لو رجع success=True
        expected_cookie = Path(COOKIES_DIR) / bot._safe_cookie_filename(username)
        cookie_ok = expected_cookie.exists() and expected_cookie.stat().st_size > 0

        if success and cookie_ok:
            ok += 1
        else:
            fail += 1
            reason = []
            if not success:
                reason.append("login_failed")
            if not cookie_ok:
                reason.append("cookie_not_saved")
            append_problem_account(PROBLEM_CSV, username, password, "+".join(reason) or "unknown")
            print(f"⚠️ تم تسجيل الحساب ضمن المشاكل في: {PROBLEM_CSV}")

        # تهدئة بسيطة بين الحسابات لتقليل الاشتباه
        time.sleep(random.uniform(5, 12))

    print("\n" + "=" * 60)
    print(f"✅ اكتمل: نجاح {ok} | فشل {fail} | الإجمالي {len(accounts)}")
    print(f"📁 ملفات الكوكيز داخل: {COOKIES_DIR}/")
    print("📄 الحسابات التي بها مشكلة (إن وُجدت): problem_accounts.csv")
    print("=" * 60)
