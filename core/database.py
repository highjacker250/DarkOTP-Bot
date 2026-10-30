import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def get_db():
    return await asyncpg.connect(os.getenv("DATABASE_URL"))

async def init_db():
    """Start hote hi tables check karega"""
    conn = await get_db()
    # Yahan hum tables create kar sakte hain agar nahi hain
    await conn.close()
