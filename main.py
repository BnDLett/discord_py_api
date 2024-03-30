import json
import time
import requests
# import websocket
from requests import Response

# wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream


class Debug:
    INFO = "INFO"
    DEBUG = "DEBUG"

    def __init__(self, debug: bool):
        self.debug = debug
        self.start_time = time.time()

    def message(self, level: str, message: str):
        if self.debug is None:
            return

        elif level == self.INFO:
            print(f"[{(time.time() - self.start_time):.3f}] [{level}]: {message}")
            return

        elif not self.debug:
            return

        print(f"[{(time.time() - self.start_time):.3f}] [{level}]: {message}")


class User:
    def __init__(self, id: str, username: str, display_name: str, avatar: str):
        self.id = id
        self.username = username
        self.display_name = display_name
        self.avatar = avatar


class Message:
    def __init__(self, content: str, message_id: str, author: User):
        """
        A class for Discord messages.
        :param content: The content of the message.
        :param message_id: The ID of the message.
        :param author: The author of the message.
        """
        self.content = content
        self.message_id = message_id
        self.author = author


class Client:
    def __init__(self, token: str = None, username: str = None, password: str = None, auth_code: str = None,
                 debug: bool = None) -> None:
        if token is None:
            token = self.authenticate(username, password, auth_code)

        self.__data = {"Authorization": token}
        token = None
        self.debugger = Debug(debug)

    def type(self, channel: str) -> Response:
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/typing", headers=self.__data)
        return r

    def send_message(self, channel: str, message: str) -> Response:
        json = {"content": message, "tts": False, "flags": 0}

        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=self.__data, json=json)
        return r

    def get_messages(self, channel: str, limit: int = 1) -> list:
        r = requests.get(f"https://discord.com/api/v9/channels/{channel}/messages?limit={limit}",
                         headers=self.__data)

        self.debugger.message(self.debugger.INFO, str(r.status_code))
        json_messages: list = json.loads(r.content)
        message_list = []

        for message in json_messages:
            message_list.append(Message(
                message['content'],
                message['id'],
                User(
                    message['author']['id'],
                    message['author']['username'],
                    message['author']['global_name'],
                    message['author']['avatar']
                )
            ))

        return message_list

    @staticmethod
    def authenticate(username: str, password: str, auth_code: str = None) -> str:
        __json = {"login": f"{username}", "password": f"{password}", "undelete": False}
        __r = requests.post("https://discord.com/api/v9/auth/login", json=__json)
        if "ticket" not in __r.json():
            __token = __r.json()['token']
            return __token

        if auth_code is None:
            raise Exception("An auth code was needed but none was provided.")

        __totp_json = {"code": f"{auth_code}", "ticket": f"{__r.json()['ticket']}"}
        __totp = requests.post("https://discord.com/api/v9/auth/mfa/totp", json=__totp_json)
        __token = __totp.json()['token']

        return __token


if __name__ == "__main__":
    import maskpass

    # username = input("Enter username:\n> ")
    # password = maskpass.askpass("Enter password:\n> ", '*')
    # code = input("Enter auth code (leave blank if there is none):\n> ")

    # if code == "".strip(): code = None

    # user = User(username=username, password=password, auth_code=code)
    input_token = maskpass.askpass("Enter token:\n> ", '*')
    user = Client(token=input_token, debug=True)

    channel = input("Please enter a channel ID:\n> ")
    messages: list[Message] = user.get_messages(channel, limit=10)
    messages.reverse()

    for x in messages:
        print(f"[{x.author.display_name if x.author.display_name is not None else x.author.username}]: {x.content}")
