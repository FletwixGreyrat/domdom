
from config import settings
from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


class Question1(Base):
    type_of_answer: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(BIGINT)
    date: Mapped[str] = mapped_column()


class Question2(Base):
    type_of_answer: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(BIGINT)
    date: Mapped[str] = mapped_column()


class Question3(Base):
    type_of_answer: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(BIGINT)
    date: Mapped[str] = mapped_column()


class Question4(Base):
    type_of_answer: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(BIGINT)
    date: Mapped[str] = mapped_column()


class Question5(Base):
    type_of_answer: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(BIGINT)
    date: Mapped[str] = mapped_column()



class FormIsPassed(Base):
    user_id: Mapped[int] = mapped_column(BIGINT)


from sqlalchemy import create_engine
from config import settings
from os import getenv
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")


url: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
from sqlalchemy import insert
engine = create_engine(url=url, echo=settings.echo)

# with engine.connect() as connection:
#     connection.execute(insert(Question1).values(user_id="6142402831", type_of_answer="1", date="2024.12.04"))
#     connection.commit()

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
