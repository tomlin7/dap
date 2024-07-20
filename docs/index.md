# Debug Adapter Client for Python

DAP Client is an up-to-date generic client side implementation of the [Debug Adapter Protocol (DAP)](https://microsoft.github.io/debug-adapter-protocol/) that is used in IDEs, editors and other tools to communicate with different debuggers. The client is not tied to any specific debugger, so it can be used to interact with any debug adapter that implements the DAP protocol, significantly reducing the effort required to build a new debugging tool.

## Key Features

- **Sans I/O Implementation**: A protocol-only client that can be integrated into any I/O framework.
- **Abstract Clients**: Ready-to-use threaded and asyncio clients for immediate integration.
- **Flexible Architecture**: Easily extensible to support various debugging scenarios.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Usage Examples](#usage-examples)
4. [API Reference](#api-reference)
5. [License](#license)

## Installation

Install DAP Client using pip:

```bash
pip install dap-client
```

## Quick Start

The following example demonstrates how to use the async client to connect to a [`debugpy`](https://aka.ms/debugpy) debug adapter server that is running on port 1234.

```bash
python -m debugpy --listen localhost:1234 --wait-for-client hello.py
```

```python
import asyncio
from dap import AsyncServer

async def main():
    server = AsyncServer("debugpy", port=1234)
    try:
        await server.start()
    except asyncio.CancelledError:
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Usage Examples

### Using the Sans I/O Client

The sans I/O client allows you to implement your own I/O mechanism:

```python
from dap import Client
from dap.responses import Initialized

client = Client()
client.launch(no_debug=True)

# get the request data
request = client.send()

# send the request using your I/O implementation
# ...

# feed the response data to the client
for result in client.receive(response_data):
    if isinstance(result, Initialized):
        print("The debug adapter is initialized.")
    ...
```

### Using the Threaded Socket IO Client

The threaded client provides a simple interface for synchronous usage:

```python
from dap import ThreadedServer

server = ThreadedServer("debugpy", port=1234)
server.start()
client = server.client

# Use the client synchronously
client.launch()
client.disconnect()
server.stop()
```

### Using the Asyncio Client

The asyncio client offers an asynchronous interface:

```python
import asyncio
from dap import AsyncServer

async def debug_session():
    server = AsyncServer("debugpy", port=1234)
    server.start()
    client = server.client

    client.launch()
    client.disconnect()
    server.stop()

asyncio.run(debug_session())
```

## License

DAP Client is released under the [MIT License](../LICENSE).
