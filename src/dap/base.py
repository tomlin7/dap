from enum import StrEnum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

from .types import Message


class ProtocolMessage(BaseModel):
    """Base class of requests, responses, and events"""

    seq: int = Field(..., description="Sequence number (message ID) of the message.")
    type: Literal["request", "response", "event"] | str = Field(
        ..., description="Message type."
    )


class Request(ProtocolMessage):
    type: str = "request"  # type: ignore
    command: str = Field(..., description="The command to execute.")
    arguments: Optional[Any] = Field(
        None, description="Object containing arguments for the command."
    )


class EventBody(BaseModel):
    """Base class of event bodies"""

    ...


class Event(ProtocolMessage):
    type: str = "event"
    event: str = Field(..., description="The event type.")
    body: Optional[dict[str, Any] | Any] = Field(
        None, description="Event-specific information."
    )


class ResponseBody(BaseModel):
    """Base class of response bodies"""

    ...


class Response(ProtocolMessage):
    type: str = "response"
    request_seq: int = Field(
        ..., description="Sequence number of the corresponding request."
    )
    success: bool = Field(
        ..., description="Indicates whether the request was successful."
    )
    command: str = Field(..., description="The command requested.")
    message: Optional[Literal["cancelled", "notStopped"] | str] = Field(
        None, description="Raw error message if success is False."
    )
    body: Optional[dict[str, Any] | Any] = Field(
        None, description="Request result if success is true, error details otherwise."
    )


class ErrorBody(BaseModel):
    error: Optional[Message] = Field(
        None,
        description="Error details.",
    )


class ErrorResponse(Response):
    body: ErrorBody = Field(..., description="A structured error message.")


class DAPMessage(StrEnum):
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"


class Requests(StrEnum):
    """Enumeration of DAP requests."""

    CANCEL = "cancel"
    ATTACH = "attach"
    BREAKPOINTLOCATIONS = "breakpointLocations"
    COMPLETIONS = "completions"
    CONFIGURATIONDONE = "configurationDone"
    CONTINUE = "continue"
    DATABREAKPOINTINFO = "dataBreakpointInfo"
    DISASSEMBLE = "disassemble"
    DISCONNECT = "disconnect"
    EVALUATE = "evaluate"
    EXCEPTIONINFO = "exceptionInfo"
    GOTO = "goto"
    GOTOTARGETS = "gotoTargets"
    INITIALIZE = "initialize"
    LAUNCH = "launch"
    LOADEDSOURCES = "loadedSources"
    MODULES = "modules"
    NEXT = "next"
    PAUSE = "pause"
    READMEMORY = "readMemory"
    RESTART = "restart"
    RESTARTFRAME = "restartFrame"
    REVERSECONTINUE = "reverseContinue"
    SCOPES = "scopes"
    SETBREAKPOINTS = "setBreakpoints"
    SETDATABREAKPOINTS = "setDataBreakpoints"
    SETEXCEPTIONBREAKPOINTS = "setExceptionBreakpoints"
    SETEXPRESSION = "setExpression"
    SETFUNCTIONBREAKPOINTS = "setFunctionBreakpoints"
    SETINSTRUCTIONBREAKPOINTS = "setInstructionBreakpoints"
    SETVARIABLE = "setVariable"
    SOURCE = "source"
    STACKTRACE = "stackTrace"
    STEPBACK = "stepBack"
    STEPIN = "stepIn"
    STEPINTARGETS = "stepInTargets"
    STEPOUT = "stepOut"
    TERMINATE = "terminate"
    TERMINATETHREADS = "terminateThreads"
    THREADS = "threads"
    VARIABLES = "variables"
    WRITEMEMORY = "writeMemory"


class Events(StrEnum):
    """Enumeration of DAP events."""

    BREAKPOINT = "breakpoint"
    CAPABILITIES = "capabilities"
    CONTINUED = "continued"
    EXITED = "exited"
    INITIALIZED = "initialized"
    INVALIDATED = "invalidated"
    LOADED_SOURCE = "loadedSource"
    MEMORY = "memory"
    MODULE = "module"
    OUTPUT = "output"
    PROCESS = "process"
    PROGRESS_END = "progressEnd"
    PROGRESS_START = "progressStart"
    PROGRESS_UPDATE = "progressUpdate"
    STOPPED = "stopped"
    TERMINATED = "terminated"
    THREAD = "thread"
