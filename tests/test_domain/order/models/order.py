from datetime import datetime
from decimal import Decimal

import pytest

from app.domain.order.models.order import (
    Confirmation,
    ConfirmationPath,
    ConfirmationPaths,
    ConfirmationPathType,
    Cost,
    Currency,
    Department,
    Order,
    OrderDetails,
    User,
)


@pytest.fixture()
def order():
    return Order(
        id=1,
        confirmation_path=ConfirmationPath(
            creator=User(id=1, name="Fake"),
            cost=Cost(
                id=1,
                name="Car maintenance",
                department=Department(id=1, name="Administration"),
            ),
            confirmation_paths=(
                ConfirmationPaths(
                    id=1, user=User(id=1, name="Fake"), type=ConfirmationPathType.CHIEF
                ),
            ),
        ),
        order_details=OrderDetails(
            date=datetime.now(),
            amount=Decimal("103.11"),
            vat=True,
            currency=Currency(id=1, name="UAH"),
            comment="expense",
        ),
        confirmation=Confirmation(
            date=None,
            status=None,
        ),
    )


class TestOrder:
    def test_confirm(self, order):
        assert not order.confirmation.processed
        order.confirm()
        assert order.confirmation.status is True
        assert order.confirmation.date is not None

    def test_deny(self, order):
        assert not order.confirmation.processed
        order.deny()
        assert order.confirmation.status is False
        assert order.confirmation.date is not None

    def test_invert_confirmation_status(self, order):
        order.confirm()

        old_status = order.confirmation.status
        old_date = order.confirmation.date
        assert order.confirmation.processed
        order.invert_status()
        assert order.confirmation.status is not old_status
        assert order.confirmation.date is old_date

    def test_clean(self, order):
        order.confirm()
        order.clean_confirmation_status()

        assert not order.confirmation.processed
