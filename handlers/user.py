from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
from aiogram.filters import Command
from core.database import get_db
import asyncio

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Get Number", callback_data="get_number")],
        [InlineKeyboardButton(text="📊 Traffic", callback_data="traffic")]
    ])
    await message.answer("🚀 <b>Premium SMS & OTP Hub</b>\n\nSelect an option below:", reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "get_number")
async def select_service(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 WhatsApp", callback_data="srv_WhatsApp"), InlineKeyboardButton(text="🔵 Facebook", callback_data="srv_Facebook")],
        [InlineKeyboardButton(text="🟣 Instagram", callback_data="srv_Instagram"), InlineKeyboardButton(text="🔵 Telegram", callback_data="srv_Telegram")],
        [InlineKeyboardButton(text="⚫ Twitter (X)", callback_data="srv_Twitter"), InlineKeyboardButton(text="🔴 Google (Gmail)", callback_data="srv_Google")],
        [InlineKeyboardButton(text="🌐 Other Service", callback_data="srv_Other")]
    ])
    await callback.message.edit_text("📄 <b>Select Service:</b>", reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("srv_"))
async def select_country(callback: CallbackQuery):
    service = callback.data.split("_")[1]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇱🇰 Sri Lanka", callback_data=f"buy_{service}_Sri Lanka")],
        [InlineKeyboardButton(text="🇷🇺 Russia", callback_data=f"buy_{service}_Russia")],
        [InlineKeyboardButton(text="🇮🇩 Indonesia", callback_data=f"buy_{service}_Indonesia")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="get_number")]
    ])
    await callback.message.edit_text(f"🌍 Select Country for <b>{service}</b>:", reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("buy_"))
async def show_numbers(callback: CallbackQuery):
    _, service, country = callback.data.split("_")
    
    await callback.message.edit_text("⏳ <i>Connecting to Server...</i>", parse_mode="HTML")
    await asyncio.sleep(1)
    
    # Database se URL check karo
    conn = await get_db()
    panel = await conn.fetchrow("SELECT url FROM panel_urls WHERE country = $1 AND is_dead = FALSE", country)
    await conn.close()

    # Agar Owner ne URL add nahi kiya
    if not panel:
        return await callback.message.edit_text(
            f"❌ <b>Not Available in this Range!</b>\n\n"
            f"Abhi {country} ke liye koi panel/URL add nahi kiya gaya hai.\n"
            f"Kripya admin se contact karein.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Back", callback_data=f"srv_{service}")]
            ])
        )
    
    # URL mil gaya (Yahan API call karni hai)
    panel_url = panel['url']
    
    # DUMMY NUMBERS (Jab tak real API integrate nahi hoti)
    numbers = ["+94765601844", "+94765607342"] 
    
    kb_buttons = []
    for num in numbers:
        kb_buttons.append([InlineKeyboardButton(text=f"📞 {num}", copy_text=CopyTextButton(text=num))])
        
    kb_buttons.append([InlineKeyboardButton(text="🔄 Refresh", callback_data=f"buy_{service}_{country}")])
    
    await callback.message.edit_text(
        f"✅ <b>Numbers Fetched for {service}!</b>\n\n"
        f"Aapke numbers taiyar hain. OTP aane par yahin bheja jayega.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_buttons),
        parse_mode="HTML"
    )
