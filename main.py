import requests, json
from requests import Response


class User:
    def __init__(self, token: str = None, username: str = None, password: str = None, auth_code: str = None) -> None:
        if token is None:
            token = self.authenticate(username, password, auth_code)

        self.__data = {"Authorization": token}
        token = None

    def type(self, channel: str) -> Response:
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/typing", headers=self.__data)
        return r

    def send_message(self, channel: str, message: str) -> Response:
        json = {"content": message, "tts": False, "flags": 0}

        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers=self.__data, json=json)
        return r

    def get_messages(self, channel: str, limit: int = 1) -> list:
        r = requests.get(f"https://discord.com/api/v9/channels/{channel}/messages?limit={limit}",
                         headers=self.__data).content

        messages: list = json.loads(r)

        return messages

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

    username = input("Enter username:\n> ")
    password = maskpass.askpass("Enter password:\n> ", '*')
    code = input("Enter auth code (leave blank if there is none):\n> ")

    if code == "".strip(): code = None

    user = User(username=username, password=password, auth_code=code)

    channel = input("Please enter a channel ID:\n> ")
    messages = user.get_messages(channel, limit=10)
    messages.reverse()

    for x in messages:
        print(f"[{x['author']['username']}]: {x['content']}")
