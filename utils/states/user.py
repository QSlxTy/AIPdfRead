from aiogram.fsm.state import State, StatesGroup


class FSMStart(StatesGroup):
    start = State()