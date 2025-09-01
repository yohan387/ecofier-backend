# database.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


DATABASE_URL = "mongodb+srv://admin:admin@cluster0.hagx7ew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = 'ecofier_1'

CLIENT_MONGO = AsyncIOMotorClient(DATABASE_URL)
DATABASE = CLIENT_MONGO[DATABASE_NAME]


async def init_db(db: AsyncIOMotorDatabase):
    logging.info(f"Initialise la base de données")
    

async def close_db():
    CLIENT_MONGO.close()
    print("❌ Database connection closed")
