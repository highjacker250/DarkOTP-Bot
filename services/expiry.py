import asyncio
import datetime
from core.database import get_db

async def start_expiry_task(bot):
    while True:
        conn = await get_db()
        # 1 ghante purane numbers check karo
        one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        
        expired = await conn.fetch(
            "SELECT user_id, number FROM assigned_numbers WHERE assigned_at < $1", 
            one_hour_ago
        )
        
        for row in expired:
            # Number wapas free kar do
            await conn.execute("DELETE FROM assigned_numbers WHERE number = $1", row['number'])
            
            # User ko message bhejo
            try:
                await bot.send_message(
                    row['user_id'], 
                    f"⏳ <b>Number Expired!</b>\n\n"
                    f"Aapka number <code>{row['number']}</code> expire ho gaya hai (1 Hour).\n"
                    f"Naya number lene ke liye /start dabayein.",
                    parse_mode="HTML"
                )
            except:
                pass
        
        await conn.close()
        await asyncio.sleep(60) # Har 1 minute me check karega
