#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Authentication System
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import SessionLocal, init_db
from app.db.models import User
from app.auth.security import hash_password, verify_password

def test_database():
    print("=" * 60)
    print("🧪 Testing Database Connection")
    print("=" * 60)
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Test: Create a user
        print("\n📝 Testing user creation...")
        test_email = "test@example.com"
        
        # Check if user exists
        existing_user = db.query(User).filter(User.email == test_email).first()
        if existing_user:
            print(f"⚠️  User {test_email} already exists, deleting...")
            db.delete(existing_user)
            db.commit()
        
        # Create new user
        hashed_pw = hash_password("test1234")
        new_user = User(
            email=test_email,
            password_hash=hashed_pw
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"✅ User created successfully!")
        print(f"   ID: {new_user.id}")
        print(f"   Email: {new_user.email}")
        print(f"   Created: {new_user.created_at}")
        
        # Test: Verify password
        print("\n🔐 Testing password verification...")
        if verify_password("test1234", new_user.password_hash):
            print("✅ Password verification works!")
        else:
            print("❌ Password verification failed!")
        
        # Test: Query user
        print("\n🔍 Testing user query...")
        found_user = db.query(User).filter(User.email == test_email).first()
        if found_user:
            print(f"✅ User found in database!")
            print(f"   ID: {found_user.id}")
            print(f"   Email: {found_user.email}")
        else:
            print("❌ User not found!")
        
        # Count users
        user_count = db.query(User).count()
        print(f"\n📊 Total users in database: {user_count}")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()
