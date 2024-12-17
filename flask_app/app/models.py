from app.common import Base
from typing import Any
import sqlalchemy


class User(Base):
    __tablename__ = 'user'
    id: Any = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username: Any = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email: Any = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    registration_date: Any = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

