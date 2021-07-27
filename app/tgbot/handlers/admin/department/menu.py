from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Cancel, Start
from aiogram_dialog.widgets.text import Const

from app.tgbot.states.admin_menu import DepartmentCategory
from app.tgbot.states.department import AddDepartment, DeleteDepartment, EditDepartment

department_menu_dialog = Dialog(
    Window(
        Const("Department\n\n Select action"),
        Start(
            Const("Add"),
            id="add_department",
            state=AddDepartment.name,
            mode=StartMode.NORMAL,
        ),
        Start(
            Const("Edit"),
            id="edit_department",
            state=EditDepartment.select_department,
            mode=StartMode.NORMAL,
        ),
        Start(
            Const("Delete"),
            id="delete_department",
            state=DeleteDepartment.select_department,
            mode=StartMode.NORMAL,
        ),
        Cancel(),
        state=DepartmentCategory.action,
    ),
)
