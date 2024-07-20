from __future__ import annotations

import asyncio
import queue
import socket
from threading import Thread
from typing import Optional


class AsyncConnection:
    """Asyncio-based connection to a debug adapter server.

    This class is used to connect to a debug adapter server using asyncio.
    It provides methods to start, stop, read and write to the server."""

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.alive = False

    async def start(self):
        """Start the connection to the server."""

        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.alive = True

    async def stop(self):
        """Stop the connection to the server."""

        self.writer.close()
        await self.writer.wait_closed()
        self.alive = False

    async def write(self, data: bytes):
        """Write data to the server

        Args:
            data (bytes): The data to write to the server.
        """

        self.writer.write(data)
        await self.writer.drain()

    async def read(self) -> bytes:
        """Read data from the server

        Returns:
            bytes: The data read from the server.
        """

        return await self.reader.read(1024)


class Connection:
    """Connection to a debug adapter server.

    This class is used to connect to a debug adapter server using threads.
    It provides methods to start, stop, read and write to the server."""

    def __init__(self, host="localhost", port=6789):
        self.alive = True
        self.host = host
        self.port = port

        self.out_queue = queue.Queue()

    def write(self, buf: bytes) -> None:
        """Write data to the server

        Args:
            buf (bytes): The data to write to the server.
        """

        self.sock.sendall(buf)

    def read(self) -> None:
        """Read data from the server

        Returns:
            bytes: The data read from the server.
        """

        buf = bytearray()
        while True:
            try:
                buf += self.out_queue.get(block=False)
            except queue.Empty:
                break

        if self.t_out.is_alive() and not buf:
            return None
        return bytes(buf)

    def start(self, *_) -> None:
        """Start the connection to the server."""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.t_out = Thread(target=self._process_output, daemon=True)
        self.t_out.start()

    def stop(self, *_) -> None:
        """Stop the connection to the server."""

        self.alive = False
        self.sock.close()

    def _process_output(self) -> None:
        while self.alive:
            try:
                data = self.sock.recv(1024)
            except ConnectionAbortedError:
                break
            except ConnectionResetError:
                break

            if not data:
                break

            self.out_queue.put(data)
