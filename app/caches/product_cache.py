from app.caches.redis_cache import RedisCache


class ProductCache(RedisCache):
    prefix = "product:"

    async def set_product_cache(self, key, value):
        final_key = self.prefix+key
        await self.set(key=final_key, value=value)
    
    async def get_product_cache(self, key):
        final_key = self.prefix+key
        return await self.get(key=final_key)