from enum import StrEnum
from typing import Optional, TypedDict


class AttachRequestArguments(TypedDict):
    """Arguments for 'attach' request."""

    __restart: Optional[bool] = None


class LaunchRequestArguments(TypedDict):
    """Arguments for 'launch' request."""

    noDebug: Optional[bool] = None
    __restart: Optional[bool] = None


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
