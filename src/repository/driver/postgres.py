from sqlalchemy import create_engine
from src.configs.app_config import POSTGRES_CONN_URL


engine = create_engine(POSTGRES_CONN_URL, echo=True)