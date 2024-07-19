import threading
import time

from .client import Client
from .connection import Connection


class Server:
    """Threaded server implementation of the DAP Client"""

    def __init__(self, adapter_id: str, host="localhost", port=6789) -> None:
        """Initializes the server with the given adapter_id, host and port

        Args:
            adapter_id (str): The adapter id
            host (str, optional): The host to connect to. Defaults to "localhost".
            port (int, optional): The port to connect to. Defaults to 6789.
        """

        self.connection = Connection(host, port)
        self.connection.start()

        self.client = Client(adapter_id)
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.client.terminate()
        self.connection.stop()

    def _run_loop(self):
        while self.running and self.connection.alive and self.run_single():
            ...

    def run_single(self):
        s = self.client.send()
        if s:
            self.connection.write(s)

        r = self.connection.read()
        if not r:
            return False

        if r:
            result = self.client.receive(r)
            for r in result:
                print(r, flush=True)

        return True
