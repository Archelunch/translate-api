import logging
import logging.config
import sys
import time
from typing import Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

# Logging configuration
logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stderr,
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console"
        ],
        "propagate": True
    }
}

logging.config.dictConfig(logging_config)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        self._logger = logging.getLogger(__name__)
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id: str = str(uuid4())
        logging_dict = {
            "X-API-REQUEST-ID": request_id
        }

        await self.set_body(request)
        response, response_dict = await self._log_response(call_next, request, request_id)
        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict

        self._logger.info(logging_dict)

        return response

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def _log_request(self, request: Request) -> str:
        """Logs request part
            Arguments:
           - request: Request
        """

        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host
        }

        try:
            body = await request.json()
            request_logging["body"] = body
        except Exception:
            body = None

        return request_logging

    async def _log_response(self, call_next: Callable, request: Request, request_id: str) -> Response:
        """Logs response part
               Arguments:
               - call_next: Callable (To execute the actual path function and get response back)
               - request: Request
               - request_id: str (uuid)
               Returns:
               - response: Response
               - response_logging: str
        """

        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request, request_id)
        finish_time = time.perf_counter()

        overall_status = "successful" if response.status_code < 400 else "failed"
        execution_time = finish_time - start_time

        response_logging = {
            "status": overall_status,
            "status_code": response.status_code,
            "time_taken": f"{execution_time:0.4f}s"
        }
        return response, response_logging

    async def _execute_request(self, call_next: Callable, request: Request, request_id: str) -> Response:
        """Executes the actual path function using call_next.
               It also injects "X-API-Request-ID" header to the response.

               Arguments:
               - call_next: Callable (To execute the actual path function
                            and get response back)
               - request: Request
               - request_id: str (uuid)
               Returns:
               - response: Response
        """
        try:
            response: Response = await call_next(request)
            response.headers["X-API-Request-ID"] = request_id
            return response
        except Exception as e:
            self._logger.exception(
                {
                    "path": request.url.path,
                    "method": request.method,
                    "reason": e
                }
            )
