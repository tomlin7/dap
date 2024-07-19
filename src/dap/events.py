from pydantic import Field

from .base import EventBody
from .types import *


class BreakpointEvent(EventBody):
    """Event sent when a breakpoint is hit."""

    reason: Literal["changed", "new", "removed"] | str = Field(
        ...,
        description="The reason the event was sent. 'changed' for a changed breakpoint, 'new' for a new breakpoint, 'removed' for a removed breakpoint.",
    )
    breakpoint: Breakpoint = Field(..., description="The breakpoint that was hit.")


class CapabilitiesEvent(EventBody):
    """Event sent when capabilities are requested."""

    capabilities: Capabilities = Field(
        ..., description="The capabilities of the debug adapter."
    )


class ContinuedEvent(EventBody):
    """Event sent when the execution is continued."""

    threadId: int = Field(..., description="The thread that continued.")
    allThreadsContinued: Optional[bool] = Field(
        None,
        description="If all threads continued, the attribute is omitted. If a specific thread continued, the attribute contains the thread ID.",
    )


class ExitedEvent(EventBody):
    """Event sent when the debuggee has exited."""

    exitCode: int = Field(..., description="The exit code of the debuggee.")


class InitializedEvent(EventBody):
    """Event sent when the debug adapter is initialized."""

    ...


class InvalidatedEvent(EventBody):
    """Event sent when breakpoints are invalidated."""

    areas: Optional[list[InvalidatedAreas]] = Field(
        None, description="The invalidated areas."
    )
    threadId: Optional[int] = Field(
        None,
        description="The thread ID of the invalidated areas. If omitted, the invalidated areas are not specific to a thread.",
    )
    stackFrameId: Optional[int] = Field(
        None,
        description="The stack frame ID of the invalidated areas. If omitted, the invalidated areas are not specific to a stack frame.",
    )


class LoadedSourceEvent(EventBody):
    """Event sent when a source is loaded."""

    reason: Literal["new", "changed", "removed"] = Field(
        ...,
        description="The reason the event was sent. 'new' for a new source, 'changed' for a changed source, 'removed' for a removed source.",
    )
    source: Source = Field(..., description="The source that was loaded.")


class MemoryEvent(EventBody):
    """Event sent when memory is accessed."""

    memoryReference: str = Field(..., description="The memory reference.")
    offset: int = Field(..., description="The memory offset.")
    count: int = Field(..., description="The number of bytes.")


class ModuleEvent(EventBody):
    """Event sent when a module is loaded or unloaded."""

    reason: Literal["new", "changed", "removed"] = Field(
        ...,
        description="The reason the event was sent. 'new' for a new module, 'changed' for a changed module, 'removed' for a removed module.",
    )
    module: Module = Field(..., description="The module that was loaded or unloaded.")


class OutputEvent(EventBody):
    """Event sent when output is produced."""

    category: Optional[
        Literal["console", "important", "stdout", "stderr", "telemetry"] | str
    ] = Field(
        ...,
        description="The category of the output.",
    )
    output: str = Field(..., description="The output text.")
    group: Optional[Literal["start", "startCollapsed", "end"]] = Field(
        None,
        description="The output group.",
    )
    variablesReference: Optional[int] = Field(
        None,
        description="The reference to a variable.",
    )
    source: Optional[Source] = Field(
        None,
        description="The source of the output.",
    )
    line: Optional[int] = Field(
        None,
        description="The line of the output.",
    )
    column: Optional[int] = Field(
        None,
        description="The column of the output.",
    )
    data: Optional[Any] = Field(None, description="Additional data.")


class ProcessEvent(EventBody):
    """Event sent when a process is created or exited."""

    name: str = Field(..., description="The name of the process.")
    systemProcessId: Optional[int] = Field(
        None,
        description="The system process ID.",
    )
    isLocalProcess: Optional[bool] = Field(
        None,
        description="If the process is local.",
    )
    startMethod: Optional[Literal["launch", "attach", "attachForSuspendedLaunch"]] = (
        Field(
            None,
            description="The start method.",
        )
    )
    pointerSize: Optional[int] = Field(
        None,
        description="The pointer size.",
    )


class ProgressEndEvent(EventBody):
    """Event sent when a progress ends."""

    progressId: str = Field(..., description="The progress ID.")
    message: Optional[str] = Field(None, description="The message.")


class ProgressStartEvent(EventBody):
    """Event sent when a progress starts."""

    progressId: str = Field(..., description="The progress ID.")
    title: str = Field(..., description="The title of the progress.")
    requestId: Optional[str] = Field(
        None,
        description="The request ID.",
    )
    cancellable: Optional[bool] = Field(
        None,
        description="If the progress is cancellable.",
    )
    message: Optional[str] = Field(None, description="The message.")
    percentage: Optional[int] = Field(
        None,
        description="The percentage of the progress.",
    )


class ProgressUpdateEvent(EventBody):
    """Event sent when a progress updates."""

    progressId: str = Field(..., description="The progress ID.")
    message: Optional[str] = Field(None, description="The message.")
    percentage: Optional[int] = Field(
        None,
        description="The percentage of the progress.",
    )


class StoppedEvent(EventBody):
    """Event sent when the execution is stopped."""

    reason: Literal[
        "step",
        "breakpoint",
        "exception",
        "pause",
        "entry",
        "goto",
        "function breakpoint",
        "data breakpoint",
        "instruction breakpoint",
    ] = Field(
        ...,
        description="The reason the execution was stopped.",
    )
    description: Optional[str] = Field(
        None,
        description="The description of the stop event.",
    )
    threadId: Optional[int] = Field(
        None,
        description="The thread that stopped.",
    )
    preserveFocusHint: Optional[bool] = Field(
        None,
        description="If the focus should be preserved.",
    )
    text: Optional[str] = Field(
        None,
        description="The text of the stop event.",
    )
    allThreadsStopped: Optional[bool] = Field(
        None,
        description="If all threads stopped, the attribute is omitted. If a specific thread stopped, the attribute contains the thread ID.",
    )
    hitBreakpointIds: Optional[list[str]] = Field(
        None,
        description="The hit breakpoint IDs.",
    )


class TerminatedEvent(EventBody):
    """Event sent when the debuggee is terminated."""

    restart: Optional[bool] = Field(
        None,
        description="If the debuggee should be restarted.",
    )


class ThreadEvent(EventBody):
    """Event sent when a thread is created or exited."""

    reason: Literal["started", "exited"] | str = Field(
        ...,
        description="The reason the event was sent. 'started' for a started thread, 'exited' for an exited thread.",
    )
    threadId: int = Field(..., description="The thread ID.")
