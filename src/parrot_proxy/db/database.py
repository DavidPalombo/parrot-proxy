from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from parrot_proxy.db.models import RequestModel

DATABASE_URL = "sqlite:///parrot_proxy.db"

engine = create_engine(
    DATABASE_URL,
    ehco=False,
)

SessoinLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)