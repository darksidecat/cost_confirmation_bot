import pytest

from app.domain.access_levels.models.helper import Levels
from app.domain.user.exceptions.user import (
    BlockedUserWithOtherRole,
    UserWithNoAccessLevels,
)
from app.domain.user.models.user import TelegramUser


class TestUser:
    @pytest.mark.parametrize(
        "user",
        [
            TelegramUser(
                id=1,
                name="U",
                access_levels=[
                    Levels.USER.value,
                ],
            ),
            TelegramUser(
                id=1,
                name="U",
                access_levels=[Levels.USER.value, Levels.ADMINISTRATOR.value],
            ),
        ],
    )
    def test_block_user(self, user):
        user.block_user()
        assert user.access_levels == [
            Levels.BLOCKED.value,
        ]

    @pytest.mark.parametrize(
        "user, result",
        [
            [
                TelegramUser(
                    id=1,
                    name="U",
                    access_levels=[Levels.USER.value, Levels.ADMINISTRATOR.value],
                ),
                False,
            ],
            [
                TelegramUser(
                    id=1,
                    name="U",
                    access_levels=[
                        Levels.BLOCKED.value,
                    ],
                ),
                True,
            ],
            [
                TelegramUser(
                    id=1,
                    name="U",
                    access_levels=[
                        Levels.BLOCKED.value,
                    ],
                ),
                True,
            ],
        ],
    )
    def test_blocked(self, user, result):
        assert user.is_blocked is result

    def test_not_empty_access_levels(self):
        with pytest.raises(UserWithNoAccessLevels):
            TelegramUser(id=1, name="U", access_levels=())

    def test_duplicate_access_levels(self):
        user = TelegramUser(
            id=1, name="U", access_levels=[Levels.USER.value, Levels.USER.value]
        )
        assert user.access_levels == [
            Levels.USER.value,
        ]

        user.access_levels = [Levels.USER.value, Levels.USER.value]
        assert user.access_levels == [
            Levels.USER.value,
        ]

    def test_blocked_role(self):
        with pytest.raises(BlockedUserWithOtherRole):
            TelegramUser(
                id=1, name="U", access_levels=[Levels.BLOCKED.value, Levels.USER.value]
            )
