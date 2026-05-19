import uuid


class User:
    def __init__(self, name: str, email: str, cpf: str,
                 phone: str, city: str, user_id: str = None):
        self.id = user_id or str(uuid.uuid4())[:8].upper()
        self.name = name
        self.email = email
        self.cpf = cpf
        self.phone = phone
        self.city = city
        self.confirmed_events: list = []

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'cpf': self.cpf,
            'phone': self.phone,
            'city': self.city,
            'confirmed_events': self.confirmed_events,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        user = cls(
            name=data['name'],
            email=data['email'],
            cpf=data['cpf'],
            phone=data['phone'],
            city=data['city'],
            user_id=data['id'],
        )
        user.confirmed_events = data.get('confirmed_events', [])
        return user

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"
