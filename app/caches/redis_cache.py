import json
from typing import Optional
import aioredis

class RedisCache:

    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client: Optional[aioredis.Redis] = None
        self.host = host
        self.port = port
        self.db = db

    
    async def initialize(self, host='localhost', port=6379, db=0):
        self.redis_client = await aioredis.from_url(
            f"redis://{self.host}:{self.port}/{self.db}",
            encoding="utf-8",
            decode_responses=True
        )
    
    async def set(self, key, value, expiration=None):
        serialized_value = json.dumps(value)
        if expiration:
            await self.redis_client.setex(key, expiration, serialized_value)
        else:
            await self.redis_client.set(key, serialized_value)
    
    async def get(self, key):
        value = await self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def delete(self, key):
        await self.redis_client.delete(key)
    
    async def exists(self, key):
        return await self.redis_client.exists(key)
