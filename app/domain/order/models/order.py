from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple


from app.domain.common.models.entity import entity
from app.domain.common.models.value_object import value_object
from app.domain.order.exceptions.order import (
    ConfirmationAlreadyProcessed,
    OrderNotConfirmed,
)


class ConfirmationPathType(Enum):
    CHIEF = "CHIEF"
    INFORM = "INFORM"


@entity
class User:
    id: int
    name: str


@entity
class Department:
    id: int
    name: str


@entity
class Cost:
    id: int
    name: str
    department: Department


@entity
class ConfirmationPaths:
    id: int
    user: User
    type: ConfirmationPathType


@entity
class ConfirmationPath:
    creator: User
    cost: Cost
    confirmation_paths: Tuple[ConfirmationPaths]


@entity
class Currency:
    id: int
    name: str


@value_object
class OrderDetails:
    date: datetime
    amount: Decimal
    vat: bool
    currency: Currency
    comment: str


@entity
class Confirmation:
    date: Optional[datetime]
    status: Optional[bool]

    @property
    def processed(self):
        return self.date and self.status is not None

    def confirm(self):
        if self.status is not None:
            raise ConfirmationAlreadyProcessed()

        self.date = datetime.now()
        self.status = True

    def deny(self):
        if self.status is not None:
            raise ConfirmationAlreadyProcessed()

        self.date = datetime.now()
        self.status = False

    def invert_status(self):
        if self.status is None:
            raise OrderNotConfirmed()

        self.status = not self.status

    def clean(self):
        self.date = None
        self.status = None


@entity
class Order:
    id: int
    confirmation_path: ConfirmationPath
    order_details: OrderDetails
    confirmation: Confirmation

    def change_confirmation_path(self, new_confirmation_path: ConfirmationPath):
        self.confirmation_path = new_confirmation_path

    def change_order_details(self, new_order_details: OrderDetails):
        self.order_details = new_order_details

    def confirm(self):
        self.confirmation.confirm()

    def deny(self):
        self.confirmation.deny()

    def invert_status(self):
        self.confirmation.invert_status()

    def clean_confirmation_status(self):
        self.confirmation.clean()
