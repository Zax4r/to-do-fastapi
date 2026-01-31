from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = 'sqlite:///./blog.db'

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, echo = True)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
        
