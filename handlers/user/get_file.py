import os

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from bot_start import bot, logger
from keyboards.user.user_keyboard import back_menu_kb
from utils.aiogram_helper import SendMessage, clear_directory
from utils.pdf import convert_to_sheet
from utils.states.user import FSMStart


async def get_file(message: types.Message, state: FSMContext, album: list = None):
    if album:
        await SendMessage(event=message,
                          text=f'<b>Получил <code>{len(album)}</code> файлов 📁\n'
                               f'Начинаю обработку ⚙️\n\n</b>'
                               '❗️<i>Это может занять 3-20 минут в зависимости от количества информации</i>',
                          handler_name='get_file',
                          state=state).custom_send()
        count = len(album)
        for msg in album:
            await msg.delete()
        try:
            os.makedirs(f'files/{message.from_user.id}')
        except Exception:
            pass
        await state.set_state(FSMStart.start)
        check = 0
        list_names = ''
        for msg in album:
            if '.pdf' not in msg.document.file_name:
                list_names += f'<code>{msg.document.file_name}</code>\n\n'
                check = 1
        if check == 1:
            await SendMessage(event=message,
                              text=f'<b>❗️Ошибка\n'
                                   f'Файлы:\n'
                                   f'{list_names}'
                                   f'не являются</b> <code>.pdf</code>',
                              handler_name='get_file',
                              state=state).custom_send()
            return
        for msg in album:
            await bot.download(msg.document, f'files/{msg.from_user.id}/{msg.document.file_id}.pdf')
    else:
        await message.delete()
        count = 1
        await SendMessage(event=message,
                          text=f'<b>Получил <code>1</code> файл 📁\n\n'
                               f'Начинаю обработку ⚙️\n\n</b>'
                               '❗️<i>Это может занять 3-20 минут в зависимости от количества информации</i>',
                          handler_name='get_file',
                          state=state).custom_send()
        await bot.download(message.document, f'files/{message.from_user.id}/{message.document.file_id}.pdf')

        if '.pdf' not in message.document.file_name:
            await SendMessage(event=message,
                              text=f'<b>❗️Ошибка\n'
                                   f'Файл:\n'
                                   f'{message.document.file_name}'
                                   f'не является</b> <code>.pdf</code>',
                              handler_name='get_file',
                              state=state).custom_send()
    documents = os.listdir(f'files/{message.from_user.id}')
    try:
        link_array = await convert_to_sheet(message.from_user.id,
                                            documents,
                                            message.document.file_name)
        link_str = ''
        for link in link_array:
            link_str += (f'📌 1. Название файла - {link.split(";")[1]}\n'
                         f'🔗 Cсылка - {link.split(";")[0]}\n\n')
        await SendMessage(event=message,
                          text=f'<b>Обработка <code>{count}</code> .pdf файлов завершена 📋\n\n'
                               f'{link_str}</b>',
                          handler_name='get_file',
                          keyboard=back_menu_kb,
                          state=state).custom_send()
    except Exception as _ex:
        logger.error(f'convert error --> {_ex}')
        await clear_directory(f'files/{message.from_user.id}')
        await SendMessage(event=message,
                          text=f'<b>❗️Произошла ошибка, попробуйте снова или обратитесь к администрации</b>',
                          handler_name='get_file',
                          keyboard=back_menu_kb,
                          state=state).custom_send()


def register_handler(dp: Dispatcher):
    dp.message.register(get_file, F.content_type == 'document')
