import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, JSON
POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'asyncio_db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5433')


PG_DSN = (f"postgresql+asyncpg://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_async_engine(PG_DSN)
SessionDB = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    
    __tablename__ = 'swapi_people'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(250))
    eye_color: Mapped[str] = mapped_column(String(250))
    films : Mapped[str] = mapped_column(String(1000))
    gender: Mapped[str] = mapped_column(String(250))
    hair_color: Mapped[str] = mapped_column(String(250))
    height: Mapped[str] = mapped_column(String(250))
    homeworld: Mapped[str] = mapped_column(String(250))
    mass: Mapped[str] = mapped_column(String(250))
    name: Mapped[str] = mapped_column(String(250))
    skin_color: Mapped[str] = mapped_column(String(250))
    species: Mapped[str] = mapped_column(String(1000))
    starships: Mapped[str] = mapped_column(String(1000))
    vehicles : Mapped[str] = mapped_column(String(1000))



async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)