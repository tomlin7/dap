import asyncio
from typing import Optional

from .client import Client


class AsyncConnection:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.alive = False

    async def start(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.alive = True

    async def stop(self):
        self.writer.close()
        await self.writer.wait_closed()
        self.alive = False

    async def write(self, data: bytes):
        self.writer.write(data)
        await self.writer.drain()

    async def read(self) -> bytes:
        return await self.reader.read(1024)


class AsyncServer:
    def __init__(
        self, adapter_id: str, host: str = "localhost", port: int = 6789
    ) -> None:
        self.connection = AsyncConnection(host, port)
        self.client = Client(adapter_id)
        self.running = False
        self.loop: Optional[asyncio.AbstractEventLoop] = None

    async def start(self):
        await self.connection.start()
        self.running = True
        self.loop = asyncio.get_running_loop()
        await self._run_loop()

    async def stop(self):
        self.running = False
        self.client.terminate()
        await self.connection.stop()

    async def _run_loop(self):
        while self.running and self.connection.alive:
            await self.run_single()
            await asyncio.sleep(0.1)

    async def run_single(self):
        s = self.client.send()
        if s:
            await self.connection.write(s)

        r = await self.connection.read()
        events = self.client.receive(r)

        return True
