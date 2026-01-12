#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import httpx

async def test_complete_flow():
    """اختبار التدفق الكامل من التسجيل إلى جلب البيانات"""
    
    print("=" * 60)
    print("🧪 اختبار التدفق الكامل")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. تسجيل حساب جديد
        print("\n1️⃣ تسجيل حساب جديد")
        print("-" * 60)
        
        register_response = await client.post(
            "http://localhost:8000/api/auth/register",
            json={
                "email": "newuser@test.com",
                "password": "test12345"
            }
        )
        
        print(f"Status: {register_response.status_code}")
        
        if register_response.status_code == 200:
            print("✅ تسجيل الحساب نجح!")
            register_token = register_response.json()["access_token"]
            print(f"Token: {register_token[:30]}...")
            
            # 2. جلب بيانات المستخدم بعد التسجيل
            print("\n2️⃣ جلب بيانات المستخدم بعد التسجيل")
            print("-" * 60)
            
            me_response = await client.get(
                "http://localhost:8000/api/auth/me",
                headers={"Authorization": f"Bearer {register_token}"}
            )
            
            print(f"Status: {me_response.status_code}")
            
            if me_response.status_code == 200:
                user_data = me_response.json()
                print(f"✅ جلب البيانات نجح!")
                print(f"User ID: {user_data['id']}")
                print(f"Email: {user_data['email']}")
            else:
                print(f"❌ فشل جلب البيانات: {me_response.json()}")
                return
        else:
            print(f"❌ فشل التسجيل: {register_response.json()}")
            return
        
        # 3. تسجيل الخروج
        print("\n3️⃣ تسجيل الخروج")
        print("-" * 60)
        
        logout_response = await client.post(
            "http://localhost:8000/api/auth/logout",
            headers={"Authorization": f"Bearer {register_token}"}
        )
        
        print(f"Status: {logout_response.status_code}")
        if logout_response.status_code == 200:
            print("✅ تسجيل الخروج نجح!")
        
        # 4. تسجيل الدخول مرة أخرى
        print("\n4️⃣ تسجيل الدخول مرة أخرى")
        print("-" * 60)
        
        login_response = await client.post(
            "http://localhost:8000/api/auth/login",
            json={
                "email": "newuser@test.com",
                "password": "test12345"
            }
        )
        
        print(f"Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ تسجيل الدخول نجح!")
            login_token = login_response.json()["access_token"]
            print(f"Token: {login_token[:30]}...")
            
            # 5. جلب بيانات المستخدم بعد تسجيل الدخول
            print("\n5️⃣ جلب بيانات المستخدم بعد تسجيل الدخول")
            print("-" * 60)
            
            me_response2 = await client.get(
                "http://localhost:8000/api/auth/me",
                headers={"Authorization": f"Bearer {login_token}"}
            )
            
            print(f"Status: {me_response2.status_code}")
            
            if me_response2.status_code == 200:
                user_data2 = me_response2.json()
                print(f"✅ جلب البيانات نجح!")
                print(f"User ID: {user_data2['id']}")
                print(f"Email: {user_data2['email']}")
                
                print("\n" + "=" * 60)
                print("🎉 جميع الاختبارات نجحت!")
                print("=" * 60)
            else:
                print(f"❌ فشل جلب البيانات: {me_response2.json()}")
        else:
            print(f"❌ فشل تسجيل الدخول: {login_response.json()}")

if __name__ == "__main__":
    asyncio.run(test_complete_flow())
