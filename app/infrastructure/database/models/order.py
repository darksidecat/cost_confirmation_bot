from sqlalchemy import BIGINT, BOOLEAN, INT, REAL, TEXT, TIMESTAMP, Column, ForeignKey

from .base import Base


class CurrencyEntry(Base):
    __tablename__ = "currency"

    id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)


class OrderEntry(Base):
    __tablename__ = "order"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("user.id"), nullable=False)
    confirmation_path_id = Column(
        INT, ForeignKey("confirmation_path.id"), nullable=False
    )
    amount = Column(REAL, nullable=False)
    vat = Column(BOOLEAN, nullable=False)
    currency = Column(INT, ForeignKey("currency.id"), nullable=False)
    cost_id = Column(INT, ForeignKey("cost.id"), nullable=False)
    comment = Column(TEXT, nullable=False)
    chief_confirm = Column(BOOLEAN)
    date = Column(TIMESTAMP, nullable=False)
    date_confirm = Column(TIMESTAMP)

    def __init__(
        self,
        user_id,
        confirmation_path_id,
        amount,
        vat,
        currency,
        cost_id,
        comments,
        date,
    ):
        self.user_id = user_id
        self.confirmation_path_id = confirmation_path_id
        self.amount = amount
        self.vat = vat
        self.currency = currency
        self.cost_id = cost_id
        self.comments = comments
        self.chief_confirm = None
        self.date = date
        self.date_confirm = None

    def __repr__(self):
        return f"<Order #{self.order_id}>"
