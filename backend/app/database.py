from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DB_URL, echo=True)

Base = declarative_base()


# Base.metadata.create_all(engine)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():   
    db = Session()
    
    try:
        yield db
    finally:
        db.close()