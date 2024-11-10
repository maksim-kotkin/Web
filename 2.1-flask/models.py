import datetime
import os
from sqlalchemy import  create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from atexit import register


POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'flask_db')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5433')

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

# class User(Base):
#     __tablename__ = "app_user"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
#     email: Mapped[str] = mapped_column(String(64), nullable=False)
#     password: Mapped[str] = mapped_column(String(72), nullable=False)
#     registration_time: Mapped[datetime.datetime] = mapped_column(
#         DateTime, server_default=func.now()
#     )
#     @property
#     def json(self):
#         return{
#             'id': self.id,
#             'name': self.name,
#             'email': self.email,
#             'registration_time': self.registration_time.isoformat()
#         }
        

class Advertisement(Base):
    __tablename__ = "app_adv"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner: Mapped[str] = mapped_column(String(64), nullable=False)
    # owner_id:Mapped[int] =  mapped_column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    title:Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description:Mapped[str] = mapped_column(String(500),nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    
    @property
    def json(self):
        return{
            'id': self.id,
            'owner': self.owner,
            # 'owner_id': self.owner_id,
            'title': self.title,
            'description': self.description,
            'registration_time': self.registration_time.isoformat()
        }
# Base.metadata.drop_all(bind=engine)       
Base.metadata.create_all(bind=engine)

register(engine.dispose)