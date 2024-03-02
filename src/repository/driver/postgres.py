from sqlalchemy import create_engine
from src.configs.app_config import Default as cfg


postgresql_engine = create_engine(cfg().POSTGRES_CONN_URL, echo=True)