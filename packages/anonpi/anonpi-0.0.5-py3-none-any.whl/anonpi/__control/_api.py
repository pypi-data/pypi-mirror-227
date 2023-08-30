from typing import Literal
from requests import request
from json import dumps
from ..__resources.__exceptions import *
from requests.exceptions import Timeout, ConnectTimeout


class apibaserequest:
    def __init__(self, method: Literal["get", "post", "delete", "patch"], url: str, token: str, **data):
        self._method = method
        self._url = url
        self._token = token
        self._data = data

    def __repr__(self):
        _headers = {
            "Authorization": self._token
        }
        try:
            res = request(
                method=self._method,
                url=self._url,
                json=self._data,
                headers=_headers,
                timeout=5
            )
        except (Timeout, ConnectTimeout):
            raise ServerSideError("Server is not responding")
        try:
            res.json()
        except:
            if type(res.content) == bytes:
                return str(res.content)
            raise ServerSideError("Server is not responding")

        if res.json().get("status", "error") == "error":
            message = res.json().get("message", "Unknown error occured").lower()
            if "country not available" in message:
                raise CountryNotAvailable(message)
            if "invalid authorization" in message:
                raise InvalidToken(
                    "Invalid API Token Please check your token or get a new in https://anonpi.co/apisettings")
            if "not found" in message:
                raise CallNotFound(message)
            if "not active" in message:
                raise CallNotActive(message)
            if "missing" in message:
                if "params" in message:
                    raise MissingCallingParameters(
                        str(message + res.json().get("params", "")))
                raise MissingCallingParameters(message)
            if res.status_code == 409:
                raise InvalidState(message)
        return dumps(res.json())
