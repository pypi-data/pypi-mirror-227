import datetime
import uuid

from collections.abc import Mapping
from urllib.parse import urlparse

from clipped.utils.json import orjson_dumps

from django.test import Client
from django.test.client import FakePayload

CONTENT_TYPE_APPLICATION_JSON = "application/json"


class BaseClient(Client):
    """Base client class."""

    def do_request(
        self,
        method,
        path,
        data=None,
        content_type=CONTENT_TYPE_APPLICATION_JSON,
        **extra
    ):
        if data is None:
            data = {}

        def validate_data(dvalues):
            if not isinstance(dvalues, Mapping):
                return
            for key, value in dvalues.items():
                # Fix UUIDs for convenience
                if isinstance(value, uuid.UUID):
                    dvalues[key] = value.hex

                # Fix datetimes
                if isinstance(value, datetime.datetime):
                    dvalues[key] = value.strftime("%Y-%m-%d %H:%M")

        if isinstance(data, list):
            for d in data:
                validate_data(d)
        else:
            validate_data(data)

        if content_type == CONTENT_TYPE_APPLICATION_JSON:
            data = orjson_dumps(data)

        request = self.encode_data(method, path, data, content_type, **extra)
        return self.request(**request)

    def put(self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra):
        """Construct a PUT request."""
        return self.do_request("PUT", path, data, content_type, **extra)

    def patch(
        self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra
    ):
        """Construct a PATCH request."""
        return self.do_request("PATCH", path, data, content_type, **extra)

    def post(
        self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra
    ):
        """Construct a PATCH request."""
        return self.do_request("POST", path, data, content_type, **extra)

    def delete(
        self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra
    ):
        """Construct a DELETE request."""
        return self.do_request("DELETE", path, data, content_type, **extra)

    def encode_data(self, http_method, path, data, content_type, **extra):
        patch_data = self._encode_data(data, content_type)

        parsed = urlparse(path)
        request = {
            "CONTENT_LENGTH": len(patch_data),
            "CONTENT_TYPE": content_type,
            "PATH_INFO": self._get_path(parsed),
            "QUERY_STRING": parsed[4],
            "REQUEST_METHOD": http_method,
            "wsgi.input": FakePayload(patch_data),
        }
        request.update(extra)

        return request
