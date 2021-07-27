from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Next, Row
from aiogram_dialog.widgets.text import Const

from app.tgbot import states


async def request_name(args):
    pass


edit_department_dialog = Dialog(
    Window(
        Const("Input department name:"),
        MessageInput(request_name),
        Row(Cancel()),
        # getter=get_user_data,
        state=states.department.EditDepartment.select_department,
        parse_mode="HTML",
    ),
)
