#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-here-change-in-production-min-32-chars"
ALGORITHM = "HS256"

print("=" * 60)
print("🔍 فحص JWT بشكل مباشر")
print("=" * 60)

# إنشاء token
data = {"sub": 1, "email": "test@example.com"}
expire = datetime.utcnow() + timedelta(hours=24)
to_encode = data.copy()
to_encode.update({"exp": expire, "iat": datetime.utcnow()})

token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
print(f"\nToken: {token[:50]}...")

# فك التشفير
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"\n✅ فك التشفير نجح!")
    print(f"Payload: {payload}")
except JWTError as e:
    print(f"\n❌ فك التشفير فشل: {e}")

# اختبار مع token من API
print("\n" + "=" * 60)
print("🔍 فحص token من API")
print("=" * 60)

import asyncio
import httpx

async def test_api_token():
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:8000/api/auth/login",
            json={"email": "test@example.com", "password": "test1234"}
        )
        
        if response.status_code == 200:
            api_token = response.json()["access_token"]
            print(f"\nAPI Token: {api_token[:50]}...")
            
            # فك التشفير بدون التحقق من التوقيع
            try:
                unverified = jwt.decode(api_token, options={"verify_signature": False})
                print(f"\nPayload (بدون تحقق): {unverified}")
            except Exception as e:
                print(f"\n❌ خطأ: {e}")
            
            # فك التشفير مع التحقق
            try:
                verified = jwt.decode(api_token, SECRET_KEY, algorithms=[ALGORITHM])
                print(f"\n✅ Payload (مع تحقق): {verified}")
            except JWTError as e:
                print(f"\n❌ فك التشفير فشل: {e}")

asyncio.run(test_api_token())
