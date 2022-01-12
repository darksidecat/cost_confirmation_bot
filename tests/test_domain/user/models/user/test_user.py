import pytest
from pydantic import ValidationError

from app.domain.access_levels.models.access_level import Levels
from app.domain.user.models.user import User


class TestUser:
    @pytest.mark.parametrize(
        "user",
        [
            User(id=1, name="U", access_levels=(Levels.USER.value,)),
            User(
                id=1,
                name="U",
                access_levels=(Levels.USER.value, Levels.ADMINISTRATOR.value),
            ),
        ],
    )
    def test_block_user(self, user):
        user.block_user()
        assert user.access_levels == (Levels.BLOCKED.value,)

    @pytest.mark.parametrize(
        "user, result",
        [
            [
                User(
                    id=1,
                    name="U",
                    access_levels=(Levels.USER.value, Levels.ADMINISTRATOR.value),
                ),
                False,
            ],
            [
                User(
                    id=1,
                    name="U",
                    access_levels=(Levels.BLOCKED.value,),
                ),
                True,
            ],
            [User(id=1, name="U", access_levels=(Levels.BLOCKED.value,)), True],
        ],
    )
    def test_blocked(self, user, result):
        assert user.is_blocked is result

    def test_not_empty_access_levels(self):
        with pytest.raises(
            ValidationError, match="User must have at least one access level"
        ):
            User(id=1, name="U", access_levels=())

    def test_duplicate_access_levels(self):
        user = User(
            id=1, name="U", access_levels=(Levels.USER.value, Levels.USER.value)
        )
        assert user.access_levels == (Levels.USER.value,)
        user.access_levels = [Levels.USER.value, Levels.USER.value]
        assert user.access_levels == (Levels.USER.value,)

    def test_blocked_role(self):
        with pytest.raises(
            ValidationError, match="Blocked user can have only that role"
        ):
            User(
                id=1, name="U", access_levels=(Levels.BLOCKED.value, Levels.USER.value)
            )
