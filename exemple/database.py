import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Connexion à une base de données
engine = create_engine(os.getenv("DATABASE_URL"))

Session = sessionmaker(engine)


class Model(DeclarativeBase):
    pass
