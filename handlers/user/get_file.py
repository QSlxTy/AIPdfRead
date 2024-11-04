import os

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from bot_start import bot, logger
from keyboards.user.user_keyboard import back_menu_kb
from utils.aiogram_helper import SendMessage, clear_directory
from utils.pdf import convert_to_sheet
from utils.states.user import FSMStart


async def get_file(message: types.Message, state: FSMContext, album: list = None):
    try:
        os.makedirs(f'files/{message.from_user.id}')
    except Exception:
        pass
    if album:
        msg_start = await SendMessage(event=message,
                                      text=f'<b>Получил файлов: <code>{len(album)}</code>  📁\n\n'
                                           f'Начинаю обработку ⚙️\n\n</b>'
                                           '❗️<i>Это может занять 3-20 минут в зависимости от количества информации</i>',
                                      handler_name='get_file',
                                      state=state).custom_send()
        count = len(album)
        for msg in album:
            await msg.delete()
        check = 0
        list_names = ''
        for msg in album:
            if not (msg.document.file_name.endswith('.pdf') or msg.document.file_name.endswith('.PDF')):
                list_names += f'<code>{msg.document.file_name}</code>\n\n'
                check = 1
        if check == 1:
            await SendMessage(event=message,
                              text=f'<b>❗️Ошибка\n\n'
                                   f'Файлы:\n'
                                   f'{list_names}'
                                   f'не являются</b> <code>.pdf</code>',
                              handler_name='get_file',
                              state=state).custom_send()
            return
        names = []
        for msg in album:
            await bot.download(msg.document, f'files/{msg.from_user.id}/{msg.document.file_id}.pdf')
            names.append(msg.document.file_name)
    else:
        await message.delete()
        count = 1
        msg_start = await SendMessage(event=message,
                                      text=f'<b>Получил файлов: <code>1</code> 📁\n\n'
                                           f'Начинаю обработку ⚙️\n\n</b>'
                                           '❗️<i>Это может занять 3-20 минут в зависимости от количества информации</i>',
                                      handler_name='get_file',
                                      state=state).custom_send()
        await bot.download(message.document, f'files/{message.from_user.id}/{message.document.file_id}.pdf')
        names = [message.document.file_name]
        if not (message.document.file_name.endswith('.pdf') or message.document.file_name.endswith('.PDF')):
            await SendMessage(event=message,
                              text=f'<b>❗️Ошибка\n\n'
                                   f'Файл: <code>{message.document.file_name}</code> не является</b> <code>.pdf</code>',
                              handler_name='get_file',
                              state=state).custom_send()
            return
    documents = os.listdir(f'files/{message.from_user.id}')
    await state.update_data(msg=msg_start)
    await state.set_state(FSMStart.empty)

    link_array = await convert_to_sheet(message.from_user.id,
                                        documents,
                                        names)
    if link_array is None:
        logger.error(f'convert error')
        await clear_directory(f'files/{message.from_user.id}')
        await SendMessage(event=message,
                          text=f'<b>❗️Произошла ошибка, попробуйте снова или обратитесь к администрации</b>',
                          handler_name='get_file',
                          keyboard=back_menu_kb,
                          state=state).custom_send()
        return
    if type(link_array) is str:
        await SendMessage(event=message,
                          text=f'<b>❗️Произошла ошибка, попробуйте снова или обратитесь к администрации</b>\n'
                               f'Возможно ошибка в файле {link_array.split(";")[0]}',
                          handler_name='get_file',
                          keyboard=back_menu_kb,
                          state=state).custom_send()
        return
    else:
        link_str = ''
        for i, link in enumerate(link_array):
            if 'bad' in link:
                link_str += (f'❌ {i + 1}. Название файла - {names[i]}\n'
                             f'Неудалось обработать файл\n\n')
            else:
                link_str += (f'📌 {i + 1}. Название файла - {names[i]}\n'
                             f'🔗 Cсылка -\n {link.split(";")[0]}\n\n')
        await SendMessage(event=message,
                          text=f'<b>Обработка <code>{count}</code> .pdf файлов завершена 📋\n\n'
                               f'{link_str}</b>',
                          handler_name='get_file',
                          keyboard=back_menu_kb,
                          state=state).custom_send()
        await state.clear()


def register_handler(dp: Dispatcher):
    dp.message.register(get_file, F.content_type == 'document')
