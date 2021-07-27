from operator import itemgetter

from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Next, Row, Select
from aiogram_dialog.widgets.text import Const, Format

from app.tgbot import states
from app.tgbot.constants import DEPARTMENT_NAME, YES_NO
from app.tgbot.handlers.dialogs.common import enable_send_mode, get_result


async def request_name(
    message: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager
):
    manager.current_context().dialog_data[DEPARTMENT_NAME] = message.text
    await dialog.next()


async def add_department_yes_no(args):
    pass


async def get_department_data(args):
    pass


add_department_dialog = Dialog(
    Window(
        Const("Input department name:"),
        MessageInput(request_name),
        Row(Cancel()),
        # getter=get_user_data,
        state=states.department.AddDepartment.name,
        parse_mode="HTML",
        preview_add_transitions=[
            Next(),
        ],
    ),
    Window(
        Const("Confirm ?"),
        Select(
            Format("{item[0]}"),
            id="add_yes_no",
            item_id_getter=itemgetter(1),
            items=YES_NO,
            on_click=add_department_yes_no,
        ),
        Row(Back(), Cancel()),
        getter=get_department_data,
        state=states.department.AddDepartment.confirm,
        parse_mode="HTML",
        preview_add_transitions=[Next()],
    ),
    Window(
        Format("{result}"),
        Cancel(Const("Close"), on_click=enable_send_mode),
        getter=get_result,
        state=states.department.AddDepartment.result,
        parse_mode="HTML",
    ),
)
