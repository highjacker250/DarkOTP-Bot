import asyncio
import os  # <--- Ye import zaroori tha
from aiohttp import web
from aiogram import Bot, Dispatcher
from core.database import get_db
from core.config import BOT_TOKEN
from handlers import user, admin
from services.expiry import start_expiry_task

async def start_single_bot(token: str):
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(admin.router)
    asyncio.create_task(start_expiry_task(bot))
    try:
        print(f"✅ Bot Started: {token[:10]}...")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Bot Crashed: {e}")

# Render ke liye Web Server
async def health_check(request):
    return web.Response(text="Bot is running 24/7")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌍 Web server running on port {port}")

async def main():
    # 1. Sabse pehle Web Server start karo
    await start_web_server()
    
    # 2. Fir Database connect karo
    conn = await get_db()
    bots = await conn.fetch("SELECT token FROM bots WHERE is_active = TRUE")
    await conn.close()
    
    # 3. Fir Bot start karo
    if not bots:
        await start_single_bot(BOT_TOKEN)
    else:
        tasks = [start_single_bot(row['token']) for row in bots]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
