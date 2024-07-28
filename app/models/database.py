from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import db_models
    
async def init_db():
    MONGO_DB_DATABASE_NAME = "atlys_test"
    MOTOR_CLIENT = AsyncIOMotorClient("mongodb://localhost:27017")
    DATABASE = MOTOR_CLIENT[MONGO_DB_DATABASE_NAME]
    document_models = db_models    
    await init_beanie(database=DATABASE, document_models=document_models)