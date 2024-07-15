from typing import Dict, Optional

from .buffer import *
from .data import *
from .requests import *
from .types import *


class Client:
    def __init__(self):
        self._seq: int = 0
        self._send_buf = bytearray()

    def _send_request(
        self, method: str, params: Optional[dict[str, Any]] = None
    ) -> int:
        id = self._seq
        self._seq += 1

        self._send_buf += RequestBuffer(method=method, params=params, id=id)
        return id

    def _handle_response(self, response: Response) -> Optional[Response]: ...

    def send(self, command: str, arguments: Optional[Dict[str, any]] = None) -> bytes:
        send_buf = self._send_buf
        self._send_buf = bytearray()
        return send_buf

    # Requests
    def cancel(
        self, request_id: Optional[int] = None, progress_id: Optional[str] = None
    ) -> int:
        """The cancel request is used by the client in two situations:

        - to indicate that it is no longer interested in the result produced by a specific request issued earlier
        - to cancel a progress sequence.

        Both progress_id and request_id can be specified in the same request.

        Args:
            request_id: The ID (_seq) of the request to cancel. If missing no request is canceled.
            progress_id: The progress ID of the progress sequence to cancel. If missing no progress is canceled.
        """

        return self._send_request(
            "cancel", {"requestId": request_id, "progressId": progress_id}
        )

    def attach(self, __restart: Optional[Any] = None) -> int:
        """attach to a running process.

        Args:
            __restart: Arbitrary data from the previous, restarted session. \
                The data is sent as the `restart` attribute of the `terminated` event."""

        return self._send_request("attach", {"__restart": __restart})

    def breakpoint_locations(
        self,
        source: Source,
        line: int,
        column: Optional[int] = None,
        end_line: Optional[int] = None,
        end_column: Optional[int] = None,
    ) -> int:
        """Retrieve all possible locations for source breakpoints in a given range.

        Args:
            source: The source location of the breakpoints.
            line: The source line of the breakpoints.
            column: An optional source column of the breakpoints.
            end_line: An optional end line of the range covered by the breakpoint.
            end_column: An optional end column of the range covered by the breakpoint.
        """

        return self._send_request(
            "breakpointLocations",
            {
                "source": source,
                "line": line,
                "column": column,
                "endLine": end_line,
                "endColumn": end_column,
            },
        )

    def completions(
        self,
        text: str,
        column: int,
        line: Optional[int],
        frame_id: Optional[int] = None,
    ) -> int:
        """Returns a list of possible completions for a given caret position and text.

        Args:
            text: One or more source lines. Typically this is the text users have typed into \
                the debug console before they asked for completion.
            column: The position within `text` for which to determine the completion proposals.
            line: A line for which to determine the completion proposals. If missing the \
                first line of the text is assumed.
            frame_id: An optional frameId of the stack frame, if specified returns \
                completions in the scope of this stack frame.
        """

        return self._send_request(
            "completions",
            {
                "frameId": frame_id,
                "text": text,
                "column": column,
                "line": line,
            },
        )

    def configuration_done(self) -> int:
        """This request indicates that the client has finished initialization of the debug adapter."""

        return self._send_request("configurationDone")

    def continue_(self, thread_id: int, single_thread: Optional[bool] = None) -> int:
        """The request resumes execution of all threads.
        If the debug adapter supports single thread execution, setting `single_thread` true resumes only the specified thread.

        Args:
            thread_id: the active thread.
            single_thread: Execute only this thread.
        """

        return self._send_request(
            "continue", {"threadId": thread_id, "singleThread": single_thread}
        )

    def data_breakpoint_info(
        self,
        name: str,
        variables_reference: Optional[int] = None,
        frameId: Optional[int] = None,
        bytes: Optional[int] = None,
        asAddress: Optional[bool] = None,
        mode: Optional[str] = None,
    ) -> int:
        """Retrieve the information of a data breakpoint.

        Args:
            variables_reference: Reference to the variable container if the data breakpoint is requested for \
                a child of the container.
            name: The name of the variable's child to obtain data breakpoint information for.
            frameId: When `name` is an expression, evaluate it in the scope of this stack frame.
            bytes: If specified, a debug adapter should return information for the range of memory extending \
                `bytes` number of bytes from the address or variable specified by `name`. \
                Breakpoints set using the resulting data ID should pause on data access anywhere within that range.
            asAddress: If true, `name` is an address.
            mode: The mode of the desired breakpoint.
        """

        return self._send_request(
            "dataBreakpointInfo",
            {
                "variablesReference": variables_reference,
                "name": name,
                "frameId": frameId,
                "bytes": bytes,
                "asAddress": asAddress,
                "mode": mode,
            },
        )

    def disassemble(
        self,
        memory_reference: str,
        instruction_count: Optional[int] = None,
        offset: Optional[int] = None,
        instruction_offset: Optional[int] = None,
        resolve_symbols: Optional[bool] = None,
    ) -> int:
        """Disassembles code stored at the provided location.

        Args:
            memory_reference: Memory reference to the base location containing the instructions to disassemble.
            instruction_count: The number of instructions to disassemble starting at the specified location and offset.
            offset: The offset (in bytes) of the first instruction to disassemble.
            instruction_offset: The offset (in instructions) of the first instruction to disassemble.
            resolve_symbols: If set to true, the adapter should attempt to resolve memory addresses \
                to function names and line numbers.
        """

        return self._send_request(
            "disassemble",
            {
                "memoryReference": memory_reference,
                "offset": offset,
                "instructionCount": instruction_count,
            },
        )

    def disconnect(
        self,
        restart: Optional[bool] = None,
        terminal_debuggee: Optional[bool] = None,
        suspend_debuggee: Optional[bool] = None,
    ) -> int:
        """Asks the debug adapter to disconnect from the debuggee (thus ending the debug session) and then to shut down.

        In addition, the debug adapter must terminate the debuggee if it was started with the launch request.
        If an attach request was used to connect to the debuggee, then the debug adapter must not terminate the debuggee.

        Args:
            restart: A value of true indicates that this 'disconnect' request is part of a restart sequence.
            terminal_debuggee: Indicates whether the debuggee should be terminated when the debugger is disconnected.
            suspend_debuggee: Indicates whether the debuggee should be allowed to run after the debugger is disconnected.
        """

        return self._send_request(
            "disconnect",
            {
                "restart": restart,
                "terminateDebuggee": terminal_debuggee,
                "suspendDebuggee": suspend_debuggee,
            },
        )

    def evaluate(
        self,
        expression: str,
        frame_id: Optional[int] = None,
        line: Optional[int] = None,
        column: Optional[int] = None,
        source: Optional[Source] = None,
        context: Optional[
            Literal["watch", "repl", "hover", "clipboard", "variables"] | str
        ] = None,
        format: Optional[ValueFormat] = None,
    ) -> int:
        """Evaluate the given expression in the context of topmost stack frame.
        The expression has access to any variables and arguments that are in scope.

        Args:
            expression: The expression to evaluate.
            frame_id: Evaluate the expression in the scope of this stack frame. \
                If not specified, the expression is evaluated in the global scope.
            line: The contextual line where the expression should be evaluated. \
                In the 'hover' context, this should be set to the start of the expression being hovered.
            column: The contextual column where the expression should be evaluated. \
                This may be provided if `line` is also provided.
            source: The contextual source in which the `line` is found. \
                This must be provided if `line` is provided.
            context: The context in which the evaluate request is used.
            format: Specifies details on how to format the result.
        """

        return self._send_request(
            "evaluate",
            {
                "expression": expression,
                "frameId": frame_id,
                "line": line,
                "column": column,
                "source": source,
                "context": context,
                "format": format,
            },
        )

    def exception_info(self, thread_id: int) -> int:
        """Retrieves the details of the exception that caused this event to be raised.

        Args:
            thread_id: Thread for which exception information should be retrieved.
        """

        return self._send_request("exceptionInfo", {"threadId": thread_id})

    def goto(self, thread_id: int, target_id: str) -> int:
        """The request sets the location where the debuggee will continue to run.

        Args:
            thread_id: The thread to continue.
            target_id: The location where the debuggee will continue to run.
        """

        return self._send_request(
            "goto", {"threadId": thread_id, "targetId": target_id}
        )

    def goto_targets(
        self, source: Source, line: int, column: Optional[int] = None
    ) -> int:
        """Retrieve possible goto targets for the specified location.

        Args:
            source: The source location for which the goto targets are determined.
            line: The line for which the goto targets are determined.
            column: An optional column for which the goto targets are determined.
        """

        return self._send_request(
            "gotoTargets", {"source": source, "line": line, "column": column}
        )

    def initialize(
        self,
        adapter_id: str,
        client_id: Optional[str] = None,
        client_name: Optional[str] = None,
        locale: Optional[str] = None,
        lines_start_at1: Optional[bool] = None,
        columns_start_at1: Optional[bool] = None,
        path_format: Optional[Literal["path", "uri"] | str] = None,
        supports_variable_type: Optional[bool] = None,
        supports_variable_paging: Optional[bool] = None,
        supports_run_in_terminal_request: Optional[bool] = None,
        supports_memory_references: Optional[bool] = None,
        supports_progress_reporting: Optional[bool] = None,
        supports_invalidated_event: Optional[bool] = None,
        supports_memory_event: Optional[bool] = None,
        supports_args_can_be_interpreted_by_shell: Optional[bool] = None,
        supports_start_debugging_request: Optional[bool] = None,
    ) -> int:
        """Initializes the debug adapter with the client capabilities."""

        return self._send_request(
            "initialize",
            {
                "adapterID": adapter_id,
                "clientID": client_id,
                "clientName": client_name,
                "locale": locale,
                "linesStartAt1": lines_start_at1,
                "columnsStartAt1": columns_start_at1,
                "pathFormat": path_format,
                "supportsVariableType": supports_variable_type,
                "supportsVariablePaging": supports_variable_paging,
                "supportsRunInTerminalRequest": supports_run_in_terminal_request,
                "supportsMemoryReferences": supports_memory_references,
                "supportsProgressReporting": supports_progress_reporting,
                "supportsInvalidatedEvent": supports_invalidated_event,
                "supportsMemoryEvent": supports_memory_event,
                "supportsArgsCanBeNull": supports_args_can_be_interpreted_by_shell,
                "supportsStartDebuggingRequest": supports_start_debugging_request,
            },
        )

    def launch(
        self,
        no_debug: Optional[bool] = None,
        __restart: Optional[Any] = None,
    ) -> int:
        """The launch request is used to start the debuggee with or without debugging enabled.
        
        Args:
            no_debug: Set to true if the launch request is used to just start the debuggee \
                for the purpose of collecting output. The debuggee is not supposed to stop at breakpoints.
            __restart: Arbitrary data from the previous, restarted session. \
                The data is sent as the `restart` attribute of the `terminated` event.
        """

        return self._send_request(
            "launch",
            {"noDebug": no_debug, "__restart": __restart},
        )

    def loaded_sources(self) -> int:
        """Retrieves the set of all sources currently loaded by the debugged process.

        Args:
            reason: The reason for the event.
        """

        return self._send_request("loadedSources")

    def modules(
        self, start_module: Optional[int] = None, module_count: Optional[int] = None
    ) -> int:
        """Modules can be retrieved from the debug adapter with this request which can either
        return all modules or a range of modules to support paging.

        Args:
            start_module: The 0-based index of the first module to return; if omitted modules start at 0.
            module_count: The number of modules to return. If moduleCount is not specified or 0, \
                all modules are returned.
        """

        return self._send_request(
            "modules", {"startModule": start_module, "moduleCount": module_count}
        )

    def next(
        self,
        thread_id: int,
        single_thread: Optional[bool] = None,
        granularity: Optional[str] = None,
    ) -> int:
        """The request steps through the program.

        Args:
            thread_id: Specifies the thread for which to resume execution for one step.
            single_thread: If this is true, all other suspended threads are not resumed.
            granularity: The granularity of the step, assumed to be 'statement' if not specified.
        """

        return self._send_request(
            "next",
            {
                "threadId": thread_id,
                "singleThread": single_thread,
                "granularity": granularity,
            },
        )

    def pause(self, thread_id: int) -> int:
        """Suspends the debuggee.

        Args:
            thread_id: The thread to pause.
        """

        return self._send_request("pause", {"threadId": thread_id})

    def read_memory(
        self, memory_reference: str, count: int, offset: Optional[int] = None
    ) -> int:
        """Reads memory from the debuggee.

        Args:
            memory_reference: The memory reference to the base location from which to read memory.
            count: The number of bytes to read at the specified location and offset.
            offset: The offset (in bytes) of the first byte to read.
        """

        return self._send_request(
            "readMemory",
            {"memoryReference": memory_reference, "offset": offset, "count": count},
        )

    def restart(
        self,
        arguments: Optional[LaunchRequestArguments | AttachRequestArguments] = None,
    ) -> int:
        """Restarts a debug session.

        Args:
            arguments: Use either arguments for the 'launch' or 'attach' request.
        """

        return self._send_request("restart", arguments)

    def restart_frame(self, frame_id: int) -> int:
        """Restart the stack frame identified by the given frame ID.
        The frame ID must have been obtained in the current suspended state.

        Args:
            frame_id: The frame to restart.
        """

        return self._send_request("restartFrame", {"frameId": frame_id})

    def reverse_continue(
        self, thread_id: int, single_thread: Optional[bool] = None
    ) -> int:
        """The request starts the debuggee to run backward.

        Args:
            thread_id: ID of the active thread.
            single_thread: If true, backward execution is limited to the specified thread.
        """

        return self._send_request(
            "reverseContinue",
            {"threadId": thread_id, "singleThread": single_thread},
        )

    def scopes(self, frame_id: int) -> int:
        """The request returns the variable scopes for a given stack frame.

        Args:
            frame_id: Retrieve the scopes for this stackframe.
        """

        return self._send_request("scopes", {"frameId": frame_id})

    def set_breakpoints(
        self,
        source: Source,
        breakpoints: List[SourceBreakpoint],
        lines: Optional[List[int]] = None,
        source_modified: Optional[bool] = None,
    ) -> int:
        """Sets multiple breakpoints for a single source and clears all previous breakpoints in that source.

        Args:
            source: The source location of the breakpoints.
            breakpoints: The code locations of the breakpoints.
            lines: The source lines of the breakpoints.
            source_modified: A value of true indicates that the underlying source has been modified \
                which results in new breakpoint locations.
        """

        return self._send_request(
            "setBreakpoints",
            {
                "source": source,
                "breakpoints": breakpoints,
                "lines": lines,
                "sourceModified": source_modified,
            },
        )

    def set_data_breakpoints(self, breakpoints: List[DataBreakpoint]) -> int:
        """Replaces all existing data breakpoints with new data breakpoints.

        Args:
            breakpoints: The data breakpoints to set.
        """

        return self._send_request("setDataBreakpoints", {"breakpoints": breakpoints})

    def set_exception_breakpoints(
        self,
        filters: List[str],
        filter_options: Optional[List[ExceptionFilterOptions]],
        exception_options: Optional[List[ExceptionOptions]],
    ) -> int:
        """The request configures the debugger's response to thrown exceptions.

        Each of the filters, filterOptions, and exceptionOptions in the request are independent configurations
        to a debug adapter indicating a kind of exception to catch. An exception thrown in a program should result
        in a stopped event from the debug adapter (with reason exception) if any of the configured filters match.

        Args:
            filters: Set of exception filters specified by their ID.
            filter_options: An array of ExceptionFilterOptions. The set of all possible exception filters \
                is defined by the `exceptionBreakpointFilters` capability.
            exception_options: An array of ExceptionOptions. Configuration options for selected exceptions.
        """

        return self._send_request(
            "setExceptionBreakpoints",
            {
                "filters": filters,
                "filterOptions": filter_options,
                "exceptionOptions": exception_options,
            },
        )

    def set_expression(
        self,
        expression: str,
        value: str,
        frame_id: Optional[int] = None,
        format: Optional[ValueFormat] = None,
    ) -> int:
        """Evaluates the given value expression and assigns it to the expression which must be a modifiable l-value.

        The expressions have access to any variables and arguments that are in scope of the specified frame.

        Args:
            expression: The l-value expression to assign the result to.
            value: The value expression to assign to the l-value expression.
            frame_id: Evaluate the expressions in the scope of this stack frame. \
                If not specified, the expressions are evaluated in the global scope.
            format: Specifies details on how to format the result.
        """

        return self._send_request(
            "setExpression",
            {
                "expression": expression,
                "value": value,
                "frameId": frame_id,
                "format": format,
            },
        )

    def set_function_breakpoints(
        self, breakpoints: List[FunctionBreakpoint] = []
    ) -> int:
        """Replaces all existing function breakpoints with new function breakpoints.

        To clear all function breakpoints, call this without arguments.
        When a function breakpoint is hit, a stopped event (with reason function breakpoint) is generated.

        Args:
            breakpoints: The function breakpoints to set.
        """

        return self._send_request(
            "setFunctionBreakpoints", {"breakpoints": breakpoints}
        )

    def set_instruction_breakpoints(
        self, breakpoints: List[InstructionBreakpoint]
    ) -> int:
        """Replaces all existing instruction breakpoints. Typically, instruction breakpoints would be set from a disassembly window.

        To clear all instruction breakpoints, specify an empty array.
        When an instruction breakpoint is hit, a stopped event (with reason instruction breakpoint) is generated.

        Args:
            breakpoints: The instruction breakpoints to set.
        """

        return self._send_request(
            "setInstructionBreakpoints", {"breakpoints": breakpoints}
        )

    def set_variable(
        self,
        variables_reference: int,
        name: str,
        value: str,
        format: Optional[ValueFormat] = None,
    ) -> int:
        """Set the variable with the given name in the variable container to a new value.

        Args:
            variables_reference: The reference of the variable container.
            name: The name of the variable to set.
            value: The value to set.
            format: Specifies details on how to format the response value.
        """

        return self._send_request(
            "setVariable",
            {
                "variablesReference": variables_reference,
                "name": name,
                "value": value,
                "format": format,
            },
        )

    def source(self, source_reference: int, source: Optional[Source] = None) -> int:
        """The request retrieves the source code for a given source reference.

        Args:
            source_reference: The reference to the source. This is the same as `source.sourceReference`.
            source: Specifies the source content to load. Either `source.path` or `source.sourceReference` must be specified.
        """

        return self._send_request(
            "source", {"sourceReference": source_reference, "source": source}
        )

    def stack_trace(
        self,
        thread_id: Optional[int] = None,
        start_frame: Optional[int] = None,
        levels: Optional[int] = None,
        format: Optional[StackFrameFormat] = None,
    ) -> int:
        """The request returns a stack trace from the current execution state.

        Request all stack frames by omitting the startFrame and levels arguments.

        Args:
            thread_id: Retrieve the stacktrace for this thread.
            start_frame: The index of the first frame to return; if omitted frames start at 0.
            levels: The maximum number of frames to return. If levels is not specified or 0, all frames are returned.
            format: Specifies details on how to format the stack frames.
        """

        return self._send_request(
            "stackTrace",
            {
                "threadId": thread_id,
                "startFrame": start_frame,
                "levels": levels,
                "format": format,
            },
        )

    def step_back(
        self,
        thread_id: int,
        single_thread: Optional[bool] = None,
        granularity: Optional[SteppingGranularity] = None,
    ) -> int:
        """The request executes one backward step (in the given granularity) for the specified thread
        and allows all other threads to run backward freely by resuming them.

        If the debug adapter supports single thread execution (see capability `supportsSingleThreadExecutionRequests`),
        setting the singleThread argument to true prevents other suspended threads from resuming.
        The debug adapter first sends the response and then a stopped event (with reason step) after the step has completed.

        Args:
            thread_id: ID of the active thread.
            single_thread: If true, backward execution is limited to the specified thread.
            granularity: The granularity of the step, assumed to be 'statement' if not specified.
        """

        return self._send_request(
            "stepBack",
            {
                "threadId": thread_id,
                "singleThread": single_thread,
                "granularity": granularity,
            },
        )

    def step_in(
        self,
        thread_id: int,
        single_thread: Optional[bool] = None,
        target_id: Optional[int] = None,
        granularity: Optional[SteppingGranularity] = None,
    ) -> int:
        """The request resumes the given thread to step into a function/method and allows all other threads to run freely by resuming them.

        If the debug adapter supports single thread execution (see capability `supportsSingleThreadExecutionRequests`),
        setting the singleThread argument to true prevents other suspended threads from resuming.

        If the request cannot step into a target, stepIn behaves like the next request.
        The debug adapter first sends the response and then a stopped event (with reason step) after the step has completed.

        If there are multiple function/method calls (or other targets) on the source line,
        the argument targetId can be used to control into which target the stepIn should occur.

        Args:
            thread_id: ID of the active thread.
            single_thread: If true, stepIn is limited to the specified thread.
            target_id: The stepIn target for this step.
            granularity: The granularity of the step, assumed to be 'statement' if not specified.
        """

        return self._send_request(
            "stepIn",
            {
                "threadId": thread_id,
                "singleThread": single_thread,
                "targetId": target_id,
                "granularity": granularity,
            },
        )

    def step_in_targets(self, frame_id: int) -> int:
        """The request retrieves the possible stepIn targets for the specified stack frame.
        These targets can be used in the stepIn request.

        Args:
            frame_id: The stack frame for which to retrieve the possible stepIn targets.
        """

        return self._send_request("stepInTargets", {"frameId": frame_id})

    def step_out(
        self,
        thread_id: int,
        single_thread: Optional[bool] = None,
        granularity: Optional[SteppingGranularity] = None,
    ) -> int:
        """The request resumes the given thread to step out of the current function/method and allows all other threads to run freely by resuming them.

        If the debug adapter supports single thread execution (see capability `supportsSingleThreadExecutionRequests`),
        setting the singleThread argument to true prevents other suspended threads from resuming.

        The debug adapter first sends the response and then a stopped event (with reason step) after the step has completed.

        Args:
            thread_id: ID of the active thread.
            single_thread: If true, stepOut is limited to the specified thread.
            granularity: The granularity of the step, assumed to be 'statement' if not specified.
        """

        return self._send_request(
            "stepOut",
            {
                "threadId": thread_id,
                "singleThread": single_thread,
                "granularity": granularity,
            },
        )

    def terminate(self, restart: Optional[bool] = None) -> int:
        """The terminate request is sent from the client to the debug adapter in order to shut down the debuggee gracefully.

        Typically a debug adapter implements terminate by sending a software signal which the debuggee intercepts in order
        to clean things up properly before terminating itself.

        Please note that this request does not directly affect the state of the debug session: if the debuggee decides to
        veto the graceful shutdown for any reason by not terminating itself, then the debug session just continues.

        Args:
            restart: A value of true indicates that this 'terminate' request is part of a restart sequence.
        """

        return self._send_request("terminate", {"restart": restart})

    def terminate_threads(self, thread_ids: List[int]) -> int:
        """The request terminates the threads with the given ids.

        Args:
            thread_ids: The threads to terminate.
        """

        return self._send_request("terminateThreads", {"threadIds": thread_ids})

    def threads(self) -> int:
        """The request retrieves a list of all threads.

        Args:
            reason: The reason for the event.
        """

        return self._send_request("threads")

    def variables(
        self,
        variables_reference: int,
        filter: Optional[Literal["indexed", "named"]] | str = None,
        start: Optional[int] = None,
        count: Optional[int] = None,
        format: Optional[ValueFormat] = None,
    ) -> int:
        """Retrieves all child variables for the given variable reference.

        A filter can be used to limit the fetched children to either named or indexed children.

        Args:
            variables_reference: The variable for which to retrieve its children.
            filter: Filter to limit the child variables to either named or indexed. If not specified, both types are fetched.
            start: The index of the first variable to return; if omitted variables start at 0.
            count: The number of variables to return. If not passed or 0, all variables are returned.
            format: Specifies details on how to format the response value.
        """

        return self._send_request(
            "variables",
            {
                "variablesReference": variables_reference,
                "filter": filter,
                "start": start,
                "count": count,
                "format": format,
            },
        )

    def write_memory(
        self,
        memory_reference: str,
        data: str,
        offset: Optional[int] = None,
        allow_partial: Optional[bool] = None,
    ) -> int:
        """Writes bytes to memory at the provided location.

        Args:
            memory_reference: The memory reference to the base location to write memory.
            data: Bytes to write, encoded using base64.
            offset: The offset (in bytes) of the first byte to write. Can be negative.
            allow_partial: Property to control partial writes. If true, the debug adapter should \
                attempt to write memory even if the entire memory region is not writable.
        """

        return self._send_request(
            "writeMemory",
            {
                "memoryReference": memory_reference,
                "offset": offset,
                "data": data,
                "allowPartial": allow_partial,
            },
        )
