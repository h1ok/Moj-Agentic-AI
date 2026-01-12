#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from app.auth.dependencies import require_current_user
from app.db.database import SessionLocal
from fastapi.security import HTTPAuthorizationCredentials
from app.auth.security import create_access_token

async def test_require_user():
    """اختبار require_current_user مباشرة"""
    
    print("=" * 60)
    print("🔍 اختبار require_current_user")
    print("=" * 60)
    
    # إنشاء token
    token_data = {"sub": 1, "email": "test@example.com"}
    token = create_access_token(token_data)
    
    print(f"\nToken: {token[:50]}...")
    
    # محاولة استخدام require_current_user
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )
    
    db = SessionLocal()
    
    try:
        user = await require_current_user(credentials, db)
        print(f"\n✅ User found: {user.email}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_require_user())
