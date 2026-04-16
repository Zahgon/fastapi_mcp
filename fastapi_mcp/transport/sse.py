from uuid import UUID
import logging
from typing import Union

from anyio.streams.memory import MemoryObjectSendStream
from fastapi import Request, Response, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from mcp.shared.message import SessionMessage, ServerMessageMetadata
from pydantic import ValidationError
from mcp.server.sse import SseServerTransport
from mcp.types import JSONRPCMessage, JSONRPCError, ErrorData


logger = logging.getLogger(__name__)


class FastApiSseTransport(SseServerTransport):
    async def handle_fastapi_post_message(self, request: Request) -> Response:
        """
        A reimplementation of the handle_post_message method of SseServerTransport
        that integrates better with FastAPI.

        A few good reasons for doing this:
        1. Avoid mounting a whole Starlette app and instead use a more FastAPI-native
           approach. Mounting has some known issues and limitations.
        2. Avoid re-constructing the scope, receive, and send from the request, as done
           in the original implementation.
        3. Use FastAPI's native response handling mechanisms and exception patterns to
           avoid unexpected rabbit holes.

        The combination of mounting a whole Starlette app and reconstructing the scope
        and send from the request proved to be especially error-prone for us when using
        tracing tools like Sentry, which had destructive effects on the request object
        when using the original implementation.
        """
        pass

    async def _send_message_safely(
        self, writer: MemoryObjectSendStream[SessionMessage], message: Union[SessionMessage, ValidationError]
    ):
        """Send a message to the writer, avoiding ASGI race conditions"""
        pass
