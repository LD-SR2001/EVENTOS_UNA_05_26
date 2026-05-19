import uuid
from datetime import datetime, timedelta
from models.category import Category


class Event:
    def __init__(self, name: str, address: str, category: Category,
                 event_datetime: datetime, description: str,
                 duration_hours: float = 2.0, event_id: str = None):
        self.id = event_id or str(uuid.uuid4())[:8].upper()
        self.name = name
        self.address = address
        self.category = category
        self.datetime = event_datetime
        self.description = description
        self.duration_hours = duration_hours
        self.participants: list = []

    @property
    def end_datetime(self) -> datetime:
        return self.datetime + timedelta(hours=self.duration_hours)

    def is_happening_now(self) -> bool:
        now = datetime.now()
        return self.datetime <= now <= self.end_datetime

    def is_past(self) -> bool:
        return self.end_datetime < datetime.now()

    def is_upcoming(self) -> bool:
        return self.datetime > datetime.now()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'category': self.category.value,
            'datetime': self.datetime.isoformat(),
            'description': self.description,
            'duration_hours': self.duration_hours,
            'participants': self.participants,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        event = cls(
            name=data['name'],
            address=data['address'],
            category=Category(data['category']),
            event_datetime=datetime.fromisoformat(data['datetime']),
            description=data['description'],
            duration_hours=data.get('duration_hours', 2.0),
            event_id=data['id'],
        )
        event.participants = data.get('participants', [])
        return event

    def __repr__(self) -> str:
        return f"Event(id={self.id}, name={self.name}, datetime={self.datetime})"
