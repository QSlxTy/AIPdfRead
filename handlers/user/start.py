from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.aiogram_helper import SendMessage
from utils.states.user import FSMStart


async def start_command(message: types.Message, state: FSMContext):
    await state.set_state(FSMStart.start)
    await message.delete()
    await SendMessage(event=message,
                      text=f'<b>Привет, <code>{message.from_user.first_name}</code> 👋\n\n'
                           'Отправь мне один или несколько .pdf файлов.</b> \n\n'
                           '❗️<i>Рекомендуем скидывать не больше 10 файлов за 1 раз</i>',
                      handler_name='start_command',
                      state=state).custom_send()


async def main_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMStart.start)
    await SendMessage(event=call,
                      text=f'<b>Привет, <code>{call.from_user.first_name}</code> 👋\n\n'
                           'Отправь мне один или несколько .pdf файлов.</b> \n\n'
                           '❗️<i>Рекомендуем скидывать не больше 10 файлов за 1 раз</i>',
                      handler_name='main_menu',
                      state=state).custom_send()


def register_start_handler(dp: Dispatcher):
    dp.message.register(start_command, Command('start'))
    dp.callback_query.register(main_menu, F.data == 'main_menu')
