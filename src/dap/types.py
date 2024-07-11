from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class Breakpoint(BaseModel):
    id: int = Field(..., description="Breakpoint ID.")
    verified: bool = Field(
        ...,
        description="If true, the breakpoint could be set (but not necessarily at the desired location",
    )
    message: Optional[str] = Field(
        None,
        description="A message about the state of the breakpoint"
        + "This is shown to the user and can be used to explain why a breakpoint could not be verified.",
    )
    source: Optional[Source] = Field(
        None, description="The source where the breakpoint is located."
    )
    line: Optional[int] = Field(
        None,
        description="The start line of the actual range covered by the breakpoint.",
    )
    column: Optional[int] = Field(
        None,
        description="Start position of the source range covered by the breakpoint.",
    )
    endLine: Optional[int] = Field(
        None, description="The end line of the actual range covered by the breakpoint."
    )
    endColumn: Optional[int] = Field(
        None, description="End position of the source range covered by the breakpoint."
    )
    instructionReference: Optional[str] = Field(
        None, description="A memory reference to where the breakpoint is set."
    )
    offset: Optional[int] = Field(
        None, description="The offset from the instruction reference."
    )
    reason: Optional[Literal["pending", "failed"]] = Field(
        None,
        description="A machine-readable explanation of why a breakpoint may not be verified.",
    )


class BreakpointLocation(BaseModel):
    line: int = Field(..., description="Start line of the breakpoint location.")
    column: Optional[int] = Field(
        None, description="Start column of the breakpoint location."
    )
    endLine: Optional[int] = Field(
        None, description="End line of the breakpoint location."
    )
    endColumn: Optional[int] = Field(
        None, description="End column of the breakpoint location."
    )


BreakpointModeApplicability = Union[
    Literal["source", "exception", "data", "instruction"], str
]


class BreakpointMode(BaseModel):
    mode: str = Field(..., description="The breakpoint mode.")
    label: str = Field(..., description="A label for the mode.")
    description: Optional[str] = Field(None, description="A description of the mode.")
    appliesTo: BreakpointModeApplicability = Field(
        ..., description="The breakpoint mode applicability."
    )


class Capabilities(BaseModel):
    supportsConfigurationDoneRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `configurationDone` request."
    )
    supportsFunctionBreakpoints: Optional[bool] = Field(
        None, description="The debug adapter supports function breakpoints."
    )
    supportsConditionalBreakpoints: Optional[bool] = Field(
        None, description="The debug adapter supports conditional breakpoints."
    )
    supportsHitConditionalBreakpoints: Optional[bool] = Field(
        None,
        description="The debug adapter supports breakpoints that break execution after a specified number of hits.",
    )
    supportsEvaluateForHovers: Optional[bool] = Field(
        None,
        description="The debug adapter supports a (side effect free) `evaluate` request for data hovers.",
    )
    exceptionBreakpointFilters: Optional[List[ExceptionBreakpointsFilter]] = Field(
        None,
        description="Available exception filter options for the `setExceptionBreakpoints` request.",
    )
    supportsStepBack: Optional[bool] = Field(
        None,
        description="The debug adapter supports stepping back via the `stepBack` and `reverseContinue` requests.",
    )
    supportsSetVariable: Optional[bool] = Field(
        None, description="The debug adapter supports setting a variable to a value."
    )
    supportsRestartFrame: Optional[bool] = Field(
        None, description="The debug adapter supports restarting a frame."
    )
    supportsGotoTargetsRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `gotoTargets` request."
    )
    supportsStepInTargetsRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `stepInTargets` request."
    )
    supportsCompletionsRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `completions` request."
    )
    completionTriggerCharacters: Optional[List[str]] = Field(
        None,
        description="The set of characters that should trigger completion in a REPL."
        " If not specified, the UI should assume the `.` character.",
    )
    supportsModulesRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `modules` request."
    )
    additionalModuleColumns: Optional[List[ColumnDescriptor]] = Field(
        None,
        description="The set of additional module information exposed by the debug adapter.",
    )
    supportedChecksumAlgorithms: Optional[List[ChecksumAlgorithm]] = Field(
        None,
        description="Checksum algorithms supported by the debug adapter.",
    )
    supportsRestartRequest: Optional[bool] = Field(
        None,
        description="The debug adapter supports the `restart` request."
        "In this case a client should not implement `restart` by terminating and"
        "relaunching the adapter but by calling the `restart` request.",
    )
    supportsExceptionOptions: Optional[bool] = Field(
        None,
        description="The debug adapter supports `exceptionOptions` on the `setExceptionBreakpoints` request.",
    )
    supportsValueFormattingOptions: Optional[bool] = Field(
        None,
        description="The debug adapter supports a `format` attribute on the `stackTrace`,"
        " `variables`, and `evaluate` requests.",
    )
    supportsExceptionInfoRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `exceptionInfo` request."
    )
    supportTerminateDebuggee: Optional[bool] = Field(
        None,
        description="The debug adapter supports the `terminateDebuggee` attribute on the `disconnect` request.",
    )
    supportSuspendDebuggee: Optional[bool] = Field(
        None,
        description="The debug adapter supports the `suspendDebuggee` attribute on the `disconnect` request.",
    )
    supportsDelayedStackTraceLoading: Optional[bool] = Field(
        None,
        description="The debug adapter supports the delayed loading of parts of the stack,"
        " which requires that both the `startFrame` and `levels` arguments and the `totalFrames` result "
        "of the `stackTrace` request are supported.",
    )
    supportsLoadedSourcesRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `loadedSources` request."
    )
    supportsLogPoints: Optional[bool] = Field(
        None,
        description="The debug adapter supports log points by interpreting the"
        " `logMessage` attribute of the `SourceBreakpoint`.",
    )
    supportsTerminateThreadsRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `terminateThreads` request."
    )
    supportsSetExpression: Optional[bool] = Field(
        None, description="The debug adapter supports the `setExpression` request."
    )
    supportsTerminateRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `terminate` request."
    )
    supportsDataBreakpoints: Optional[bool] = Field(
        None, description="The debug adapter supports data breakpoints."
    )
    supportsReadMemoryRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `readMemory` request."
    )
    supportsWriteMemoryRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `writeMemory` request."
    )
    supportsDisassembleRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `disassemble` request."
    )
    supportsCancelRequest: Optional[bool] = Field(
        None, description="The debug adapter supports the `cancel` request."
    )
    supportsBreakpointLocationsRequest: Optional[bool] = Field(
        None,
        description="The debug adapter supports the `breakpointLocations` request.",
    )
    supportsClipboardContext: Optional[bool] = Field(
        None,
        description="The debug adapter supports the `clipboard` context value in the `evaluate` request.",
    )
    supportsSteppingGranularity: Optional[bool] = Field(
        None,
        description="The debug adapter supports stepping granularities (argument `granularity`) for the stepping requests.",
    )
    supportsInstructionBreakpoints: Optional[bool] = Field(
        None,
        description="The debug adapter supports adding breakpoints based on instruction references.",
    )
    supportsExceptionFilterOptions: Optional[bool] = Field(
        None,
        description="The debug adapter supports `filterOptions` as an argument on the `setExceptionBreakpoints` request.",
    )
    supportsSingleThreadExecutionRequests: Optional[bool] = Field(
        None,
        description="The debug adapter supports the `singleThread` property on the execution requests"
        " (`continue`, `next`, `stepIn`, `stepOut`, `reverseContinue`, `stepBack`).",
    )
    supportsDataBreakpointBytes: Optional[bool] = Field(
        None,
        description="The debug adapter supports the `asAddress` and `bytes` fields in the `dataBreakpointInfo` request.",
    )
    breakpointModes: Optional[List[BreakpointMode]] = Field(
        None,
        description="Modes of breakpoints supported by the debug adapter, such as 'hardware' or 'software'. "
        "If present, the client may allow the user to select a mode and include it in its `setBreakpoints` request. "
        "Clients may present the first applicable mode in this array as the 'default' mode in gestures that set breakpoints.",
    )


ChecksumAlgorithm = Literal["MD5", "SHA1", "SHA256", "timestamp"]


class Checksum(BaseModel):
    algorithm: ChecksumAlgorithm = Field(
        ..., description="The algorithm used to calculate the checksum."
    )
    checksum: str = Field(
        ..., description="Value of the checksum, encoded as a hexadecimal value."
    )


class ColumnDescriptor(BaseModel):
    attributeName: str = Field(
        ..., description="Name of the attribute rendered in this column."
    )
    label: str = Field(..., description="Header UI label of column.")
    format: Optional[str] = Field(
        None, description="Format to use for the rendered values in this column."
    )
    type: Optional[Literal["string", "number", "boolean", "unixTimestampUTC"]] = Field(
        None,
        description="Datatype of values in this column. Defaults to `string` if not specified.",
    )
    width: Optional[int] = Field(
        None, description="Width of this column in characters (hint only)."
    )


CompletionItemType = Literal[
    "method",
    "function",
    "constructor",
    "field",
    "variable",
    "class",
    "interface",
    "module",
    "property",
    "unit",
    "value",
    "enum",
    "keyword",
    "snippet",
    "text",
    "color",
    "file",
    "reference",
    "customcolor",
]


class CompletionItem(BaseModel):
    label: str = Field(..., description="The label of this completion item.")
    text: Optional[str] = Field(
        None,
        description="If text is returned and not an empty string, then it is inserted instead of the label.",
    )
    sortText: Optional[str] = Field(
        None,
        description="A string that should be used when comparing this item with other items.",
    )
    detail: Optional[str] = Field(
        None,
        description="A human-readable string with additional information about this item.",
    )
    type: Optional[CompletionItemType] = Field(None, description="The item's type.")
    start: Optional[int] = Field(
        None, description="Start position where the completion text is added."
    )
    length: Optional[int] = Field(
        None,
        description="Length determines how many characters are overwritten by the completion text.",
    )
    selectionStart: Optional[int] = Field(
        None,
        description="Determines the start of the new selection after the text has been inserted.",
    )
    selectionLength: Optional[int] = Field(
        None,
        description="Determines the length of the new selection after the text has been inserted.",
    )


DataBreakpointAccessType = Literal["read", "write", "readWrite"]


class DataBreakpoint(BaseModel):
    dataId: str = Field(
        ...,
        description="An id representing the data. This id is returned from the `dataBreakpointInfo` request.",
    )
    accessType: Optional[DataBreakpointAccessType] = Field(
        None, description="The access type of the data."
    )
    condition: Optional[str] = Field(
        None, description="An expression for conditional breakpoints."
    )
    hitCondition: Optional[str] = Field(
        None,
        description="An expression that controls how many hits of the breakpoint are ignored.",
    )
