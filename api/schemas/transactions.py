from pydantic import BaseModel, Field
import datetime


class TransactionsSchema(BaseModel):
    
    PATIENT_UUID: str = Field(max_length=256)
    PHARMACY_UUID: str = Field(max_length=256)
    AMOUNT: float
    TIMESTAMP: datetime.datetime
