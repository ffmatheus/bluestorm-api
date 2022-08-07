from fastapi import APIRouter, Depends, HTTPException
from api.schemas.transactions import TransactionsSchema
from api.auth import AuthHandler
from api.start import app
from sqlmodel import Session
from sqlalchemy import desc
from api.database import get_db
from api.models.Transaction import Transaction
from api.models.Patient import Patient
from api.models.Pharmacy import Pharmacy

router = APIRouter()
auth_handler = AuthHandler()


@app.get(
    "/transactions",
    tags=["Transactions"])
def get_transactions(
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Return all transactions
    """
    result = db.query(
        Transaction.PATIENT_UUID,
        Patient.FIRST_NAME,
        Patient.LAST_NAME,
        Patient.DATE_OF_BIRTH,
        Transaction.PHARMACY_UUID,
        Pharmacy.NAME,
        Pharmacy.CITY,
        Transaction.UUID,
        Transaction.AMOUNT,
        Transaction.TIMESTAMP
    ).join(
        Patient,
        Pharmacy
    ).filter(
        Transaction.PATIENT_UUID == Patient.UUID,
        Transaction.PHARMACY_UUID == Pharmacy.UUID
    ).all()
    return result


@app.post(
    "/transactions",
    status_code=201,
    tags=["Transactions"])
def create_transaction(
    transaction: TransactionsSchema,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Create a transaction
    """
    exist_patient = db.query(
        Patient.UUID
    ).filter(
        Patient.UUID == transaction.PATIENT_UUID
    ).first()

    if not exist_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found! Verify patient UUID."
        )
    
    exist_pharmacy = db.query(
        Pharmacy.UUID
    ).filter(
        Pharmacy.UUID == transaction.PHARMACY_UUID
    ).first()

    if not exist_pharmacy:
        raise HTTPException(
            status_code=404,
            detail="Pharmacy not found! Verify pharmacy UUID."
        )
    
    id = db.query(
        Transaction.UUID
    ).order_by(
        desc(Transaction.UUID)
    ).first()
    uuid_str = "TRAN{}"
    uuid_number = str(id[0][-4:])
    number = '%04d' % (int(uuid_number) + 1)
    db_transaction = Transaction(
        **transaction.dict())
    db_transaction.UUID = uuid_str.format(number)
    db.add(db_transaction)
    db.commit()
    return True
