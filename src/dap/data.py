from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel, Field


class ProtocolMessage(BaseModel):
    """Base class of requests, responses, and events"""

    seq: int = Field(..., description="Sequence number (message ID) of the message.")
    type: Union[Literal["request", "response", "event"], str] = Field(
        ..., description="Message type."
    )


class Request(ProtocolMessage):
    type: str = "request"
    command: str = Field(..., description="The command to execute.")
    arguments: Optional[Any] = Field(
        ..., description="Object containing arguments for the command."
    )


class Event(ProtocolMessage):
    type: str = "event"
    event: str = Field(..., description="The event type.")
    body: Optional[Any] = Field(None, description="Event-specific information.")


class Response(ProtocolMessage):
    type: str = "response"
    request_seq: int = Field(
        ..., description="Sequence number of the corresponding request."
    )
    success: bool = Field(
        ..., description="Indicates whether the request was successful."
    )
    command: str = Field(..., description="The command requested.")
    message: Optional[Union[Literal["cancelled", "notStopped"], str]] = Field(
        None, description="Raw error message if success is False."
    )
    body: Optional[Any] = Field(
        None, description="Request result if success is true, error details otherwise."
    )


class ErrorBody(BaseModel):
    # TODO use Message object
    error: Optional[Any] = Field(
        ...,
        description="Error details.",
    )


class ErrorResponse(Response):
    body: ErrorBody = Field(..., description="Error details.")


DAPMessage = Union[Request, Response, Event]
