import asyncio
from typing import Optional

from .client import Client
from .connection import AsyncConnection


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
        for event in self.client.receive(r):
            self.handle_message(event)

        return True

    def handle_message(self, message):
        print(type(message), flush=True)
