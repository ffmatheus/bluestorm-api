from fastapi import APIRouter, Depends, HTTPException
from api.auth import AuthHandler
from sqlalchemy import desc
from sqlmodel import Session
from api.init import app
from api.models.Pharmacy import Pharmacy
from api.schemas.pharmacies import PharmacySchema, PharmacyUpdateSchema
from api.database import get_db


router = APIRouter()
auth_handler = AuthHandler()


@app.get(
    "/pharmacies",
    tags=["Pharmacies"])
def get_pharmacies(
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Return all pharmacies
    """
    result = db.query(
        Pharmacy
    ).all()
    return result


@app.post(
    "/pharmacies",
    status_code=201,
    tags=["Pharmacies"])
def create_pharmacy(
    pharmacy: PharmacySchema,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Create a pharmacy
    """
    id = db.query(
        Pharmacy.UUID
    ).order_by(
        desc(Pharmacy.UUID)
    ).first()
    uuid_str = "PHARM{}"
    uuid_number = str(id[0][-4:])
    number = '%04d' % (int(uuid_number) + 1)
    db_pharmacy = Pharmacy(
        **pharmacy.dict())
    db_pharmacy.UUID = uuid_str.format(number)
    db.add(db_pharmacy)
    db.commit()
    return True


@app.patch(
    "/pharmacies/{UUID}",
    status_code=201,
    tags=["Pharmacies"])
def update_pharmacy(
    uuid: str,
    pharmacy_upload: PharmacyUpdateSchema,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Update a pharmacy
    """
    pharmacy = db.query(
        Pharmacy
    ).filter(
        Pharmacy.UUID == uuid
    ).first()
    if not pharmacy:
        raise HTTPException(
            status_code=404,
            detail="UUID not found."
        )
    pharmacy_data = pharmacy_upload.dict(exclude_unset=True)
    for key, value in pharmacy_data.items():
        setattr(pharmacy, key, value)
    db.add(pharmacy)
    db.commit()
    return True


@app.delete(
    "/pharmacies/{UUID}",
    status_code=201,
    tags=["Pharmacies"])
def delete_pharmacy(
    uuid: str,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Delete a pharmacy
    """
    pharmacy = db.query(
        Pharmacy
    ).filter(
        Pharmacy.UUID == uuid
    ).first()
    if not pharmacy:
        raise HTTPException(
            status_code=404,
            detail="UUID not found."
        )
    db.delete(pharmacy)
    db.commit()
    return True