#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check and set admin status for users
"""
import sqlite3
import os

def check_admin_status():
    print("=" * 60)
    print("🔍 Checking Admin Status")
    print("=" * 60)
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    print(f"📂 Database path: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Show all users with their admin status
        print("\n👥 All users:")
        cursor.execute("SELECT id, email, name, is_admin, is_active FROM users")
        users = cursor.fetchall()
        
        if not users:
            print("  No users found")
        else:
            for user in users:
                admin_icon = "👑" if user[3] else "👤"
                active_icon = "✅" if user[4] else "❌"
                print(f"  {admin_icon} ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Admin: {user[3]}, Active: {active_icon}")
        
        # Ask which user to make admin
        print("\n" + "=" * 60)
        user_email = input("Enter email to make admin (or press Enter to skip): ").strip()
        
        if user_email:
            cursor.execute("UPDATE users SET is_admin = 1 WHERE email = ?", (user_email,))
            if cursor.rowcount > 0:
                conn.commit()
                print(f"✅ User {user_email} is now an admin!")
            else:
                print(f"❌ User {user_email} not found")
        
        # Show updated list
        print("\n👥 Updated admin users:")
        cursor.execute("SELECT id, email, name FROM users WHERE is_admin = 1")
        admins = cursor.fetchall()
        
        if admins:
            for admin in admins:
                print(f"  👑 ID: {admin[0]}, Email: {admin[1]}, Name: {admin[2]}")
        else:
            print("  No admin users found")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Done! Please log out and log in again to refresh your session.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_admin_status()
