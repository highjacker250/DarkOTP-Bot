from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
from aiogram.filters import Command

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
        [InlineKeyboardButton(text="🟢 WhatsApp", callback_data="srv_whatsapp")],
        [InlineKeyboardButton(text="🔵 Facebook", callback_data="srv_facebook")],
        [InlineKeyboardButton(text="🔴 Instagram", callback_data="srv_instagram")]
    ])
    await callback.message.edit_text("Select Service:", reply_markup=kb)

@router.callback_query(F.data.startswith("srv_"))
async def select_country(callback: CallbackQuery):
    service = callback.data.split("_")[1]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇱🇰 Sri Lanka", callback_data=f"buy_{service}_lk")],
        [InlineKeyboardButton(text="🇷🇺 Russia", callback_data=f"buy_{service}_ru")]
    ])
    await callback.message.edit_text("Select Country:", reply_markup=kb)

@router.callback_query(F.data.startswith("buy_"))
async def show_numbers(callback: CallbackQuery):
    _, service, country = callback.data.split("_")
    
    # Fake loading animation
    await callback.message.edit_text("⏳ <i>Connecting to server...</i>", parse_mode="HTML")
    import asyncio
    await asyncio.sleep(1)
    
    # Example Numbers (Yahan DB se aayenge)
    numbers = ["+94765601844", "+94765607342", "+94765608696"]
    
    kb_buttons = []
    for num in numbers:
        # Copy button feature (Naya Telegram update)
        kb_buttons.append([InlineKeyboardButton(text=f"📞 {num}", copy_text=CopyTextButton(text=num))])
        
    kb_buttons.append([InlineKeyboardButton(text="🔄 Refresh", callback_data=f"buy_{service}_{country}")])
    
    await callback.message.edit_text(
        f"✅ <b>Numbers Fetched!</b>\n\n"
        f"Aapke numbers taiyar hain. OTP aane par yahin bheja jayega.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_buttons),
        parse_mode="HTML"
    )
