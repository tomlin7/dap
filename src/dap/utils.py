import json


def parse(data: bytes):
    header, content = data.split(b"\r\n\r\n", 1)
    content = json.loads(content.decode("utf-8"))

    headers = {
        key: value
        for key, value in (
            line.decode("ascii").split(b": ", 1) for line in header.split(b"\r\n")
        )
    }

    # only 'Content-Length' is supported
    assert "Content-Length" in headers
    assert len(headers) == 1

    return header, content
