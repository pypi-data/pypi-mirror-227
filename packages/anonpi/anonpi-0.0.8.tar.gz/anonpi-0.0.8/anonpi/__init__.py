"""
anonpi: Python Module for Calling Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The "anonpi" module is a powerful Python package that provides a convenient interface for interacting with calling systems. It simplifies the development of applications that require functionalities such as machine detection, IVR (Interactive Voice Response), DTMF (Dual-Tone Multi-Frequency) handling, recording, playback, and more.
"""

from .call import (
    AnonApi,
    AnonCall,
)
from .resources.languages import (
    Language,
)
from .version import (
    version
)
__version__ = version
__name__ = "anonpi"
__slots__ = ["AnonApi","AnonCall","Language"]
__all__ = [
    'AnonApi',
    'AnonCall',
    'Language',
]
