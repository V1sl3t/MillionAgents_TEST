from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine("sqlite:///./sqlite.db")

session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


class ShortLink(Base):
    __tablename__ = 'short_links'

    id: Mapped[int] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(unique=True, nullable=False)
    original_url: Mapped[str] = mapped_column(nullable=False)


def get_db():
    with session_maker() as db:
        yield db

Base.metadata.create_all(bind=engine)