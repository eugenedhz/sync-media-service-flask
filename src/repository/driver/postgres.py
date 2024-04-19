from sqlalchemy import create_engine

from src.app import app


postgres_conn_url = app.config['POSTGRES_CONN_URL']
postgresql_engine = create_engine(postgres_conn_url, echo=False)