from aiogram import Router
from aiogram_dialog import DialogRegistry

from .add import add_department_dialog
from .delete import delete_department_dialog
from .edit import edit_department_dialog
from .menu import department_menu_dialog


def register_department_handlers(admin_router: Router, dialog_registry: DialogRegistry):
    dialog_registry.register(department_menu_dialog, router=admin_router)
    dialog_registry.register(add_department_dialog, router=admin_router)
    dialog_registry.register(edit_department_dialog, router=admin_router)
    dialog_registry.register(delete_department_dialog, router=admin_router)
