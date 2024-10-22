import os
from alembic import config
from alembic import command
from app.db import engine


def _alembic_cfg() -> config.Config:
    cfg = config.Config()
    cfg.set_main_option("script_location", os.path.join(os.getcwd(), './alembic'))
    cfg.set_main_option('sqlalchemy.url', f'sqlite:///ddos.db')
    cfg.set_main_option('version_path_separator', 'os')
    cfg.set_main_option('prepend_sys_path', '.')
    return cfg


def create_database():
    if not os.path.exists('./ddos.db'):
        try:
            cfg = _alembic_cfg()
            with engine.begin() as connection:
                cfg.attributes['connection'] = connection
                command.upgrade(cfg, "head")
        except Exception as e:
            raise e
