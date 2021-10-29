# multiple users can connect at once,
# #need some way to lock rows they're working on, store the change, queue it, apply after?

import asyncio
import os
import sys

db = {}
accepted_commands = ["GET", "SET", "DEL"]
queue = asyncio.Queue()  # TODO


class RedisServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print(f"Client {transport.get_extra_info('sockname')} connected")

    def data_received(self, data):
        print(f"Raw Data Received: {data}")
        cmd, key, val = self.parse_command(data.decode())
        print(f"cmd: {cmd}, key: {key}, val: {val}")

        if cmd == "GET":
            response = self.handle_get(key)
            print(f"GET Response: {response}")
            self.transport.write(response)
            return response
        elif cmd == "SET":
            response = self.handle_set(key, val)
            print(f"SET Response: {response}")
            self.transport.write(response)
            return response
        elif cmd == "DEL":
            response = self.handle_del(key)
            print(f"DEL Response: {response}")
            self.transport.write(response)
            return response
        else:
            self.transport.write(("-ERR Unsupported command\r\n").encode())
            return ("-ERR Unsupported command\r\n").encode()

    def parse_command(self, message):
        try:
            cmd, key, val = "nil"

            message_data = message.split("\r\n")
            print(f"message_data: {message_data}")

            cmd = message_data[2].upper()
            print(f"cmd: {cmd}")

            # Ignore the initial handshake command
            if cmd == "COMMAND":
                return "nil", "nil", "nil"

            print(f"num args: {message_data[0][1:]}")
            num_args = int(message_data[0][1:])

            # We're only handling GET/SET/DEL with a valid amount of args
            if cmd in accepted_commands and num_args >= 2:
                key = message_data[4]
                print(f"key: {key}")

            # Special care needed for SET
            if cmd == "SET":
                if num_args < 3:
                    # This command is invalid, not enough args
                    return "nil", "nil", "nil"
                val = message_data[6]
                print(f"val: {val}")
                # Deal with different types of values
                if val.isnumeric():
                    val = int(val)
                elif val.upper() == "TRUE" or val.upper() == "FALSE":
                    val = True if val.upper() == "TRUE" else False
                else:
                    # At this point it must be a float or a string
                    try:
                        val = float(val)
                    except:
                        pass

            return cmd, key, val
        except Exception as e:
            print(f"Error parsing command: {e}")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return "nil", "nil", "nil"

    def handle_get(self, key):
        try:
            # result = queue.put(db.get(key))
            print(f"DB from test: {db}")
            result = db.get(key)
            print(f"db.get('{key}') : {result}")
            if result == None:
                response = (f"$-1\r\n").encode()
            elif type(result) == bool:
                response = (f"+{result}\r\n").encode()
            elif isinstance(result, int):
                response = (f":{result}\r\n").encode()
            else:
                response = (f"+{result}\r\n").encode()

            return response
        except:
            print("ERR - User supplied invalid key")
            return b"$-1\r\n"

    def handle_set(self, key, val):
        try:
            # queue.put(db[key] = val)
            db[key] = val
            response = f"+OK\r\n".encode()

            return response
        except Exception as e:
            print(f"ERR - Error saving kvp: {e}")
            return ("-ERR error saving key value pair\r\n").encode()

    def handle_del(self, key):
        try:
            # queue.put(del db[key])
            if key in db:
                del db[key]
                response = f"+OK\r\n".encode()
            else:
                response = "-ERR Invalid key\r\n".encode()

            return response
        except Exception as e:
            print(f"Error deleting item: {e}")
            return ("-ERR Invalid key\r\n").encode()
