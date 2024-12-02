from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    login = State()
    password = State()

class Work(StatesGroup):
    main_menu = State()

class MemoryPage(StatesGroup):
    search_memory = State()
    all_memory = State()
    mp_menu = State()

class NN(StatesGroup):
    gen_photo = State()
    gen_video = State()
    colorize = State()
