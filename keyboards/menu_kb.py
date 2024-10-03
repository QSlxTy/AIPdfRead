from aiogram.utils.keyboard import InlineKeyboardBuilder


async def menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Текст', callback_data='1')
    builder.adjust(1)
    return builder.as_markup()