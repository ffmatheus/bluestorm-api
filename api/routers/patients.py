from fastapi import APIRouter, Depends, HTTPException
from api.auth import AuthHandler
from sqlmodel import Session
from sqlalchemy import desc, or_
from api.schemas.patients import PatientSchema, PatientUpdateSchema
from api.start import app
from api.models.Patient import Patient
from api.database import get_db
from typing import Optional

router = APIRouter()
auth_handler = AuthHandler()


@app.get(
    "/patients",
    tags=["Patients"])
def get_patients(
    search: Optional[str] = None,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Return all patients
    """
    if search is None:
        result = db.query(
            Patient
        ).all()
    else:
        result = db.query(
            Patient
        ).filter(or_(
                Patient.FIRST_NAME.contains(search),
                Patient.LAST_NAME.contains(search)
        )).all()
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
    "/patients/{UUID}",
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