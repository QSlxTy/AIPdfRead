from aiogram.utils.keyboard import InlineKeyboardBuilder


async def start_mail_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='🚫 В главное меню', callback_data='main_menu')
    builder.button(text='✅ Начать', callback_data='start_mail')
    return builder.as_markup()