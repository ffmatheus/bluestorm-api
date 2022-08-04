from uuid import UUID
from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from database import Base
from sqlmodel import Table
from models import Patient, Pharmacy


class Transaction(Base):
    
    __table__ = Table(
        "TRANSACTIONS",
        Base.metadata,
        Column(
            "UUID",
            String,
            primary_key=True,
            index=True,
            nullable=False),
        Column(
            "PATIENT_UUID",
            String,
            ForeignKey(Patient.Patient.UUID),
            nullable=False),
        Column(
            "PHARMACY_UUID",
            String,
            ForeignKey(Pharmacy.Pharmacy.UUID),
            nullable=False),
        Column("AMOUNT", Numeric, nullable=True),
        Column("TIMESTAMP", DateTime, nullable=True))