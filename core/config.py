import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv()

# Variables set karo
BOT_TOKEN = os.getenv("SUPER_ADMIN_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
DATABASE_URL = os.getenv("DATABASE_URL")
