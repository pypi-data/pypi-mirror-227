import asyncio
import websockets
import re
import threading
import time
import random
from typing import Callable

class TwitchChatListener:
    def __init__(self, CHANNEL: str, OAUTH_TOKEN:str="SCHMOOPIIE", NICKNAME:str=f"justinfan{random.randint(10000, 99999)}"):
        self.CHANNEL = "#" + CHANNEL
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.NICKNAME = NICKNAME
        self.message_handler_function = None
        self.thread = threading.Thread(target=self._run_loop)
        self._stop_requested = threading.Event()  # Use an event for stopping
        self._disconnect_timeout = 1 # seconds
        self.verbose_sysmessages = False

    def set_client_message_handler(self, handler: Callable[str, str]):
        """
        Sets the message handler function to pass the message data to
        Expects a function with arg1 = username arg2 = message
        """
        self.message_handler_function = handler

    async def messagehandler(self, message_input: str) -> None:
        match = re.match(r"^:(\w+)!\w+@\w+.tmi.twitch.tv PRIVMSG #\w+ :(.*)\r\n$", message_input)
        if match:
            username = match.group(1)
            message = match.group(2)
            self.message_handler_function(username, message)
        else:
            if self.verbose_sysmessages: print(message_input)
            ping = re.match(r"^PING :(\w+(?:\.\w+)+)", message_input)
            if ping:
                await self.ws.send(f"PONG :{ping.group(1)}")

    async def join_chat(self):
        async with websockets.connect(f"wss://irc-ws.chat.twitch.tv:443") as self.ws:
            await self.ws.send(f"PASS oauth:{self.OAUTH_TOKEN}")
            await self.ws.send(f"NICK {self.NICKNAME}")
            await self.ws.send(f"JOIN {self.CHANNEL}")

            while not self._stop_requested.is_set():
                try:
                    try:
                        message = await asyncio.wait_for(self.ws.recv(), timeout=self._disconnect_timeout)  # Add a timeout (the time it would wait for a message before checking if a disconnect has been requested)
                    except asyncio.TimeoutError:
                        pass  # Continue the loop if no message is received within the timeout
                    else:
                        await self.messagehandler(message)
                except websockets.exceptions.ConnectionClosedError:
                    print("Connection closed, attempting to reconnect")
                    await asyncio.sleep(5)
            await self.ws.send("PART")
            await self.ws.close()

    async def _start_loop(self):
        self.connected = True
        await self.join_chat()

    def _run_loop(self):
        asyncio.run(self._start_loop())

    def start(self):
        """
        Can only be called once per object, it is recomended to destroy the object after calling stop
        """
        self.thread.start()

    def stop(self):
        """
        Calling this function has a (high) possibility to hang the main thread for the maximum of self._disconnect_timeout seconds
        """
        self._stop_requested.set()
        self.thread.join(timeout=self._disconnect_timeout)

def example_chat_handler(uname: str, msg: str) -> None:
    print(f"{uname}: {msg}")

def main():
    tc = TwitchChatListener("goldenbeaster")
    tc.set_client_message_handler(example_chat_handler)
    tc.start()

    # Run your other blocking code here
    time.sleep(10)

    tc.stop()

if __name__ == "__main__":
    main()
