import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


DATABASE_URL = 'mongodb://localhost:27017/'
DATABASE_NAME = 'ecofier_1'

CLIENT_MONGO = AsyncIOMotorClient(DATABASE_URL)
DATABASE = CLIENT_MONGO[DATABASE_NAME]


async def init_db(db: AsyncIOMotorDatabase):
    logging.info(f"Initialise la base de données")
    

async def close_db():
    CLIENT_MONGO.close()
    logging.info("Database connection closed")