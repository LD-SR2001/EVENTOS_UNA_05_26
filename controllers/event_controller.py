from models.event import Event
from models.user import User
from repositories.event_repository import EventRepository


class EventController:
    def __init__(self, repository: EventRepository):
        self.repository = repository
        self._events: list = repository.load_all()

    def get_upcoming_events(self) -> list:
        return sorted(
            [e for e in self._events if e.is_upcoming()],
            key=lambda e: e.datetime,
        )

    def get_past_events(self) -> list:
        return sorted(
            [e for e in self._events if e.is_past()],
            key=lambda e: e.datetime,
            reverse=True,
        )

    def get_happening_now(self) -> list:
        return [e for e in self._events if e.is_happening_now()]

    def get_all_sorted(self) -> list:
        return sorted(self._events, key=lambda e: e.datetime)

    def get_event_by_id(self, event_id: str):
        return next((e for e in self._events if e.id == event_id), None)

    def add_event(self, event: Event) -> None:
        self._events.append(event)
        self._save()

    def confirm_participation(self, event: Event, user: User) -> bool:
        if user.id in event.participants:
            return False
        event.participants.append(user.id)
        if event.id not in user.confirmed_events:
            user.confirmed_events.append(event.id)
        self._save()
        return True

    def cancel_participation(self, event: Event, user: User) -> bool:
        if user.id not in event.participants:
            return False
        event.participants.remove(user.id)
        if event.id in user.confirmed_events:
            user.confirmed_events.remove(event.id)
        self._save()
        return True

    def get_user_events(self, user: User) -> list:
        return sorted(
            [e for e in self._events if e.id in user.confirmed_events],
            key=lambda e: e.datetime,
        )

    def _save(self) -> None:
        self.repository.save_all(self._events)
