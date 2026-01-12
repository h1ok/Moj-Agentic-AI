#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import httpx

async def test_login():
    """اختبار تسجيل الدخول"""
    
    print("=" * 60)
    print("🧪 اختبار تسجيل الدخول")
    print("=" * 60)
    
    # اختبار 1: تسجيل الدخول بمستخدم موجود
    print("\n1️⃣ اختبار تسجيل الدخول بمستخدم موجود")
    print("-" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/auth/login",
                json={
                    "email": "test@example.com",
                    "password": "test1234"
                }
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ تسجيل الدخول نجح!")
                
                # اختبار جلب بيانات المستخدم
                token = response.json()["access_token"]
                print(f"\n2️⃣ اختبار جلب بيانات المستخدم")
                print("-" * 60)
                
                me_response = await client.get(
                    "http://localhost:8000/api/auth/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                print(f"Status Code: {me_response.status_code}")
                print(f"User Data: {me_response.json()}")
                
                if me_response.status_code == 200:
                    print("✅ جلب بيانات المستخدم نجح!")
                else:
                    print("❌ فشل جلب بيانات المستخدم")
            else:
                print("❌ فشل تسجيل الدخول")
                
        except Exception as e:
            print(f"❌ خطأ: {e}")
    
    # اختبار 2: تسجيل حساب جديد
    print("\n\n3️⃣ اختبار تسجيل حساب جديد")
    print("-" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "http://localhost:8000/api/auth/register",
                json={
                    "email": "newuser@example.com",
                    "password": "newpass123"
                }
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ تسجيل الحساب نجح!")
            elif response.status_code == 400:
                print("⚠️ الحساب موجود بالفعل")
            else:
                print("❌ فشل تسجيل الحساب")
                
        except Exception as e:
            print(f"❌ خطأ: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_login())
