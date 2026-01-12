#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import httpx
from app.auth.security import decode_token, SECRET_KEY

async def test_token_flow():
    """اختبار تدفق Token بالكامل"""
    
    print("=" * 60)
    print("🔍 اختبار Token Flow")
    print("=" * 60)
    print(f"SECRET_KEY: {SECRET_KEY[:30]}...")
    
    # الخطوة 1: تسجيل الدخول
    print("\n1️⃣ تسجيل الدخول")
    print("-" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "http://localhost:8000/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "test1234"
            }
        )
        
        if response.status_code != 200:
            print(f"❌ فشل تسجيل الدخول: {response.json()}")
            return
        
        token = response.json()["access_token"]
        print(f"✅ تم الحصول على Token")
        print(f"Token: {token[:50]}...")
        
        # الخطوة 2: فك تشفير Token محلياً
        print("\n2️⃣ فك تشفير Token محلياً")
        print("-" * 60)
        
        token_data = decode_token(token)
        if token_data:
            print(f"✅ Token صالح محلياً")
            print(f"User ID: {token_data.user_id}")
            print(f"Email: {token_data.email}")
        else:
            print("❌ Token غير صالح محلياً")
            return
        
        # الخطوة 3: اختبار /me endpoint
        print("\n3️⃣ اختبار /me endpoint")
        print("-" * 60)
        
        me_response = await client.get(
            "http://localhost:8000/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Status Code: {me_response.status_code}")
        print(f"Response: {me_response.json()}")
        
        if me_response.status_code == 200:
            print("✅ /me endpoint يعمل بنجاح!")
        else:
            print("❌ /me endpoint فشل")
            
            # اختبار إضافي: تحقق من headers
            print("\n4️⃣ تحقق من Headers المرسلة")
            print("-" * 60)
            print(f"Authorization Header: Bearer {token[:30]}...")

if __name__ == "__main__":
    asyncio.run(test_token_flow())
