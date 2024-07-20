from typing import Literal, Optional, TypedDict

from pydantic import Field

from .base import Request, RequestArguments, Response
from .responses import (
    RunInTerminalResponse,
    RunInTerminalResponseBody,
    StartDebuggingResponse,
)


class AttachRequestArguments(TypedDict):
    """Arguments for 'attach' request."""

    __restart: Optional[bool] = None


class LaunchRequestArguments(TypedDict):
    """Arguments for 'launch' request."""

    noDebug: Optional[bool] = None
    __restart: Optional[bool] = None


# Reverse requests


class RunInTerminalRequestArguments(RequestArguments):
    """Arguments for 'runInTerminal' reverse request."""

    kind: Optional[str] = Field(
        None,
        description="The kind of terminal to run the command in.",
    )
    title: Optional[str] = Field(
        None,
        description="The title of the terminal.",
    )
    cwd: str = Field(
        ...,
        description="The working directory of the terminal.",
    )
    args: list[str] = Field(
        ...,
        description="The command to run in the terminal.",
    )
    env: Optional[dict[str, str | None]] = Field(
        None,
        description="Environment key-value pairs that should be added to or removed from the default environment.",
    )
    argsCanBeInterpretedByShell: Optional[bool] = Field(
        None,
        description="Whether the arguments can be interpreted as shell commands.",
    )


class RunInTerminalRequest(Request):
    """Request for 'runInTerminal' reverse request."""

    command: Literal["runInTerminal"] = "runInTerminal"
    arguments: RunInTerminalRequestArguments

    def reply(
        self,
        success: bool,
        processId: Optional[int] = None,
        shellProcessId: Optional[int] = None,
    ) -> RunInTerminalResponse:
        return RunInTerminalResponse(
            seq=self.seq,
            request_seq=self.seq,
            success=success,
            body=RunInTerminalResponseBody(
                processId=processId,
                shellProcessId=shellProcessId,
            ),
        )


class StartDebuggingRequestArguments(RequestArguments):
    """Arguments for 'startDebugging' request."""

    configuration: dict[str, str] = Field(
        ...,
        description="Arguments passed to the new debug session. The arguments must only contain properties understood by "
        "the `launch` or `attach` requests of the debug adapter and they must not contain any client-specific properties "
        "(e.g. `type`) or client-specific features (e.g. substitutable 'variables')",
    )
    request: Literal["launch", "attach"] = Field(
        ...,
        description="The request type: 'launch' or 'attach'.",
    )


class StartDebuggingRequest(Request):
    """Request for 'startDebugging' request."""

    command: Literal["startDebugging"] = "startDebugging"
    arguments: StartDebuggingRequestArguments

    def reply(self, success: bool) -> StartDebuggingResponse:
        return StartDebuggingResponse(
            seq=self.seq,
            request_seq=self.seq,
            success=success,
        )
