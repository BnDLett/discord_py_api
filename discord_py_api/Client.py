import json

import requests
from requests import Response

from discord_py_api.Debug import Debug
from discord_py_api.Message import Message
from discord_py_api.User import User


class Client:
    def __init__(self, token: str = None, username: str = None, password: str = None, auth_code: str = None,
                 debug: bool = None) -> None:
        if token is None:
            token = self.authenticate(username, password, auth_code)

        self.__data = {"Authorization": token}
        del token
        self.debugger = Debug(debug)

    def type(self, channel: str) -> Response:
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/typing", headers=self.__data)
        return r

    def send_message(self, channel: str, message: str) -> Response:
        payload = {"content": message, "tts": False, "flags": 0}

        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=self.__data, json=payload)
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
