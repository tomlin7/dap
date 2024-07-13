from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

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


BreakpointModeApplicability = (
    Literal["source", "exception", "data", "instruction"] | str
)


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
        None, description="The debug adapter supports the `restart` request."
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
        description="Modes of breakpoints supported by the debug adapter, such as 'hardware' or 'software'. ",
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


class DisassembledInstruction(BaseModel):
    instructionBytes: Optional[str] = Field(
        None,
        description="Raw bytes representing the instruction and its operands, in an implementation-defined format.",
    )
    instruction: str = Field(
        ...,
        description="Text representing the instruction and its operands, in an implementation-defined format.",
    )
    symbol: Optional[str] = Field(
        None,
        description="Name of the symbol that corresponds with the location of this instruction, if any.",
    )
    location: Optional[Source] = Field(
        None,
        description="Source location that corresponds to this instruction, if any.",
    )
    line: Optional[int] = Field(
        None,
        description="The line within the source location that corresponds to this instruction, if any.",
    )
    column: Optional[int] = Field(
        None,
        description="The column within the line that corresponds to this instruction, if any.",
    )
    endLine: Optional[int] = Field(
        None,
        description="The end line of the range that corresponds to this instruction, if any.",
    )
    endColumn: Optional[int] = Field(
        None,
        description="The end column of the range that corresponds to this instruction, if any.",
    )
    presentationHint: Optional[Literal["normal", "invalid"]] = Field(
        None,
        description="A hint for how to present the instruction in the UI."
        " A value of `invalid` may be used to indicate this instruction is 'filler'"
        " and cannot be reached by the program. For example, unreadable memory addresses may be presented is 'invalid.'",
    )


ExceptionBreakMode = Literal["never", "always", "unhandled", "userUnhandled"]


class ExceptionBreakpointsFilter(BaseModel):
    filter: str = Field(
        ...,
        description="The internal ID of the filter option. This value is passed to the `setExceptionBreakpoints` request.",
    )
    label: str = Field(
        ..., description="The name of the filter option. This is shown in the UI."
    )
    description: Optional[str] = Field(
        None,
        description="A help text providing additional information about the exception filter. "
        "This string is typically shown as a hover and can be translated.",
    )
    default: Optional[bool] = Field(
        None,
        description="Initial value of the filter option. If not specified a value false is assumed.",
    )
    supportsCondition: Optional[bool] = Field(
        None,
        description="Controls whether a condition can be specified for this filter option. "
        "If false or missing, a condition can not be set.",
    )
    conditionDescription: Optional[str] = Field(
        None,
        description="A help text providing information about the condition. "
        "This string is shown as the placeholder text for a text box and can be translated.",
    )


class ExceptionDetails(BaseModel):
    message: Optional[str] = Field(
        None, description="Message contained in the exception."
    )
    typeName: Optional[str] = Field(
        None, description="Short type name of the exception object."
    )
    fullTypeName: Optional[str] = Field(
        None, description="Fully-qualified type name of the exception object."
    )
    evaluateName: Optional[str] = Field(
        None,
        description="An expression that can be evaluated in the current scope to obtain the exception object.",
    )
    stackTrace: Optional[str] = Field(
        None, description="Stack trace at the time the exception was thrown."
    )
    innerException: Optional[List[ExceptionDetails]] = Field(
        None,
        description="Details of the exception contained by this exception, if any.",
    )


class ExceptionFilterOptions(BaseModel):
    filterId: str = Field(
        ...,
        description="ID of the exception filter.",
    )
    condition: Optional[str] = Field(
        None, description="An expression for conditional exceptions."
    )
    mode: Optional[str] = Field(
        None,
        description="The mode of this exception breakpoint. "
        "If defined, this must be one of the `breakpointModes` the debug adapter advertised in its `Capabilities`.",
    )


class ExceptionOptions(BaseModel):
    path: Optional[List[ExceptionPathSegment]] = Field(
        None,
        description="A path that selects a single or multiple exceptions in a tree."
        "If `path` is missing, the whole tree is selected. "
        "By convention the first segment of the path is a category that is used to group exceptions in the UI.",
    )
    breakMode: Optional[ExceptionBreakMode] = Field(
        None, description="Condition when a thrown exception should result in a break."
    )


class ExceptionPathSegment(BaseModel):
    negate: Optional[bool] = Field(
        None,
        description="If false or missing this segment matches the names provided, "
        "otherwise it matches anything except the names provided.",
    )
    names: Optional[List[str]] = Field(
        None,
        description="Depending on the value of `negate` the names that should either be selected or ignored.",
    )


class FunctionBreakpoint(BaseModel):
    name: Optional[str] = Field(None, description="The name of the function.")
    condition: Optional[str] = Field(
        None, description="An expression for conditional breakpoints."
    )
    hitCondition: Optional[str] = Field(
        None,
        description="An expression that controls how many hits of the breakpoint are ignored.",
    )


class GotoTarget(BaseModel):
    id: str = Field(..., description="Unique identifier for a goto target.")
    label: str = Field(
        ..., description="The label shown to the user for the goto target."
    )
    line: int = Field(..., description="The line of the goto target.")
    column: Optional[int] = Field(None, description="The column of the goto target.")
    endLine: Optional[int] = Field(
        None, description="The end line of the range covered by the goto target."
    )
    endColumn: Optional[int] = Field(
        None, description="The end column of the range covered by the goto target."
    )
    instructionPointerReference: Optional[str] = Field(
        None,
        description="An optional memory reference for the instruction pointer value representing the goto target.",
    )


class InstructionBreakpoint(BaseModel):
    instructionReference: str = Field(
        ...,
        description="The instruction reference of the breakpoint. This should be a memory or instruction "
        "pointer reference from an `EvaluateResponse`, `Variable`, `StackFrame`, `GotoTarget`, or `Breakpoint`.",
    )
    offset: Optional[int] = Field(
        None,
        description="The offset from the instruction reference in bytes. This can be negative.",
    )
    condition: Optional[str] = Field(
        None,
        description="An expression for conditional breakpoints. It is only honored by a debug adapter "
        "if the corresponding capability `supportsConditionalBreakpoints` is true.",
    )
    hitCondition: Optional[str] = Field(
        None,
        description="An expression that controls how many hits of the breakpoint are ignored. "
        "The debug adapter is expected to interpret the expression as needed. "
        "The attribute is only honored by a debug adapter if the corresponding capability `supportsHitConditionalBreakpoints` is true.",
    )
    mode: Optional[str] = Field(
        None,
        description="The mode of this breakpoint. If defined, this must be one of the `breakpointModes` "
        "the debug adapter advertised in its `Capabilities`.",
    )


InvalidatedAreas = Literal["all", "stacks", "threads", "variables"] | str


class Message(BaseModel):
    id: int = Field(..., description="Unique identifier for the message.")
    format: str = Field(
        ...,
        description="A format string for the message. Embedded variables have the form `{name}`.",
    )
    variables: Optional[Dict[str, str]] = Field(
        None,
        description="An object used as a dictionary for looking up the variables in the format string.",
    )
    sendTelemetry: Optional[bool] = Field(
        None, description="If true, the message should be sent to telemetry."
    )
    showUser: Optional[bool] = Field(
        None, description="If true, the message should be shown to the user."
    )
    url: Optional[str] = Field(
        None,
        description="A URL where additional information about this message can be found.",
    )
    urlLabel: Optional[str] = Field(
        None,
        description="A label that is presented to the user as the UI for opening the URL.",
    )


class Module(BaseModel):
    id: int | str = Field(..., description="Unique identifier for the module.")
    name: str = Field(..., description="Name of the module.")
    path: Optional[str] = Field(None, description="Path to the module.")
    isOptimized: Optional[bool] = Field(None, description="Is optimized or not.")
    isUserCode: Optional[bool] = Field(None, description="Is user code or not.")
    version: Optional[str] = Field(None, description="Version of Module.")
    symbolStatus: Optional[str] = Field(None, description="Symbol status of Module.")
    symbolFilePath: Optional[str] = Field(
        None, description="Symbol file path of Module."
    )
    dateTimeStamp: Optional[str] = Field(
        None, description="Date and time stamp of Module."
    )
    addressRange: Optional[str] = Field(None, description="Address range of Module.")


class Scope(BaseModel):
    name: str = Field(
        ...,
        description="Name of the scope such as 'Arguments', 'Locals', or 'Registers'.",
    )
    presentationHint: Optional[
        Literal["arguments", "locals", "registers", "returnValue"] | str
    ] = Field(
        None, description="An optional hint for how to present this scope in the UI."
    )
    variablesReference: int = Field(
        ...,
        description="The variables reference of the variables presented in this scope. "
        "This can be a reference to a `Variable` or a `Container`.",
    )
    namedVariables: Optional[int] = Field(
        None,
        description="The number of named variables in this scope. The client can use "
        "this optional information to present the variables in a paged UI and fetch them in chunks.",
    )
    indexedVariables: Optional[int] = Field(
        None,
        description="The number of indexed variables in this scope. The client can use"
        "this optional information to present the variables in a paged UI and fetch them in chunks.",
    )
    expensive: Optional[bool] = Field(
        None,
        description="If true, the number of variables in this scope is large or expensive to retrieve.",
    )
    source: Optional[Source] = Field(
        None, description="Optional source for this scope."
    )
    line: Optional[int] = Field(
        None, description="Optional start line of the range covered by this scope."
    )
    column: Optional[int] = Field(
        None, description="Optional start column of the range covered by this scope."
    )
    endLine: Optional[int] = Field(
        None, description="Optional end line of the range covered by this scope."
    )
    endColumn: Optional[int] = Field(
        None, description="Optional end column of the range covered by this scope."
    )


class Source(BaseModel):
    name: Optional[str] = Field(None, description=" The short name of the source.")
    path: Optional[str] = Field(
        None, description="The path used to be shown in the UI."
    )
    sourceReference: Optional[int] = Field(
        None,
        description="If the value > 0 the contents of the source must be retrieved through the "
        "`source` request (even if a path is specified).",
    )
    presentationHint: Optional[Literal["normal", "emphasize", "deemphasize"]] = Field(
        None, description="A hint for how to present the source in the UI."
    )
    origin: Optional[str] = Field(None, description="The origin of this source.")
    sources: Optional[List[Source]] = Field(
        None, description="A list of sources that are related to this source."
    )
    adapterData: Optional[Any] = Field(
        None,
        description="Additional data that a debug adapter might want to loop through the client.",
    )
    checksums: Optional[Dict[str, Checksum]] = Field(
        None, description="The checksums associated with this file."
    )


class SourceBreakpoint(BaseModel):
    line: int = Field(..., description="The source line of the breakpoint.")
    column: Optional[int] = Field(
        None, description="An optional source column of the breakpoint."
    )
    condition: Optional[str] = Field(
        None, description="An optional expression for conditional breakpoints."
    )
    hitCondition: Optional[str] = Field(
        None,
        description="An optional expression that controls how many hits of the breakpoint are ignored.",
    )
    logMessage: Optional[str] = Field(
        None,
        description="The log message to be shown when the breakpoint is hit."
        " If not specified, the log message is not changed.",
    )
    mode: Optional[str] = Field(
        None,
        description="The mode of this breakpoint. If defined, this must be one of the `breakpointModes`"
        " the debug adapter advertised in its `Capabilities`.",
    )


class StackFrame(BaseModel):
    id: int = Field(..., description="An identifier for the stack frame.")
    name: str = Field(..., description="The name of the stack frame.")
    source: Optional[Source] = Field(
        None, description="The source where the stack frame is located."
    )
    line: int = Field(..., description="The line within the file of the stack frame.")
    column: int = Field(
        ..., description="The column within the line of the stack frame."
    )
    endLine: Optional[int] = Field(
        None, description="The end line of the range covered by the stack frame."
    )
    endColumn: Optional[int] = Field(
        None, description="The end column of the range covered by the stack frame."
    )
    canRestart: Optional[bool] = Field(
        None, description="If true, the stack frame can be restarted."
    )
    instructionPointerReference: Optional[str] = Field(
        None,
        description="An optional memory reference to where the instruction pointer is stored.",
    )
    moduleId: Optional[int | str] = Field(
        None, description="The module identifier of the stack frame."
    )
    presentationHint: Optional[Literal["normal", "label", "subtle"]] = Field(
        None, description="An optional hint for how to present this frame in the UI."
    )


class StackFrameTarget(BaseModel):
    parameters: Optional[bool] = Field(
        None, description="Displays parameters for the stack frame."
    )
    parameterTypes: Optional[bool] = Field(
        None, description="Displays parameter types for the stack frame."
    )
    parameterNames: Optional[bool] = Field(
        None, description="Displays parameter names for the stack frame."
    )
    parameterValues: Optional[bool] = Field(
        None, description="Displays parameter values for the stack frame."
    )
    line: Optional[bool] = Field(
        None, description="Displays the line for the stack frame."
    )
    module: Optional[bool] = Field(
        None, description="Displays the module for the stack frame."
    )
    includeAll: Optional[bool] = Field(
        None,
        description="Includes all stack frames, including those the debug adapter might otherwise hide.",
    )


class StepInTarget(BaseModel):
    id: str = Field(..., description="Unique identifier for a stepIn target.")
    label: str = Field(
        ..., description="The name of the stepIn target (shown in the UI)."
    )
    line: int = Field(..., description="The line of the stepIn target.")
    column: Optional[int] = Field(None, description="The column of the stepIn target.")
    endLine: Optional[int] = Field(
        None, description="The end line of the range covered by the stepIn target."
    )
    endColumn: Optional[int] = Field(
        None, description="The end column of the range covered by the stepIn target."
    )


SteppingGranularity = Literal["statement", "line", "instruction"]


class Thread(BaseModel):
    id: int = Field(..., description="Unique identifier for the thread.")
    name: str = Field(..., description="A name for the thread.")


class ValueFormat(BaseModel):
    hex: Optional[bool] = Field(None, description="Display the value in hex.")


class Variable(BaseModel):
    name: str = Field(..., description="The variable's name.")
    value: str = Field(..., description="The variable's value.")
    type: Optional[str] = Field(None, description="The variable's type.")
    presentationHint: Optional[VariablePresentationHint] = Field(
        None, description="An optional hint for how to present this variable in the UI."
    )
    evaluateName: Optional[str] = Field(
        None,
        description="An optional expression that can be evaluated in the current scope to obtain the variable's value.",
    )
    variablesReference: int = Field(
        ...,
        description="The variable's reference. This can be a reference to a `Variable` or a `Container`.",
    )
    namedVariables: Optional[int] = Field(
        None,
        description="The number of named child variables. The client can use this optional information to "
        "present the children in a paged UI and fetch them in chunks.",
    )
    indexedVariables: Optional[int] = Field(
        None,
        description="The number of indexed child variables. The client can use this optional information to "
        "present the children in a paged UI and fetch them in chunks.",
    )
    memoryReference: Optional[str] = Field(
        None,
        description="If the value is structured and can be retrieved in memory, the memory reference to the value.",
    )


class VariablePresentationHint(BaseModel):
    kind: (
        Literal[
            "property",
            "method",
            "class",
            "data",
            "event",
            "baseClass",
            "innerClass",
            "interface",
            "mostDerivedClass",
            "virtual",
            "dataBreakpoint",
        ]
        | str
    ) = Field(
        ...,
        description="The kind of variable. Before introducing additional values, try to use the listed values.",
    )
    attributes: Optional[
        List[
            Literal[
                "static",
                "constant",
                "readOnly",
                "rawString",
                "hasObjectId",
                "canHaveObjectId",
                "hasSideEffects",
                "hasDataBreakpoint",
            ]
            | str
        ]
    ] = Field(None, description="Set of attributes represented as an array of strings.")
    visibility: Optional[
        Literal["public", "protected", "private", "internal", "final", "dynamic"] | str
    ] = Field(
        None,
        description="Visibility of variable. Before introducing additional values, try to use the listed values.",
    )
    lazy: Optional[bool] = Field(
        None,
        description="If true, clients can present the variable with a UI that supports a specific gesture to trigger its evaluation."
        "This mechanism can be used for properties that require executing code when retrieving their value and where the code execution "
        "can be expensive and/or produce side-effects. A typical example are properties based on a getter function.",
    )
