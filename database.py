# database.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import DB_NAME, DB_URL

CLIENT_MONGO: AsyncIOMotorClient | None = None
DATABASE: AsyncIOMotorDatabase | None = None


async def init_db():
    global CLIENT_MONGO, DATABASE
    CLIENT_MONGO = AsyncIOMotorClient("mongodb://localhost:27017/")
    DATABASE = CLIENT_MONGO["ecofier"]
    print("✅ Database initialized")


async def close_db():
    CLIENT_MONGO.close()
    print("❌ Database connection closed")
