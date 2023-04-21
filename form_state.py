from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    """Class for FSM"""
    main = State()
    main_meny = State()
    chanel = State()
    add_chanel = State()
    add_chanel_bd = State()
    select_chanel = State()
    save_tag = State()
    add_media_db = State()
    publesh_post = State()
    time_post = State()
    list_events = State()
    choose_action_event = State()
    delete_event = State()
    add_tag = State()
