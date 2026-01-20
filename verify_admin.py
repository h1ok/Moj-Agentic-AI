import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update user to admin
cursor.execute("UPDATE users SET is_admin = 1 WHERE email = 'saudallosh@gmail.com'")
conn.commit()

# Verify
cursor.execute("SELECT id, email, is_admin, is_active FROM users WHERE email = 'saudallosh@gmail.com'")
user = cursor.fetchone()

print("=" * 70)
print("تحديث صلاحيات المستخدم - User Permissions Update")
print("=" * 70)

if user:
    print(f"\n✅ تم تحديث المستخدم بنجاح!")
    print(f"\nالبريد الإلكتروني: {user[1]}")
    print(f"صلاحيات المسؤول: {'نعم ✅' if user[2] == 1 else 'لا ❌'}")
    print(f"الحساب نشط: {'نعم ✅' if user[3] == 1 else 'لا ❌'}")
else:
    print("\n❌ المستخدم غير موجود")

# Show all admins
print("\n" + "=" * 70)
print("جميع المسؤولين في النظام:")
print("=" * 70)
cursor.execute("SELECT id, email, name FROM users WHERE is_admin = 1")
admins = cursor.fetchall()

for admin in admins:
    print(f"👑 {admin[1]} (الاسم: {admin[2] or 'غير محدد'})")

conn.close()

print("\n" + "=" * 70)
print("الخطوات التالية:")
print("=" * 70)
print("1. سجل خروج من النظام")
print("2. سجل دخول مرة أخرى بنفس الحساب")
print("3. اضغط على اسمك في الشريط الجانبي")
print("4. ستجد خيار 'لوحة التحكم الإدارية' 👑")
print("5. أو اذهب مباشرة إلى: http://localhost:3000/admin")
print("=" * 70)
