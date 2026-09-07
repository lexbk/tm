from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import TYPE_CHECKING

from django.http import HttpResponse

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIRequest


class RequestIDMiddleware:
    request_id_header = 'X-Request-ID'

    def __init__(self, get_response: Callable[[WSGIRequest], HttpResponse]) -> None:
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: WSGIRequest) -> HttpResponse:
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Check if the request header already contains an ID
        request_id = request.headers.get(self.request_id_header) or request.META.get("HTTP_X_REQUEST_ID")

        # If not present, generate a new random UUID
        if not request_id:
            request_id = uuid.uuid4().hex

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        response[self.request_id_header] = request_id

        return response
