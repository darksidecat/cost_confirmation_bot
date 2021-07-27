from aiogram.dispatcher.fsm.state import State, StatesGroup


class AddDepartment(StatesGroup):
    name = State()
    confirm = State()
    result = State()


class DeleteDepartment(StatesGroup):
    select_department = State()
    # confirm = State()
    # result = State()


class EditDepartment(StatesGroup):
    select_department = State()
    # result = State()
