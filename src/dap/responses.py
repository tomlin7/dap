from pydantic import Field

from .base import Response, ResponseBody
from .types import *

# Reverse Request Responses


class RunInTerminalResponseBody(ResponseBody):
    """Body of a 'runInTerminal' response."""

    processId: Optional[int] = Field(
        None, description="The process ID of the terminal."
    )
    shellProcessId: Optional[int] = Field(
        None, description="The process ID of the shell."
    )


class RunInTerminalResponse(Response):
    """Response to 'runInTerminal' request."""

    request_seq: int = Field(
        ..., description="Sequence number of the corresponding request."
    )
    success: bool = Field(
        ..., description="Indicates whether the request was successful."
    )
    command: str = "runInTerminal"
    body: RunInTerminalResponseBody


class StartDebuggingResponse(Response):
    """Body of a 'startDebugging' response."""

    request_seq: int = Field(
        ..., description="Sequence number of the corresponding request."
    )
    success: bool = Field(
        ..., description="Indicates whether the request was successful."
    )
    command: str = "startDebugging"


# Request Responses
class Cancelled(Response):
    """Response to 'cancel' request."""

    ...


class Attached(Response):
    """Response to 'attach' request."""

    ...


class BreakpointLocationsResponse(ResponseBody):
    """Body of a 'breakpointLocations' response."""

    breakpoints: list[BreakpointLocation] = Field(
        ..., description="List of breakpoints."
    )


class CompletionsResponse(ResponseBody):
    """Body of a 'completions' response."""

    targets: list[CompletionItem] = Field(..., description="List of completion items.")


class ConfigurationDone(Response):
    """Response to 'configurationDone' request."""

    ...


class Continued(ResponseBody):
    """Body of a 'continue' response."""

    allThreadsContinued: Optional[bool] = Field(
        None, description="If all threads were continued."
    )


class DataBreakpointInfoResponse(ResponseBody):
    """Body of a 'dataBreakpoint' response."""

    dataId: Optional[str] = Field(
        None, description="An identifier for the data breakpoint."
    )
    description: str = Field(
        ..., description="A user-visible description of the breakpoint."
    )
    accessTypes: Optional[list[DataBreakpointAccessType]] = Field(
        None, description="The access types of the data breakpoint."
    )
    canPersist: Optional[bool] = Field(
        None, description="Whether the data breakpoint can be persisted."
    )


class DisassembleResponse(ResponseBody):
    """Body of a 'disassemble' response."""

    instructions: list[DisassembledInstruction] = Field(
        ..., description="List of disassembled instructions."
    )


class Disconnected(Response):
    """Response to 'disconnect' request."""

    ...


class EvaluateResponse(ResponseBody):
    """Body of an 'evaluate' response."""

    result: str = Field(..., description="The result of the evaluation.")
    type: Optional[str] = Field(None, description="The type of the result.")
    presentationHint: Optional[VariablePresentationHint] = Field(
        None, description="The presentation hint of the result."
    )
    variablesReference: int = Field(
        ...,
        description="The reference to the variables of the evaluation result.",
    )
    namedVariables: Optional[int] = Field(
        None, description="The number of named variables."
    )
    indexedVariables: Optional[int] = Field(
        None, description="The number of indexed variables."
    )
    memoryReference: Optional[str] = Field(
        None, description="The memory reference of the result."
    )


class ExceptionInfoResponse(ResponseBody):
    exceptionID: str = Field(..., description="The exception ID.")
    description: Optional[str] = Field(
        None, description="The description of the exception."
    )
    breakMode: ExceptionBreakMode = Field(
        ..., description="The break mode of the exception."
    )
    details: Optional[ExceptionDetails] = Field(
        None, description="The details of the exception."
    )


class GotoDone(Response):
    """Response to 'goto' request."""

    ...


class GotoTargetsResponse(ResponseBody):
    """Body of a 'gotoTargets' response."""

    targets: list[GotoTarget] = Field(..., description="List of goto targets.")


class Initialized(Capabilities):
    """Response to 'initialize' request."""

    ...


class LaunchDone(Response):
    """Response to 'launch' request."""

    ...


class LoadedSourcesResponse(ResponseBody):
    """Body of a 'loadedSources' response."""

    sources: list[Source] = Field(..., description="List of loaded sources.")


class ModulesResponse(ResponseBody):
    """Body of a 'modules' response."""

    modules: list[Module] = Field(..., description="List of modules.")
    totalModules: Optional[int] = Field(
        None, description="The total number of modules."
    )


class NextResponse(Response):
    """Response to 'next' request."""

    ...


class Paused(Response):
    """Response to 'pause' request."""

    ...


class ReadMemoryResponse(ResponseBody):
    """Body of a 'readMemory' response."""

    address: str = Field(..., description="The address of the memory read.")
    unreadableBytes: Optional[int] = Field(
        None, description="The number of unreadable bytes."
    )
    data: Optional[str] = Field(None, description="The data read from memory.")


class Restarted(Response):
    """Response to 'restart' request."""

    ...


class RestartFrameDone(Response):
    """Response to 'restartFrame' request."""

    ...


class ReverseContinueDone(Response):
    """Response to 'reverseContinue' request."""

    ...


class ScopesResponse(ResponseBody):
    """Body of a 'scopes' response."""

    scopes: list[Scope] = Field(..., description="List of scopes.")


class SetBreakpointsResponse(ResponseBody):
    """Body of a 'setBreakpoints' response."""

    breakpoints: list[Breakpoint]


class SetDataBreakpointsResponse(ResponseBody):
    """Body of a 'setDataBreakpoints' response."""

    breakpoints: list[Breakpoint]


class SetExceptionBreakpointsResponse(ResponseBody):
    """Body of a 'setExceptionBreakpoints' response."""

    breakpoints: list[ExceptionBreakpointsFilter]


class SetExceptionBreakpointsResponse(Response):
    """Response to 'setExceptionBreakpoints' request."""

    ...


class SetExpressionResponse(ResponseBody):
    """Body of a 'setExpression' response."""

    value: str = Field(..., description="The value of the expression.")
    type: Optional[str] = Field(None, description="The type of the expression.")
    presentationHint: Optional[VariablePresentationHint] = Field(
        None, description="The presentation hint of the expression."
    )
    variablesReference: Optional[int] = Field(
        None,
        description="The reference to the variables of the expression result.",
    )
    namedVariables: Optional[int] = Field(
        None, description="The number of named variables."
    )
    indexedVariables: Optional[int] = Field(
        None, description="The number of indexed variables."
    )
    memoryReference: Optional[str] = Field(
        None, description="The memory reference of the expression."
    )


class SetFunctionBreakpointsResponse(ResponseBody):
    """Body of a 'setFunctionBreakpoints' response."""

    breakpoints: list[FunctionBreakpoint] = Field(
        ..., description="List of function breakpoints."
    )


class SetInstructionBreakpointsResponse(ResponseBody):
    """Body of a 'setInstructionBreakpoints' response."""

    breakpoints: list[Breakpoint]


class SetVariableResponse(ResponseBody):
    """Body of a 'setVariable' response."""

    value: str = Field(..., description="The value of the variable.")
    type: Optional[str] = Field(None, description="The type of the variable.")
    variablesReference: Optional[int] = Field(
        None,
        description="The reference to the variables of the variable result.",
    )
    namedVariables: Optional[int] = Field(
        None, description="The number of named variables."
    )
    indexedVariables: Optional[int] = Field(
        None, description="The number of indexed variables."
    )
    memoryReference: Optional[str] = Field(
        None, description="The memory reference of the variable."
    )


class SourceResponse(ResponseBody):
    """Body of a 'source' response."""

    content: str = Field(..., description="The content of the source.")
    mimeType: Optional[str] = Field(None, description="The MIME type of the source.")


class StackTraceResponse(ResponseBody):
    """Body of a 'stackTrace' response."""

    stackFrames: list[StackFrame] = Field(..., description="List of stack frames.")
    totalFrames: Optional[int] = Field(None, description="The total number of frames.")


class StepBackDone(Response):
    """Response to 'stepBack' request."""

    ...


class StepInDone(Response):
    """Response to 'stepIn' request."""

    ...


class StepInTargetsResponse(ResponseBody):
    """Body of a 'stepInTargets' response."""

    targets: list[StepInTarget] = Field(..., description="List of step in targets.")


class StepOutDone(Response):
    """Response to 'stepOut' request."""

    ...


class Terminated(Response):
    """Response to 'terminate' request."""

    ...


class TerminateThreadsDone(Response):
    """Response to 'terminateThreads' request."""

    ...


class ThreadsResponse(ResponseBody):
    """Body of a 'threads' response."""

    threads: list[Thread] = Field(..., description="List of threads.")


class VariablesResponse(ResponseBody):
    """Body of a 'variables' response."""

    variables: list[Variable] = Field(..., description="List of variables.")


class WriteMemoryResponse(ResponseBody):
    """Body of a 'writeMemory' response."""

    offset: Optional[int] = Field(None, description="The offset of the memory write.")
    bytesWritten: Optional[int] = Field(
        None, description="The number of bytes written."
    )
