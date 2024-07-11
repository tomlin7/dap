from typing import Dict, Optional, Union

from .data import *


class DAPClient:
    def __init__(self):
        self._buffer = bytearray()
        self._seq = 0

    def send(self, command: str, arguments: Optional[Dict[str, any]] = None) -> bytes:
        """
        Create a message to send to the debug adapter.
        """
        ...

    def receive(self, data: bytes) -> Optional[DAPMessage]:
        """
        Receive a message from the debug adapter.
        """
        ...
