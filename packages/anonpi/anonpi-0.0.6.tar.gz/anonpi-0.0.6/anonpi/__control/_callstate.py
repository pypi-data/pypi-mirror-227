from ._base import callcontrol
from json import loads
import typing as t
from ..__resources.__exceptions import *
from ._recording import Recording
from ..__resources.languages import Language

def check_audio_url(url):
    if not url.startswith("http"):
        return False
    if not "://" in url:
        return False
    return True

class AnonCall:
    """# AnonCall class for handling call
        Usage:
        >>> call:AnonCall = anonapi.get_call("calluuid")
        >>> call.uuid -> str
        >>> call.playback_audio("https://example.com/audio.mp3")
        >>> call.playback_text() -> None
        >>> call.playback_stop() -> None
        >>> call.hangup() -> None
        >>> call.status() -> bool
        >>> call.hold() -> None
        >>> call.unhold() -> None
        >>> call.record_start() -> None
        >>> call.record_stop() -> None
        >>> call.get_recording() -> Recording

        Raises:
        ```python
            InvalidParameter: If calluuid is not valid
            TokenRequired: If token is not provided
            CallNotActive: If call is not active
            CallNotFound: If call is not found
            Exception: If any other error occurs
        ```
        """

    def __init__(self, **d):
        self._calluuid = d.get("calluuid")
        self._token = d.get("token")
        if not self._calluuid:
            raise InvalidParameter(
                "calluuid is required to create AnonCall instance")
        if not self._token:
            raise TokenRequired(
                "token is required to create AnonCall instance")
        else:
            pass
        
    def __repr__(self):
        return "<{0.__class__.__name__} {1} >".format(
            self,
            " ".join(
                f'{attr}={getattr(self, attr) if getattr(self, attr) != "" else "None"}'
                for attr in dir(self)
                if not attr.startswith('__')
                and isinstance(getattr(self, attr), str)
            )
        )

    def __str__(self):
        return "<{0.__class__.__name__} {1} >".format(
            self,
            " ".join(
                f'{attr}={getattr(self, attr) if getattr(self, attr) != "" else "None"}'
                for attr in dir(self)
                if not attr.startswith('__')
                and isinstance(getattr(self, attr), str)
            )
        )


    @property
    def to_dict(self) -> dict:
        """Get call status as dict"""
        return self.___call_status

    @property
    def uuid(self) -> str:
        """Get calluuid of the call"""
        return self._calluuid
    
    @property
    def from_number(self) -> str:
        """Get from_number of the call"""
        return self.___call_status.get("data").get("from_number")
    
    @property
    def to_number(self) -> str:
        """Get to_number of the call"""
        return self.___call_status.get("data").get("to_number")
    
    @property
    def callback_url(self) -> str:
        """Get callback_url of the call"""
        return self.___call_status.get("data").get("callback_url")

    @property
    def status(self) -> dict:
        """Get call status
        """
        __ =  str(callcontrol(
            "status",
            self._token,
            calluuid=self._calluuid
        ))

        if loads(__).get("status","error") == "error":
            message = loads(__).get("message","Unknown error occured")
            if "not found" in message.lower():
                raise CallNotFound(message)
            elif "not active" in message.lower():
                raise CallNotActive(message)
            else:
                raise Exception("Error: " + message)
        else:
            if loads(__).get("status") == "active":
                _data = {
                    "status":True,
                    "calluuid":loads(__).get("calluuid"),
                    "to_number":loads(__).get("to_number"),
                    "from_number":loads(__).get("from_number"),
                }
                return _data
            else:
                _data = {
                    "status":False,
                    "calluuid":loads(__).get("calluuid"),
                    "to_number":loads(__).get("to_number"),
                    "from_number":loads(__).get("from_number"),
                }
                return _data

    def hangup(self):
        """Hangup the call"""
        __ = str(
            callcontrol(
                "hangup_call",
                self._token,
                calluuid=self._calluuid
            )
        )
        return None

    def hold(self):
        """Hold the call"""
        __ = str(callcontrol(
            "hold",
            self._token,
            calluuid=self._calluuid
        ))
        return None

    def unhold(self):
        """Unhold the call"""
        __ = str(callcontrol(
            "unhold",
            self._token,
            calluuid=self._calluuid
        ))
        return None

    def playback_start_audio(self, audio_url: t.Union[str, None] = None)->None:
        """### Start playback of audio

        #### Args:
            `audio_url` str: Audio url to be played

        #### Raises:
            `CallNotActive`: If call is not active
        """
        if not check_audio_url(audio_url):
            raise InvalidAudioURL("Invalid audio url provided")
        __ = str(callcontrol(
            "playback_audio_start",
            self._token,
            calluuid=self._calluuid,
            audio_url=audio_url
        ))
        return None

    def speak(self, text: str, lang: t.Union[Language , str] = Language.english):
        """Speak text to call

        Args:
            text (str): Text prompt to be spoken to the call

            lang (Language, str): [anonpi.Language] Defaults to anonpi.Language.english
        """
        __ = str(callcontrol(
            "playback_text_start",
            self._token,
            calluuid=self._calluuid,
            text=text,
            lang=lang
        ))
        return None

    def stop_speaking(self):
        """Stop speaking text to the call"""
        __ = str(callcontrol(
            "playback_text_stop",
            self._token,
            calluuid=self._calluuid
        ))
        return None

    def playback_stop(self):
        """Stop playback of audio"""
        __ = str(callcontrol(
            "playback_stop",
            self._token,
            calluuid=self._calluuid
        ))
        return None

    def record_start(self):
        """Start recording the call"""
        __ = str(callcontrol(
            "record_start",
            self._token,
            calluuid=self._calluuid
        ))
        return None

    def record_stop(self):
        """Stop recording the call"""
        __ = str(callcontrol(
            "record_stop",
            self._token,
            calluuid=self._calluuid
        ))
        return None

    def get_recording(self) -> Recording:
        """### Get recording of the call
        
        #### Returns:
            Recording: Recording object
        """
        __ = loads(str(callcontrol(
            "record_get",
            self._token,
            calluuid=self._calluuid
        )))
        return Recording(**__)

    def pause_recording(self):
        return callcontrol(
            "record_pause",
            self._token,
            calluuid=self._calluuid
        )

    def resume_recording(self):
        """### Resume recording the call"""
        return callcontrol(
            "record_resume",
            self._token,
            calluuid=self._calluuid
        )

    def gather_using_audio(self,
                           *,
                           dtmf_count: t.Optional[int] = None,
                           terminating_digit: t.Optional[str] = None,
                           audio_url: t.Union[str,None])->None:
        """### Gather Dtmf Using Audio

        #### Args:
            `dtmf_count` (t.Optional[int], optional) : Number of dtmf to be collected. Defaults to None.
            
            `terminating_digit` (t.Optional[str], optional): Dtmf to terminate the gather. Defaults to None.
            
            `audio_url` (t.Union[str], optional): Audio url to be played while gathering dtmf. Defaults to None.

        #### Returns:
            None
        """
        return str(callcontrol(
            "gather_using_audio",
            self._token,
            calluuid=self._calluuid,
            dtmf_count=dtmf_count,
            terminating_digit=terminating_digit,
            audio_url=audio_url
        ))

    def gather_using_speak(self,
                    *,
                    dtmf_count: t.Optional[int] = None,
                    terminating_digits: t.Optional[str] = None,
                    text: t.Union[str, None] = None,
                    lang: t.Union[Language , str] = "en"):
        """## Gather Dtmf Using Speak

        #### Args:
            `dtmf_count` (t.Optional[int], optional) : Number of dtmf to be collected. Defaults to None.
            
            `terminating_digits` (t.Optional[str], optional): Dtmf to terminate the gather. Defaults to None.
            
            `text` (t.Union[str], optional): Text to be spoken while gathering dtmf. Defaults to None.

            `lang` (t.Union[Language , str], optional): Language to be spoken. Defaults to "en".
        
        #### Raises:
            InvalidParameter: If invalid language is provided

        #### Returns:
            None
        """
        if lang not in list(Language()):
            raise InvalidParameter(f"Invalid language {lang}")
        return str(callcontrol(
            "gather_using_text",
            self._token,
            calluuid=self._calluuid,
            dtmf_count=dtmf_count,
            terminating_digits=terminating_digits,
            text=text,
            lang=lang
        ))