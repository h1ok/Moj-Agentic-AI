#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add admin fields to database
"""
import sqlite3
import os

def update_database():
    print("=" * 60)
    print("🔧 Adding Admin Fields to Database")
    print("=" * 60)
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    print(f"📂 Database path: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current schema
        print("\n📋 Current users table schema:")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        existing_columns = [col[1] for col in columns]
        
        # Add is_admin column if it doesn't exist
        if 'is_admin' not in existing_columns:
            print("\n➕ Adding 'is_admin' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0 NOT NULL")
            print("✅ 'is_admin' column added successfully")
        else:
            print("\n✓ 'is_admin' column already exists")
        
        # Add is_active column if it doesn't exist
        if 'is_active' not in existing_columns:
            print("\n➕ Adding 'is_active' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL")
            print("✅ 'is_active' column added successfully")
        else:
            print("\n✓ 'is_active' column already exists")
        
        conn.commit()
        
        # Make first user admin
        print("\n👑 Setting first user as admin...")
        cursor.execute("UPDATE users SET is_admin = 1 WHERE id = (SELECT MIN(id) FROM users)")
        conn.commit()
        
        # Show admin users
        print("\n👥 Admin users:")
        cursor.execute("SELECT id, email, name, is_admin FROM users WHERE is_admin = 1")
        admins = cursor.fetchall()
        if admins:
            for admin in admins:
                print(f"  ID: {admin[0]}, Email: {admin[1]}, Name: {admin[2]}")
        else:
            print("  No admin users found")
        
        # Verify changes
        print("\n📋 Updated users table schema:")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Database updated successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_database()
