from typing import Awaitable, Callable

from fastapi import Request, Response
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class DatabaseSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, session_factory: sessionmaker) -> None:
        super().__init__(app)
        self.session_factory = session_factory

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        async with self.session_factory() as session:
            request.state.db_session = session
            return await call_next(request)
