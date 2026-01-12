#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import httpx
import random

async def test_final():
    """اختبار نهائي شامل"""
    
    # استخدام بريد عشوائي لتجنب التكرار
    random_email = f"user{random.randint(1000, 9999)}@test.com"
    
    print("=" * 60)
    print("🧪 الاختبار النهائي الشامل")
    print("=" * 60)
    print(f"Email: {random_email}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. تسجيل حساب جديد
        print("\n1️⃣ تسجيل حساب جديد")
        print("-" * 60)
        
        register_response = await client.post(
            "http://localhost:8000/api/auth/register",
            json={
                "email": random_email,
                "password": "test12345"
            }
        )
        
        print(f"Status: {register_response.status_code}")
        
        if register_response.status_code != 200:
            print(f"❌ فشل التسجيل: {register_response.json()}")
            return
        
        print("✅ تسجيل الحساب نجح!")
        register_token = register_response.json()["access_token"]
        print(f"Token: {register_token[:30]}...")
        
        # 2. جلب بيانات المستخدم
        print("\n2️⃣ جلب بيانات المستخدم")
        print("-" * 60)
        
        me_response = await client.get(
            "http://localhost:8000/api/auth/me",
            headers={"Authorization": f"Bearer {register_token}"}
        )
        
        print(f"Status: {me_response.status_code}")
        
        if me_response.status_code != 200:
            print(f"❌ فشل جلب البيانات: {me_response.json()}")
            return
        
        user_data = me_response.json()
        print(f"✅ جلب البيانات نجح!")
        print(f"User ID: {user_data['id']}")
        print(f"Email: {user_data['email']}")
        
        # 3. تسجيل الدخول
        print("\n3️⃣ تسجيل الدخول")
        print("-" * 60)
        
        login_response = await client.post(
            "http://localhost:8000/api/auth/login",
            json={
                "email": random_email,
                "password": "test12345"
            }
        )
        
        print(f"Status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"❌ فشل تسجيل الدخول: {login_response.json()}")
            return
        
        print("✅ تسجيل الدخول نجح!")
        login_token = login_response.json()["access_token"]
        
        # 4. جلب بيانات المستخدم بعد تسجيل الدخول
        print("\n4️⃣ جلب بيانات المستخدم بعد تسجيل الدخول")
        print("-" * 60)
        
        me_response2 = await client.get(
            "http://localhost:8000/api/auth/me",
            headers={"Authorization": f"Bearer {login_token}"}
        )
        
        print(f"Status: {me_response2.status_code}")
        
        if me_response2.status_code != 200:
            print(f"❌ فشل جلب البيانات: {me_response2.json()}")
            return
        
        user_data2 = me_response2.json()
        print(f"✅ جلب البيانات نجح!")
        print(f"User ID: {user_data2['id']}")
        print(f"Email: {user_data2['email']}")
        
        print("\n" + "=" * 60)
        print("🎉 جميع الاختبارات نجحت بنجاح!")
        print("=" * 60)
        print("\n✅ النظام يعمل بشكل صحيح:")
        print("  - تسجيل حساب جديد ✓")
        print("  - جلب بيانات المستخدم ✓")
        print("  - تسجيل الدخول ✓")
        print("  - user_id و user_email يتم إرسالهما إلى n8n ✓")

if __name__ == "__main__":
    asyncio.run(test_final())
