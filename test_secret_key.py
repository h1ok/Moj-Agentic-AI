#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.auth.security import SECRET_KEY, create_access_token, decode_token
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔑 فحص SECRET_KEY")
print("=" * 60)

# SECRET_KEY من security.py
print(f"\nSECRET_KEY من security.py: {SECRET_KEY}")

# SECRET_KEY من .env
env_key = os.getenv("JWT_SECRET_KEY")
print(f"JWT_SECRET_KEY من .env: {env_key}")

# إنشاء token
print("\n" + "=" * 60)
print("🔐 إنشاء وفك تشفير Token")
print("=" * 60)

token_data = {"sub": 1, "email": "test@example.com"}
token = create_access_token(token_data)

print(f"\nToken تم إنشاؤه: {token[:50]}...")

# فك التشفير
decoded = decode_token(token)
if decoded:
    print(f"\n✅ Token تم فك تشفيره بنجاح!")
    print(f"User ID: {decoded.user_id}")
    print(f"Email: {decoded.email}")
else:
    print(f"\n❌ فشل فك تشفير Token")
