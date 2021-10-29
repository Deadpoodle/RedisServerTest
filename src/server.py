import asyncio
from protocol import RedisServerProtocol


def main(hostname="localhost", port=6379):
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(RedisServerProtocol, hostname, port)
    server = loop.run_until_complete(coroutine)

    print(f"Listening on port {port}\nCtrl+C to exit.")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("User requested shutdown.")
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        print("Redis Server shutdown successfully")
    return 0


if __name__ == "__main__":
    main()
