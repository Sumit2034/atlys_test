from typing import Optional
from beanie import Document, Insert, Replace, Update, after_event
from pydantic import BaseModel
from bson import ObjectId

from app.models.time_stamps import TimeStamps


class Product(BaseModel):
    name: str
    price: float
    image: str

    class Config:
        json_encoders = {ObjectId: str}

    
class ProductDocument(Document, Product, TimeStamps):

    class Settings:
        name = "products"

    @classmethod
    async def get_by_name(cls, name: str) -> Optional['ProductDocument']:
        return await cls.find_one({"name": name})
    

    @after_event(Insert, Replace, Update)
    async def set_cache(cls):
        from app.main import product_cache
        value = {
            "id": str(cls.id),
            "name": cls.name,
            "price": cls.price,
            "image": cls.image
        }
        await product_cache.set_product_cache(cls.name, value=value)

    

