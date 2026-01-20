#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fix Database Schema - Add missing columns
"""
import sqlite3
import os

def fix_database():
    print("=" * 60)
    print("🔧 Fixing Database Schema")
    print("=" * 60)
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        print(f"💡 Make sure the backend has been run at least once to create the database")
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
        
        # Add name column if it doesn't exist
        if 'name' not in existing_columns:
            print("\n➕ Adding 'name' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR(255)")
            print("✅ 'name' column added successfully")
        else:
            print("\n✓ 'name' column already exists")
        
        # Add profile_picture column if it doesn't exist
        if 'profile_picture' not in existing_columns:
            print("\n➕ Adding 'profile_picture' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)")
            print("✅ 'profile_picture' column added successfully")
        else:
            print("\n✓ 'profile_picture' column already exists")
        
        conn.commit()
        
        # Verify changes
        print("\n📋 Updated users table schema:")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Show sample data
        print("\n📊 Sample user data:")
        cursor.execute("SELECT id, email, name, profile_picture FROM users LIMIT 3")
        users = cursor.fetchall()
        if users:
            for user in users:
                print(f"  ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Picture: {user[3]}")
        else:
            print("  No users found in database")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Database schema fixed successfully!")
        print("=" * 60)
        print("\n🔄 Please restart the backend server (python run.py)")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_database()
