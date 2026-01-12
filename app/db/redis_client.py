import redis
from typing import Optional
from app.core.config import settings


class RedisClient:
    _instance: Optional[redis.Redis] = None
    _connection_failed: bool = False
    
    @classmethod
    def get_client(cls) -> Optional[redis.Redis]:
        """Get Redis client instance (singleton)"""
        # If connection already failed, don't try again
        if cls._connection_failed:
            return None
            
        if cls._instance is None:
            try:
                cls._instance = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    decode_responses=True,
                    socket_connect_timeout=0.5,
                    socket_timeout=0.5
                )
                # Test connection
                cls._instance.ping()
            except Exception as e:
                print(f"⚠️  Redis not available: {e}")
                print("⚠️  Authentication will work without Redis (sessions won't be cached)")
                cls._instance = None
                cls._connection_failed = True
        return cls._instance
    
    @classmethod
    def set_session(cls, session_id: str, user_id: int, expires: int = 86400) -> bool:
        """Store session in Redis (default 24 hours)"""
        try:
            client = cls.get_client()
            if client:
                client.setex(f"session:{session_id}", expires, str(user_id))
                return True
            return False
        except Exception as e:
            print(f"Redis error setting session: {e}")
            return False
    
    @classmethod
    def get_session(cls, session_id: str) -> Optional[int]:
        """Get user_id from session"""
        try:
            client = cls.get_client()
            if client:
                user_id = client.get(f"session:{session_id}")
                return int(user_id) if user_id else None
            return None
        except Exception as e:
            print(f"Redis error getting session: {e}")
            return None
    
    @classmethod
    def delete_session(cls, session_id: str) -> bool:
        """Delete session from Redis"""
        try:
            client = cls.get_client()
            if client:
                client.delete(f"session:{session_id}")
                return True
            return False
        except Exception as e:
            print(f"Redis error deleting session: {e}")
            return False
    
    @classmethod
    def add_to_blacklist(cls, token: str, expires: int = 86400) -> bool:
        """Add JWT token to blacklist (for logout)"""
        try:
            client = cls.get_client()
            if client:
                client.setex(f"blacklist:{token}", expires, "1")
                return True
            return False
        except Exception as e:
            print(f"Redis error adding to blacklist: {e}")
            return False
    
    @classmethod
    def is_blacklisted(cls, token: str) -> bool:
        """Check if token is blacklisted"""
        try:
            client = cls.get_client()
            if client:
                return client.exists(f"blacklist:{token}") > 0
            return False
        except Exception as e:
            print(f"Redis error checking blacklist: {e}")
            return False
    
    @classmethod
    def test_connection(cls) -> bool:
        """Test Redis connection"""
        try:
            client = cls.get_client()
            client.ping()
            return True
        except Exception as e:
            print(f"Redis connection failed: {e}")
            return False
