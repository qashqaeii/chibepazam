import mysql.connector
from mysql.connector import pooling

from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

_pool: pooling.MySQLConnectionPool | None = None


def init_pool() -> pooling.MySQLConnectionPool:
    global _pool
    if _pool is not None:
        return _pool

    _pool = pooling.MySQLConnectionPool(
        pool_name="food_bot_pool",
        pool_size=Config.DB_POOL_SIZE,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        autocommit=False,
    )
    logger.info("MySQL connection pool initialized")
    return _pool


def get_connection():
    if _pool is None:
        init_pool()
    return _pool.get_connection()
