import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "che_bepazam")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ADMIN_IDS: list[int] = [
        int(x.strip())
        for x in os.getenv("ADMIN_IDS", "").split(",")
        if x.strip().isdigit()
    ]

    HISTORY_MAX: int = 50
    FAVORITES_PER_PAGE: int = 5
    RECIPES_PER_PAGE: int = 5
    INGREDIENTS_PER_PAGE: int = 8
    CALLBACK_DATA_MAX: int = 64

    @classmethod
    def validate(cls) -> None:
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required in .env")
