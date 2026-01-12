#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import httpx
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

async def test_decode():
    """اختبار فك تشفير Token"""
    
    print("=" * 60)
    print("🔍 اختبار فك تشفير Token")
    print("=" * 60)
    
    # الحصول على SECRET_KEY من البيئة
    secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-change-in-production-min-32-chars")
    print(f"\nSECRET_KEY من .env: {secret_key[:30]}...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # تسجيل الدخول
        login_response = await client.post(
            "http://localhost:8000/api/auth/login",
            json={"email": "test@example.com", "password": "test1234"}
        )
        
        if login_response.status_code != 200:
            print(f"❌ فشل تسجيل الدخول")
            return
        
        token = login_response.json()["access_token"]
        print(f"\n✅ Token: {token[:50]}...")
        
        # محاولة فك التشفير بدون التحقق
        print("\n1️⃣ فك التشفير بدون التحقق")
        try:
            payload_unverified = jwt.decode(token, options={"verify_signature": False})
            print(f"Payload: {payload_unverified}")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        
        # محاولة فك التشفير مع التحقق
        print("\n2️⃣ فك التشفير مع التحقق باستخدام SECRET_KEY من .env")
        try:
            payload_verified = jwt.decode(token, secret_key, algorithms=["HS256"])
            print(f"✅ Payload: {payload_verified}")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        
        # اختبار مع مفاتيح مختلفة
        print("\n3️⃣ اختبار مع المفتاح الافتراضي")
        try:
            default_key = "your-secret-key-here-change-in-production-min-32-chars"
            payload_default = jwt.decode(token, default_key, algorithms=["HS256"])
            print(f"✅ Payload مع المفتاح الافتراضي: {payload_default}")
        except Exception as e:
            print(f"❌ خطأ مع المفتاح الافتراضي: {e}")

if __name__ == "__main__":
    asyncio.run(test_decode())
