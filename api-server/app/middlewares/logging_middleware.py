import json
import logging
import os
from datetime import datetime
from typing import Callable

from app.config.settings import settings
from fastapi import FastAPI, Request


class JSONFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "process": record.process,
            "thread": record.thread,
            "extra": record.__dict__.get("extra", {}),
            "function": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(data)


class LoggingMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.logger = logging.getLogger("fastapi")
        self.setup_logging()

    def setup_logging(self):
        os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setFormatter(JSONFormatter())
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        request.state.start_time = datetime.now()

        async def send_with_logging(message):
            if message["type"] == "http.response.start":
                request.state.response = message
            await send(message)

        try:
            response = await self.app(scope, receive, send_with_logging)
            extra_data = {
                "method": request.method,
                "path": request.url.path,
                "response_time_ms": int(
                    (datetime.now() - request.state.start_time).total_seconds() * 1000
                ),
                "client_ip": request.client.host,
                "user_id": getattr(request.state, "user_id", None),
                "request_id": getattr(request.state, "request_id", None),
            }
            self.logger.info("Request processed", extra=extra_data)
            return response
        except Exception as e:
            extra_data = {
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host,
                "error": str(e),
            }
            self.logger.error("Request failed", extra=extra_data)
            raise
