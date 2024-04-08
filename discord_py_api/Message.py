from discord_py_api import User


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
