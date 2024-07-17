import json
from typing import Optional

CONTENT_ENCODING = "utf-8"


class Buffer(bytearray): ...


class RequestBuffer(Buffer):
    def __init__(
        self,
        seq: int,
        command: str,
        arguments: Optional[dict[str, any]] = None,
    ) -> None:
        super().__init__()
        self.seq = seq
        self.command = command
        self.arguments = arguments

        self.content = {
            "seq": self.seq,
            "type": "request",
            "command": self.command,
        }

        if self.arguments:
            self.content["arguments"] = {
                i: self.arguments[i]
                for i in self.arguments
                if self.arguments[i] is not None
            }

        self.encoded = json.dumps(self.content).encode(CONTENT_ENCODING)
        self.headers = f"Content-Length: {len(self.encoded)}\r\n\r\n".encode(
            CONTENT_ENCODING
        )

        super().extend(self.headers + self.encoded)

    def __repr__(self) -> str:
        return f"<RequestBuffer method={self.command!r} params={self.arguments!r}>"
