from dap import ThreadedServer

server = ThreadedServer("anyadapter")
try:
    server.start()
    while True:
        pass
except KeyboardInterrupt:
    print("Server stopped by user")
finally:
    server.stop()
