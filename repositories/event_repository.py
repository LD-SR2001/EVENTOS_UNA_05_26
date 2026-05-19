import json
import os
from models.event import Event

DATA_FILE = 'events.data'


class EventRepository:
    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath

    def load_all(self) -> list:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Event.from_dict(e) for e in data.get('events', [])]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def save_all(self, events: list) -> None:
        data = {'events': [e.to_dict() for e in events]}
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
