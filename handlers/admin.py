from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from core.database import get_db
from core.config import OWNER_ID
import asyncio

router = Router()

# Owner check
@router.message(Command("panel"), F.from_user.id == OWNER_ID)
async def owner_panel(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Add New Bot", callback_data="add_bot")],
        [InlineKeyboardButton(text="🌍 Add Bulk URLs", callback_data="add_bulk_urls")]
    ])
    await message.answer("👑 <b>Owner Panel</b>\nSelect an option:", reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "add_bot")
async def ask_bot_token(callback: CallbackQuery):
    await callback.message.answer("BotFather se naya token copy karke bhejein:")
    # Yahan state machine use karenge (temporarily simple rakha hai)

# Naya Bot Add (Command se)
@router.message(Command("add_bot"), F.from_user.id == OWNER_ID)
async def add_new_bot(message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("⚠️ Format: `/add_bot <TOKEN>`", parse_mode="Markdown")
    
    token = args[1]
    conn = await get_db()
    try:
        await conn.execute("INSERT INTO bots (token, owner_id) VALUES ($1, $2) ON CONFLICT DO NOTHING", token, message.from_user.id)
        await message.answer("✅ Bot added to Database! Render restart hote hi ye bot bhi chalega.")
        
        # Agar Render pe hai, toh restart karna padega. (Better approach niche bataya hai)
    except Exception as e:
        await message.answer(f"❌ Error: {e}")
    finally:
        await conn.close()
