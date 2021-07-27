from sqlalchemy import BIGINT, INT, TEXT, Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship

from app.domain.access_levels.entities.access_level import LevelName

from .base import Base

user_access_levels = Table(
    "user_access_levels",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
    Column(
        "access_level_id",
        ForeignKey("access_level.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
)


class AccessLevelEntry(Base):
    __tablename__ = "access_level"

    id = Column(INT, primary_key=True, autoincrement=True)
    name = Column(SQLEnum(LevelName), nullable=False)

    users = relationship(
        "TelegramUserEntry",
        secondary=user_access_levels,
        back_populates="access_levels",
        cascade="all, delete",
    )


class TelegramUserEntry(Base):
    __tablename__ = "user"
    id = Column(BIGINT, primary_key=True)
    name = Column(TEXT, nullable=False)

    access_levels = relationship(
        "AccessLevelEntry",
        secondary=user_access_levels,
        back_populates="users",
        cascade="all, delete",
        lazy="selectin",
    )
    confirmation_path = relationship("ConfirmationPathEntry", back_populates="user")
    confirmation_path_chief = relationship(
        "ConfirmationPathChiefEntry", back_populates="chief"
    )
