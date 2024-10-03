from aiogram.utils.keyboard import InlineKeyboardBuilder


async def back_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔙 В главное меню', callback_data='main_menu')
    return builder.as_markup()
