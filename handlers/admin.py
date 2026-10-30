import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from core.database import get_db

router = Router()

# 🛑 TUMHARI ID YAHAN FIX KAR DI HAI
OWNER_ID = 8480878371 

# ================= OWNER PANEL =================
@router.message(Command("admin", "panel"), F.from_user.id == OWNER_ID)
async def owner_panel(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Add Panel URL", callback_data="admin_add_url")],
        [InlineKeyboardButton(text="🚫 Ban User", callback_data="admin_ban")],
        [InlineKeyboardButton(text="✅ Unban User", callback_data="admin_unban")],
        [InlineKeyboardButton(text="📊 API Stats", callback_data="admin_stats")]
    ])
    await message.answer(
        f"👑 <b>Owner Control Panel</b>\n\n"
        f"Welcome King! 👋\n"
        f"Yahan se sab manage karein:", 
        reply_markup=kb, 
        parse_mode="HTML"
    )

# ================= ADD PANEL URL =================
@router.message(Command("addurl"), F.from_user.id == OWNER_ID)
async def add_url_cmd(message: Message):
    try:
        args = message.text.replace("/addurl ", "").split("|")
        country = args[0].strip()
        url = args[1].strip()
        
        conn = await get_db()
        await conn.execute("INSERT INTO panel_urls (country, url) VALUES ($1, $2)", country, url)
        await conn.close()
        
        await message.answer(f"✅ <b>Panel URL Added!</b>\nCountry: {country}\nURL: <code>{url}</code>", parse_mode="HTML")
    except Exception:
        await message.answer("❌ Format galat hai! Aise bhejo:\n<code>/addurl Sri Lanka | https://your-panel.com/api</code>", parse_mode="HTML")
