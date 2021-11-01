import asyncio

db = {}
accepted_commands = ["GET", "SET", "DEL"]


class RedisServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print(f"Client {transport.get_extra_info('sockname')} connected")

    def data_received(self, data):
        cmd, key, val = self.parse_command(data.decode())

        if cmd == "GET":
            response = self.handle_get(key)
            self.transport.write(response)
            return response
        elif cmd == "SET":
            response = self.handle_set(key, val)
            self.transport.write(response)
            return response
        elif cmd == "DEL":
            response = self.handle_del(key)
            self.transport.write(response)
            return response
        else:
            self.transport.write(("-ERR Unsupported command\r\n").encode())
            return ("-ERR Unsupported command\r\n").encode()

    def parse_command(self, message):
        try:
            cmd, key, val = "nil"

            message_data = message.split("\r\n")
            cmd = message_data[2].upper()

            # Ignore the initial handshake command
            if cmd == "COMMAND":
                return "nil", "nil", "nil"

            num_args = int(message_data[0][1:])

            # We're only handling GET/SET/DEL with a valid amount of args
            if cmd in accepted_commands and num_args >= 2:
                key = message_data[4]

            # Special care needed for SET
            if cmd == "SET":
                if num_args < 3:
                    # This command is invalid, not enough args
                    return "nil", "nil", "nil"
                val = message_data[6]
                # Deal with different types of values
                # I'm aware of the character that denotes the data type, but the cli seems to only send strings, so here we are
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
            return "nil", "nil", "nil"

    def handle_get(self, key):
        try:
            result = db.get(key)
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
            print("Error - User supplied invalid key")
            return b"$-1\r\n"

    def handle_set(self, key, val):
        try:
            db[key] = val
            response = f"+OK\r\n".encode()

            return response
        except Exception as e:
            print(f"Error saving kvp: {e}")
            return ("-ERR error saving key value pair\r\n").encode()

    def handle_del(self, key):
        try:
            if key in db:
                del db[key]
                response = f"+OK\r\n".encode()
            else:
                response = "-ERR Invalid key\r\n".encode()

            return response
        except Exception as e:
            print(f"Error deleting item: {e}")
            return ("-ERR Invalid key\r\n").encode()
