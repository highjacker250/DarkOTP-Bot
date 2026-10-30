import asyncio
from aiogram import Bot, Dispatcher
from core.database import get_db
from core.config import BOT_TOKEN
from handlers import user, admin
from services.expiry import start_expiry_task

async def start_single_bot(token: str):
    bot = Bot(token=token)
    dp = Dispatcher()
    
    # Handlers Register karo
    dp.include_router(user.router)
    dp.include_router(admin.router)
    
    # Background Task: 1 Hour Expiry
    asyncio.create_task(start_expiry_task(bot))
    
    try:
        print(f"✅ Bot Started: {token[:10]}...")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Bot Crashed: {e}")

async def main():
    # 1. Database se saare active bots uthao
    conn = await get_db()
    bots = await conn.fetch("SELECT token FROM bots WHERE is_active = TRUE")
    await conn.close()
    
    # 2. Agar koi bot DB me nahi hai, toh default token chalao
    if not bots:
        await start_single_bot(BOT_TOKEN)
    else:
        # Saare bots ek saath (parallel) chalao
        tasks = [start_single_bot(row['token']) for row in bots]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

from aiohttp import web

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
