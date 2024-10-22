from fastapi import FastAPI
from uvicorn import Config, Server
from app.api.api import router
from app.utils import setup_logging
from app.init_migrations import create_database

app = FastAPI()


def build_app() -> Server:
    app.include_router(router, prefix="")
    setup_logging()  # Инициализация логирования
    create_database()  # Инициализация миграций alembic

    server = Server(
        Config(
            app,
            host='127.0.0.1',
            port=9313
        )
    )
    return server


def start_app() -> None:
    build_app().run()
