#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import httpx
from jose import jwt

async def test():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # تسجيل حساب جديد
        response = await client.post(
            "http://localhost:8000/api/auth/register",
            json={"email": "test2@test.com", "password": "test12345"}
        )
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"Token: {token[:50]}...")
            
            # فك التشفير بدون التحقق
            try:
                payload = jwt.decode(token, options={"verify_signature": False})
                print(f"\nPayload: {payload}")
                print(f"sub type: {type(payload.get('sub'))}")
                print(f"sub value: {payload.get('sub')}")
            except Exception as e:
                print(f"Error: {e}")

asyncio.run(test())
