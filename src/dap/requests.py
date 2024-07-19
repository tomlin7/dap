from enum import StrEnum
from typing import Optional, TypedDict


class AttachRequestArguments(TypedDict):
    """Arguments for 'attach' request."""

    __restart: Optional[bool] = None


class LaunchRequestArguments(TypedDict):
    """Arguments for 'launch' request."""

    noDebug: Optional[bool] = None
    __restart: Optional[bool] = None
