from typing import Any, Optional
import json

class BaseCacheService:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.base_prefix = ""

    def build_key(self, key: str) -> str:
        return f"{self.base_prefix}:{key}"

    async def get(self, key: str) -> Optional[Any]:
        data = await self.redis.get(self.build_key(key))
        return json.loads(data) if data else None

    async def set(self, key: str, value: Any, ttl: int = 300):
        data = json.dumps(value, default=str)
        await self.redis.set(
            self.build_key(key), 
            data, 
            ex=ttl
        )