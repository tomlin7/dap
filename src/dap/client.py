from typing import Dict, Optional

from .buffer import *
from .data import *
from .types import *


class DAPClient:
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
