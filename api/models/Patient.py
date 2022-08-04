from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from database import Base
from sqlmodel import Table


class Patient(Base):
    
    __table__ = Table(
        "PATIENTS",
        Base.metadata,
        Column(
            "UUID",
            String,
            primary_key=True,
            index=True,
            nullable=False),
        Column("FIRST_NAME", String, nullable=False),
        Column("LAST_NAME", String, nullable=False),
        Column("DATE_OF_BIRTH", DateTime, nullable=True))