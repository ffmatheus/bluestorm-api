from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from api.database import Base
from sqlmodel import Table


class Pharmacy(Base):
    
    __table__ = Table(
        "PHARMACIES",
        Base.metadata,
        Column(
            "UUID",
            String,
            primary_key=True,
            index=True,
            nullable=False),
        Column("NAME", String, nullable=False),
        Column("CITY", String, nullable=False))