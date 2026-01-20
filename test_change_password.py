#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Change Password API Endpoint
"""
import httpx
import asyncio

async def test_change_password():
    print("=" * 60)
    print("🧪 Testing Change Password API")
    print("=" * 60)
    
    # Step 1: Login first to get token
    login_url = "http://localhost:8000/api/auth/login"
    login_data = {
        "email": "test@example.com",
        "password": "test1234"
    }
    
    print(f"\n📤 Step 1: Logging in...")
    print(f"URL: {login_url}")
    print(f"Data: {login_data}")
    
    try:
        async with httpx.AsyncClient() as client:
            # Login
            login_response = await client.post(
                login_url,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\n📥 Login Response Status: {login_response.status_code}")
            
            if login_response.status_code != 200:
                print(f"❌ Login failed: {login_response.text}")
                return
            
            login_result = login_response.json()
            access_token = login_result.get("access_token")
            
            if not access_token:
                print("❌ No access token received")
                return
            
            print(f"✅ Login successful!")
            print(f"🔑 Token: {access_token[:50]}...")
            
            # Step 2: Change password
            change_password_url = "http://localhost:8000/api/auth/change-password"
            password_data = {
                "current_password": "test1234",
                "new_password": "newtest1234"
            }
            
            print(f"\n📤 Step 2: Changing password...")
            print(f"URL: {change_password_url}")
            print(f"Data: {password_data}")
            
            change_response = await client.post(
                change_password_url,
                json=password_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
            )
            
            print(f"\n📥 Change Password Response Status: {change_response.status_code}")
            print(f"📥 Response: {change_response.text}")
            
            if change_response.status_code == 200:
                print("\n✅ Password changed successfully!")
                
                # Step 3: Test login with new password
                print(f"\n📤 Step 3: Testing login with new password...")
                new_login_data = {
                    "email": "test@example.com",
                    "password": "newtest1234"
                }
                
                new_login_response = await client.post(
                    login_url,
                    json=new_login_data,
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"📥 New Login Response Status: {new_login_response.status_code}")
                
                if new_login_response.status_code == 200:
                    print("✅ Login with new password successful!")
                    
                    # Step 4: Change password back
                    print(f"\n📤 Step 4: Changing password back to original...")
                    new_token = new_login_response.json().get("access_token")
                    
                    restore_password_data = {
                        "current_password": "newtest1234",
                        "new_password": "test1234"
                    }
                    
                    restore_response = await client.post(
                        change_password_url,
                        json=restore_password_data,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {new_token}"
                        }
                    )
                    
                    if restore_response.status_code == 200:
                        print("✅ Password restored to original!")
                    else:
                        print(f"⚠️  Failed to restore password: {restore_response.text}")
                else:
                    print(f"❌ Login with new password failed: {new_login_response.text}")
            else:
                print(f"❌ Password change failed!")
                print(f"Error details: {change_response.json()}")
                
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_change_password())
