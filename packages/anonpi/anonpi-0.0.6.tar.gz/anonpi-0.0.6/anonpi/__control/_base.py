import typing as t
from ._api import apibaserequest
from ..__resources._endpoints import AnonEndpoints
from json import loads, dumps
from ..__resources.__exceptions import CallNotActive, CallNotFound




class callcontrol:
    def __init__(self, event:t.Union[str , None], token: t.Union[str,None], **kwargs):
        self._kwargs = kwargs
        self._token = token
        self._event = event
        

    def _check_call_status(self):
        calluuid = self._kwargs["calluuid"]
        return str(apibaserequest(
            "get",
            AnonEndpoints("status"),
            self._token,
            calluuid=calluuid
        ))

    def __repr__(self):
        if self._event == "record_get":
            __D = (str(apibaserequest(
                "get",
                AnonEndpoints("record_get"),
                self._token,
                calluuid=self._kwargs["calluuid"]
            )))
            if loads(__D).get("status", "error") == "error":
                raise CallNotFound(loads(__D).get("message", "Call not found"))
            else:
                return __D

        if self._event == "status":
            return str(self._check_call_status())
        else:
            return str(apibaserequest(
                    "post",
                    AnonEndpoints(self._event),
                    self._token,
                    **self._kwargs
            ))

