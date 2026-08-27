from database.repositories.users import UsersRepository


class UserService:
    def __init__(self):
        self.repo = UsersRepository()

    def register(self, telegram_id: int, username: str | None, first_name: str | None, last_name: str | None) -> dict:
        return self.repo.get_or_create(telegram_id, username, first_name, last_name)

    def get_user(self, telegram_id: int) -> dict | None:
        return self.repo.get_by_telegram_id(telegram_id)

    def is_admin(self, telegram_id: int) -> bool:
        return self.repo.is_admin(telegram_id)
