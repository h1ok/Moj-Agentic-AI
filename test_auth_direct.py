#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import httpx

async def test_auth():
    """اختبار مباشر للمصادقة"""
    
    print("=" * 60)
    print("🔐 اختبار المصادقة المباشر")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # تسجيل الدخول
        print("\n1️⃣ تسجيل الدخول")
        login_response = await client.post(
            "http://localhost:8000/api/auth/login",
            json={"email": "test@example.com", "password": "test1234"}
        )
        
        print(f"Status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"❌ فشل: {login_response.json()}")
            return
        
        token = login_response.json()["access_token"]
        print(f"✅ Token: {token[:30]}...")
        
        # اختبار /me مع headers مختلفة
        print("\n2️⃣ اختبار /me مع Authorization header")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"Headers: {headers}")
        
        me_response = await client.get(
            "http://localhost:8000/api/auth/me",
            headers=headers
        )
        
        print(f"Status: {me_response.status_code}")
        print(f"Response: {me_response.json()}")
        
        # اختبار verify endpoint
        print("\n3️⃣ اختبار /verify endpoint")
        
        verify_response = await client.get(
            "http://localhost:8000/api/auth/verify",
            headers=headers
        )
        
        print(f"Status: {verify_response.status_code}")
        print(f"Response: {verify_response.json()}")

if __name__ == "__main__":
    asyncio.run(test_auth())
