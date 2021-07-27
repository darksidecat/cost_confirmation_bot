from sqlalchemy import BIGINT, INT, TEXT, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class DepartmentEntry(Base):
    __tablename__ = "department"

    id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)

    costs = relationship("CostEntry", back_populates="department")


class InformLevelEntry(Base):
    __tablename__ = "inform_level"

    id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)

    confirmation_path_chief = relationship(
        "ConfirmationPathChiefEntry", back_populates="inform_level"
    )


class CostEntry(Base):
    __tablename__ = "cost"

    id = Column(INT, primary_key=True, autoincrement=True)
    department_id = Column(INT, ForeignKey("department.id"))
    name = Column(TEXT, nullable=False)

    department = relationship("DepartmentEntry", back_populates="costs")
    confirmation_paths = relationship("ConfirmationPathEntry", back_populates="cost")


class ConfirmationPathEntry(Base):
    __tablename__ = "confirmation_path"

    id = Column(INT, primary_key=True, autoincrement=True)
    cost_id = Column(INT, ForeignKey("cost.id"), nullable=False)
    user_id = Column(BIGINT, ForeignKey("user.id"), nullable=False)

    cost = relationship("CostEntry", back_populates="confirmation_paths")
    user = relationship("TelegramUserEntry", back_populates="confirmation_path")
    confirmation_path_chief = relationship(
        "ConfirmationPathChiefEntry", back_populates="confirmation_path"
    )

    __table_args__ = (UniqueConstraint("cost_id", "user_id", name="_user_cost"),)


class ConfirmationPathChiefEntry(Base):
    __tablename__ = "confirmation_path_chief"

    id = Column(INT, primary_key=True, autoincrement=True)
    confirmation_path_id = Column(
        INT, ForeignKey("confirmation_path.id"), nullable=False
    )
    chief_id = Column(BIGINT, ForeignKey("user.id"), nullable=False)
    inform_level_id = Column(INT, ForeignKey("inform_level.id"), nullable=False)

    confirmation_path = relationship(
        "ConfirmationPathEntry", back_populates="confirmation_path_chief"
    )
    chief = relationship("TelegramUserEntry", back_populates="confirmation_path_chief")
    inform_level = relationship(
        "InformLevelEntry", back_populates="confirmation_path_chief"
    )
