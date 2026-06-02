from sqlmodel import create_engine, Session
from pathlib import Path

DB_FILE = Path(__file__).parent.parent / "data.db"
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
