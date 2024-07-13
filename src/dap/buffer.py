import json
from typing import Optional


class Buffer(bytearray): ...


class RequestBuffer(Buffer):
    def __init__(
        self,
        method: str,
        params: Optional[dict[str, any]] = None,
        encoding: str = "utf-8",
    ):
        super().__init__()
        self.method = method
        self.params = params

        self.content = {
            "jsonrpc": "2.0",
            "method": method,
        }
        if params is not None:
            self.content["params"] = params

        self.encoded = json.dumps(self.content).encode(encoding)
        self.headers = f"Content-Length: {len(self.encoded)}\r\n\r\n".encode(encoding)

        super().extend(self.headers + self.encoded)

    def __repr__(self) -> str:
        return f"<RequestBuffer method={self.method!r} params={self.params!r}>"
