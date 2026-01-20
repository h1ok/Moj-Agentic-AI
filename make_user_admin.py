#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Make specific user admin
"""
import sqlite3
import os

def make_user_admin():
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Make saudallosh@gmail.com admin
        cursor.execute("UPDATE users SET is_admin = 1 WHERE email = ?", ('saudallosh@gmail.com',))
        conn.commit()
        
        print("✅ User saudallosh@gmail.com is now an admin!")
        
        # Show all admins
        cursor.execute("SELECT id, email, name FROM users WHERE is_admin = 1")
        admins = cursor.fetchall()
        
        print("\n👑 Admin users:")
        for admin in admins:
            print(f"  - ID: {admin[0]}, Email: {admin[1]}, Name: {admin[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    make_user_admin()
