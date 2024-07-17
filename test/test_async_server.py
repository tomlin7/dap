import asyncio

from dap import AsyncServer


async def main():
    server = AsyncServer("anyadapter")
    try:
        await server.start()
    except asyncio.CancelledError:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
