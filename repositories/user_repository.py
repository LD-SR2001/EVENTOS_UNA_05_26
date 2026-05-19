import json
import os
from models.user import User

USER_FILE = 'users.data'


class UserRepository:
    def __init__(self, filepath: str = USER_FILE):
        self.filepath = filepath

    def load_all(self) -> list:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [User.from_dict(u) for u in data.get('users', [])]
        except (json.JSONDecodeError, KeyError):
            return []

    def save_all(self, users: list) -> None:
        data = {'users': [u.to_dict() for u in users]}
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
