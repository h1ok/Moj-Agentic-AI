#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Login System
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import SessionLocal
from app.db.models import User
from app.auth.security import verify_password

def test_login():
    print("=" * 60)
    print("🔐 Testing Login System")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Test credentials
        test_email = "test@example.com"
        test_password = "test1234"
        
        print(f"\n🔍 Looking for user: {test_email}")
        
        # Find user
        user = db.query(User).filter(User.email == test_email).first()
        
        if not user:
            print("❌ User not found in database!")
            print("\n📊 All users in database:")
            all_users = db.query(User).all()
            for u in all_users:
                print(f"   - {u.email} (ID: {u.id})")
            return
        
        print(f"✅ User found!")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Password Hash: {user.password_hash[:50]}...")
        
        # Test password verification
        print(f"\n🔐 Testing password: {test_password}")
        
        if verify_password(test_password, user.password_hash):
            print("✅ Password is CORRECT!")
            print("✅ Login should work!")
        else:
            print("❌ Password is INCORRECT!")
            print("❌ Login will fail!")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_login()
