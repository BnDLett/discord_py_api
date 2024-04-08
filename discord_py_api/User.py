class User:
    def __init__(self, snowflake_id: str, username: str, display_name: str, avatar: str):
        self.id = snowflake_id
        self.username = username
        self.display_name = display_name
        self.avatar = avatar
