from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config import Config

engine = create_engine(url=Config.DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
BaseOrm = declarative_base()


@contextmanager
def get_db_session():
    """Creates new database session each time"""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


def create_db_tables():
    """Creates db tables if they are not created yet"""
    BaseOrm.metadata.create_all(engine)


class PromptHistory(BaseOrm):
    __tablename__ = "prompt_history"

    id = sa.Column(sa.Integer, primary_key=True)
    prompt = sa.Column(sa.String(1000), nullable=False)
    image_path = sa.Column(sa.String(100), nullable=False)

    def __init__(self, prompt, image_path):
        self.prompt = prompt
        self.image_path = image_path

    @classmethod
    def get_all(cls, db_session: Session):
        return db_session.query(cls).order_by(sa.desc(cls.id)).all()

    @classmethod
    def remove_all(cls, db_session: Session):
        db_session.query(cls).delete()

    @classmethod
    def find_by_id(cls, db_session: Session, prompt_id: int):
        return db_session.query(cls).filter_by(id=prompt_id).first()

    def save_to_db(self, db_session: Session):
        db_session.add(self)
        db_session.commit()

    def remove_from_db(self, db_session: Session):
        db_session.delete(self)
        db_session.commit()
