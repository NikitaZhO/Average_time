from fastapi import FastAPI
from uvicorn import Config, Server
import logging
from app.api.api import router
from app.utils import setup_logging
from app.init_migrations import create_database
from config import host, port

app = FastAPI()


def build_app() -> Server:
    logging.info("Запуск приложения")
    app.include_router(router, prefix="")
    setup_logging()  # Инициализация логирования
    create_database()  # Применение миграций alembic

    server = Server(
        Config(
            app,
            host=host,
            port=port
        )
    )
    return server


def start_app() -> None:
    build_app().run()
