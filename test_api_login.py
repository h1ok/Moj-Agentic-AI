#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Login API Endpoint
"""
import httpx
import asyncio

async def test_login_api():
    print("=" * 60)
    print("🧪 Testing Login API Endpoint")
    print("=" * 60)
    
    url = "http://localhost:8000/api/auth/login"
    
    # Test data
    login_data = {
        "email": "test@example.com",
        "password": "test1234"
    }
    
    print(f"\n📤 Sending POST request to: {url}")
    print(f"📝 Data: {login_data}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\n📥 Response Status: {response.status_code}")
            print(f"📥 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ Login successful!")
                print(f"📝 Response data: {data}")
                
                if "access_token" in data:
                    print(f"\n🔑 Access Token: {data['access_token'][:50]}...")
                    print("✅ Token received successfully!")
                else:
                    print("\n⚠️  No access_token in response!")
            else:
                print(f"\n❌ Login failed!")
                print(f"📝 Response: {response.text}")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_login_api())
