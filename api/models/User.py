from sqlalchemy import Column, String
from database import Base
from sqlmodel import Table


class User(Base):
    
    __table__ = Table(
        "USERS",
        Base.metadata,
        Column(
            "UUID",
            String,
            primary_key=True,
            index=True,
            nullable=False),
        Column("USERNAME", String, nullable=False),
        Column("PASSWORD", String, nullable=False))