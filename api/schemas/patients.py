from pydantic import BaseModel, Field
from typing import Optional
import datetime


class PatientSchema(BaseModel):

    FIRST_NAME: str = Field(max_length=30)
    LAST_NAME: str = Field(max_length=30)
    DATE_OF_BIRTH: datetime.datetime


class PatientUpdateSchema(BaseModel):

    FIRST_NAME: Optional[str] = Field(max_length=30)
    LAST_NAME: Optional[str] = Field(max_length=30)
    DATE_OF_BIRTH: Optional[datetime.datetime]
