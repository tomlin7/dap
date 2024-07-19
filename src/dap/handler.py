from __future__ import annotations

import json
import typing

from .base import DAPMessage, ErrorResponse, Event, Events, Requests, Response
from .events import *
from .responses import *

if typing.TYPE_CHECKING:
    from .client import Client


HEADER_ENCODING = "ascii"
CONTENT_ENCODING = "utf-8"


class Handler:
    """Handler for DAP events, responses and reverse requests."""

    def __init__(self, client: Client) -> None:
        self.client = client

    def _parse_message(self, data: dict[str, any]) -> Response | Event:
        try:
            return Response.model_validate(data)
        except ValueError:
            return Event.model_validate(data)

    def handle(self) -> typing.Generator[EventBody | ResponseBody, None, None]:
        """Handle incoming messages from the client."""

        while b"\r\n\r\n" in self.client._receive_buf:
            headers, rest = self.client._receive_buf.split(b"\r\n\r\n", 1)

            # temporary setup, will break if multiple headers are added
            content_length = int(
                headers.decode(encoding=HEADER_ENCODING).split(":")[1].strip()
            )

            if len(rest) >= content_length:
                self.client._receive_buf = rest[content_length:]
                content = json.loads(
                    rest[:content_length].decode(encoding=CONTENT_ENCODING)
                )
                content = self._parse_message(content)
                message_type = content.type
                if message_type == DAPMessage.EVENT:
                    yield self.handle_event(content)
                elif message_type == DAPMessage.RESPONSE:
                    yield self.handle_response(content)
                elif message_type == DAPMessage.REQUEST:
                    # TODO: Implement reverse request handling
                    raise ValueError("Request messages are not supported yet")
                else:
                    raise ValueError(f"Unsupported message: {message_type}")

            else:
                # more data is needed to complete the event
                break

    def handle_event(self, event: Event) -> EventBody:
        match event.event:
            case Events.INITIALIZED:
                return InitializedEvent.model_validate(event.body)
            case Events.BREAKPOINT:
                return BreakpointEvent.model_validate(event.body)
            case Events.CAPABILITIES:
                return CapabilitiesEvent.model_validate(event.body)
            case Events.CONTINUED:
                return ContinuedEvent.model_validate(event.body)
            case Events.EXITED:
                return ExitedEvent.model_validate(event.body)
            case Events.INVALIDATED:
                return InvalidatedEvent.model_validate(event.body)
            case Events.LOADED_SOURCE:
                return LoadedSourceEvent.model_validate(event.body)
            case Events.MEMORY:
                return MemoryEvent.model_validate(event.body)
            case Events.MODULE:
                return ModuleEvent.model_validate(event.body)
            case Events.OUTPUT:
                return OutputEvent.model_validate(event.body)
            case Events.PROCESS:
                return ProcessEvent.model_validate(event.body)
            case Events.PROGRESS_END:
                return ProgressEndEvent.model_validate(event.body)
            case Events.PROGRESS_START:
                return ProgressStartEvent.model_validate(event.body)
            case Events.PROGRESS_UPDATE:
                return ProgressUpdateEvent.model_validate(event.body)
            case Events.STOPPED:
                return StoppedEvent.model_validate(event.body)
            case Events.TERMINATED:
                return TerminatedEvent.model_validate(event.body)
            case Events.THREAD:
                return ThreadEvent.model_validate(event.body)
            case _:
                # event specific to the debug adapter
                # print(f"⚠️ Unsupported event: {event.event}")
                return event

    def handle_response(self, response: Response) -> ResponseBody:
        assert response.request_seq is not None

        request = self.client._pending_requests.pop(response.request_seq)
        assert request is not None
        assert request.command == response.command

        if not response.success:
            # print(f"⚠️ FAIL Request failed {request}: {response.message}")
            return ErrorResponse.model_validate(response.model_dump())

        match response.command:
            case Requests.INITIALIZE:
                return Initialized.model_validate(response.body)
            case Requests.CANCEL:
                return Cancelled.model_validate(response.body)
            case Requests.ATTACH:
                return Attached.model_validate(response.body)
            case Requests.BREAKPOINTLOCATIONS:
                return BreakpointLocationsResponse.model_validate(response.body)
            case Requests.COMPLETIONS:
                return CompletionsResponse.model_validate(response.body)
            case Requests.CONFIGURATIONDONE:
                return ConfigurationDone.model_validate(response.body)
            case Requests.CONTINUE:
                return Continued.model_validate(response.body)
            case Requests.DATABREAKPOINTINFO:
                return DataBreakpointInfoResponse.model_validate(response.body)
            case Requests.DISASSEMBLE:
                return DisassembleResponse.model_validate(response.body)
            case Requests.DISCONNECT:
                return Disconnected.model_validate(response.body)
            case Requests.EVALUATE:
                return EvaluateResponse.model_validate(response.body)
            case Requests.EXCEPTIONINFO:
                return ExceptionInfoResponse.model_validate(response.body)
            case Requests.GOTO:
                return GotoDone.model_validate(response.body)
            case Requests.GOTOTARGETS:
                return GotoTargetsResponse.model_validate(response.body)
            case Requests.LAUNCH:
                return LaunchDone.model_validate(response.body)
            case Requests.LOADEDSOURCES:
                return LoadedSourcesResponse.model_validate(response.body)
            case Requests.MODULES:
                return ModulesResponse.model_validate(response.body)
            case Requests.NEXT:
                return NextResponse.model_validate(response.body)
            case Requests.PAUSE:
                return Paused.model_validate(response.body)
            case Requests.READMEMORY:
                return ReadMemoryResponse.model_validate(response.body)
            case Requests.RESTART:
                return Restarted.model_validate(response.body)
            case Requests.RESTARTFRAME:
                return RestartFrameDone.model_validate(response.body)
            case Requests.REVERSECONTINUE:
                return ReverseContinueDone.model_validate(response.body)
            case Requests.SCOPES:
                return ScopesResponse.model_validate(response.body)
            case Requests.SETBREAKPOINTS:
                return SetBreakpointsResponse.model_validate(response.body)
            case Requests.SETDATABREAKPOINTS:
                return SetDataBreakpointsResponse.model_validate(response.body)
            case Requests.SETEXCEPTIONBREAKPOINTS:
                return SetExceptionBreakpointsResponse.model_validate(response.body)
            case Requests.SETEXPRESSION:
                return SetExpressionResponse.model_validate(response.body)
            case Requests.SETFUNCTIONBREAKPOINTS:
                return SetFunctionBreakpointsResponse.model_validate(response.body)
            case Requests.SETINSTRUCTIONBREAKPOINTS:
                return SetInstructionBreakpointsResponse.model_validate(response.body)
            case Requests.SETVARIABLE:
                return SetVariableResponse.model_validate(response.body)
            case Requests.SOURCE:
                return SourceResponse.model_validate(response.body)
            case Requests.STACKTRACE:
                return StackTraceResponse.model_validate(response.body)
            case Requests.STEPBACK:
                return StepBackDone.model_validate(response.body)
            case Requests.STEPIN:
                return StepInDone.model_validate(response.body)
            case Requests.STEPINTARGETS:
                return StepInTargetsResponse.model_validate(response.body)
            case Requests.STEPOUT:
                return StepOutDone.model_validate(response.body)
            case Requests.TERMINATE:
                return Terminated.model_validate(response.body)
            case Requests.TERMINATETHREADS:
                return TerminateThreadsDone.model_validate(response.body)
            case Requests.THREADS:
                return ThreadsResponse.model_validate(response.body)
            case Requests.VARIABLES:
                return VariablesResponse.model_validate(response.body)
            case Requests.WRITEMEMORY:
                return WriteMemoryResponse.model_validate(response.body)
            case _:
                # possibly some request specific to the debug adapter?
                # print(f"⚠️ Unsupported request: {response.command}")
                return response
