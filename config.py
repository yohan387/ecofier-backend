from dotenv import load_dotenv
import os

# Charger .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_URL = os.getenv("DB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
