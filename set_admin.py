import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Set saudallosh@gmail.com as admin
cursor.execute("UPDATE users SET is_admin = 1 WHERE email = 'saudallosh@gmail.com'")
conn.commit()

# Verify
cursor.execute("SELECT id, email, is_admin, is_active FROM users WHERE email = 'saudallosh@gmail.com'")
result = cursor.fetchone()

print("=" * 60)
print("Updated user:")
print(f"ID: {result[0]}")
print(f"Email: {result[1]}")
print(f"Is Admin: {result[2]} {'✅' if result[2] else '❌'}")
print(f"Is Active: {result[3]} {'✅' if result[3] else '❌'}")
print("=" * 60)

# Show all admins
cursor.execute("SELECT id, email FROM users WHERE is_admin = 1")
admins = cursor.fetchall()
print("\nAll admin users:")
for admin in admins:
    print(f"  👑 {admin[1]} (ID: {admin[0]})")

conn.close()
print("\n✅ Done! User must logout and login again to access admin panel.")
