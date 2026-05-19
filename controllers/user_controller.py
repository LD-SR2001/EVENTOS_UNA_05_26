from models.user import User
from repositories.user_repository import UserRepository


class UserController:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self._users: list = repository.load_all()
        self.current_user = None

    def register(self, name: str, email: str, cpf: str,
                 phone: str, city: str):
        if self.find_by_cpf(cpf):
            return None
        user = User(name=name, email=email, cpf=cpf, phone=phone, city=city)
        self._users.append(user)
        self._save()
        self.current_user = user
        return user

    def login(self, cpf: str):
        user = self.find_by_cpf(cpf)
        if user:
            self.current_user = user
        return user

    def logout(self) -> None:
        self.current_user = None

    def save_current_user(self) -> None:
        self._save()

    def find_by_cpf(self, cpf: str):
        clean = cpf.replace('.', '').replace('-', '').strip()
        return next(
            (u for u in self._users
             if u.cpf.replace('.', '').replace('-', '') == clean),
            None,
        )

    def _save(self) -> None:
        self.repository.save_all(self._users)
