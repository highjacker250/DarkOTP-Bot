import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from core.database import get_db
from core.config import BOT_TOKEN
from handlers import user, admin
from services.expiry import start_expiry_task

async def start_single_bot(token: str):
    """Ek single bot ko start karne ka function"""
    bot = Bot(token=token)
    dp = Dispatcher()
    
    # Routers register karo
    dp.include_router(user.router)
    dp.include_router(admin.router)
    
    # Background task (1 hour expiry) start karo
    asyncio.create_task(start_expiry_task(bot))
    
    try:
        print(f"✅ Bot Started: {token[:10]}...")
        # Polling start karo
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Bot Crashed (Token: {token[:10]}...): {e}")

async def health_check(request):
    """Render ke liye dummy route taaki port open rahe"""
    return web.Response(text="Bot is running 24/7")

async def start_web_server():
    """Render requirement: Port bind karna zaroori hai"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render ka PORT variable use karo, aur 0.0.0.0 par bind karo
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌍 Web server running on port {port}")

async def main():
    print("🚀 Starting Bot System...")
    
    # 1. Sabse pehle Web Server start karo (Render ke liye zaroori)
    await start_web_server()
    
    # 2. Database connect karke bots fetch karo
    print("⏳ Connecting to Database...")
    bots = []
    try:
        conn = await get_db()
        print("✅ Database connected successfully!")
        bots = await conn.fetch("SELECT token FROM bots WHERE is_active = TRUE")
        await conn.close()
        print(f"📦 Found {len(bots)} active bots in database.")
    except Exception as e:
        print(f"⚠️ Database Error: {e}")
        print("⚠️ Falling back to default bot from ENV.")
    
    # 3. Bots start karo
    if not bots:
        # Agar DB me koi bot nahi hai, toh ENV wala default bot chalao
        print("🤖 Starting default bot from ENV...")
        await start_single_bot(BOT_TOKEN)
    else:
        # Agar DB me bots hain, toh sabko parallel chalao
        print("🤖 Starting bots from Database...")
        tasks = [start_single_bot(row['token']) for row in bots]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Bot stopped manually.")
