import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT email, is_admin, is_active FROM users WHERE email = 'saudallosh@gmail.com'")
result = cursor.fetchone()

print("=" * 60)
print("حالة المستخدم في قاعدة البيانات:")
print("=" * 60)
if result:
    print(f"البريد الإلكتروني: {result[0]}")
    print(f"صلاحيات المسؤول (is_admin): {result[1]} {'✅' if result[1] == 1 else '❌'}")
    print(f"الحساب نشط (is_active): {result[2]} {'✅' if result[2] == 1 else '❌'}")
else:
    print("❌ المستخدم غير موجود")

conn.close()

print("\n" + "=" * 60)
print("الحل:")
print("=" * 60)
if result and result[1] == 1:
    print("✅ الصلاحيات صحيحة في قاعدة البيانات")
    print("\nيجب عليك:")
    print("1. فتح Console في المتصفح (F12)")
    print("2. كتابة: localStorage.clear()")
    print("3. إعادة تحميل الصفحة (F5)")
    print("4. تسجيل الدخول مرة أخرى")
    print("\nأو ببساطة:")
    print("- سجل خروج من النظام")
    print("- سجل دخول مرة أخرى")
else:
    print("❌ الصلاحيات غير صحيحة - سيتم تحديثها الآن...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_admin = 1 WHERE email = 'saudallosh@gmail.com'")
    conn.commit()
    conn.close()
    print("✅ تم التحديث - سجل خروج ودخول مرة أخرى")

print("=" * 60)
