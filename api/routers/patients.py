from fastapi import APIRouter, Depends, HTTPException
from auth import AuthHandler
from sqlmodel import Session
from sqlalchemy import desc
from schemas.patients import PatientSchema, PatientUpdateSchema
from start import app
from models.Patient import Patient
from database import get_db

router = APIRouter()
auth_handler = AuthHandler()


@app.get(
    "/patients",
    tags=["Patients"])
def get_patients(
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Return all patients
    """
    result = db.query(
        Patient
    ).all()
    return result


@app.post(
    "/patients",
    status_code=201,
    tags=["Patients"])
def create_patient(
    patient: PatientSchema,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Create a patient
    """
    id = db.query(
        Patient.UUID
    ).order_by(
        desc(Patient.UUID)
    ).first()
    uuid_str = "PATIENT{}"
    uuid_number = str(id[0][-4:])
    number = '%04d' % (int(uuid_number) + 1)
    db_patient = Patient(
        **patient.dict())
    db_patient.UUID = uuid_str.format(number)
    db.add(db_patient)
    db.commit()
    return True


@app.patch(
    "/patient/{UUID}",
    status_code=201,
    tags=["Patients"])
def update_patient(
    uuid: str,
    patient_upload: PatientUpdateSchema,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Update a patient
    """
    patient = db.query(
        Patient
    ).filter(
        Patient.UUID == uuid
    ).first()
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="UUID not found."
        )
    patient_data = patient_upload.dict(exclude_unset=True)
    for key, value in patient_data.items():
        setattr(patient, key, value)
    db.add(patient)
    db.commit()
    return True


@app.delete(
    "/patients/{UUID}",
    status_code=201,
    tags=["Patients"])
def delete_patient(
    uuid: str,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Delete a patient
    """
    patient = db.query(
        Patient
    ).filter(
        Patient.UUID == uuid
    ).first()
    if not patient:
        raise HTTPException(
            status_code=404,
            detail="UUID not found."
        )
    db.delete(patient)
    db.commit()
    return True