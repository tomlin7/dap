import threading

from .client import Client
from .connection import Connection


class ThreadedServer:
    """Abstract Threaded server implementation of the DAP Client

    It is meant to be used as a base class for creating a server. It handles the connection and the client.
    Following methods need to be implemented by the child class:
    - handle_message
    """

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
        """Starts the server"""

        self.running = True
        threading.Thread(target=self._run_loop, daemon=True).start()

    def stop(self):
        """Stops the server"""

        self.running = False
        self.client.terminate()
        self.connection.stop()

    def _run_loop(self):
        while self.running and self.connection.alive and self.run_single():
            ...

    def run_single(self):
        if s := self.client.send():
            self.connection.write(s)

        r = self.connection.read()
        if not r:
            return False

        for result in self.client.receive(r):
            self.handle_message(result)

        return True

    def handle_message(self, message):
        """Handles the message received from the client

        To be implemented by child classes
        Args:
            message (Any): The message to handle
        """

        print(type(message), flush=True)
