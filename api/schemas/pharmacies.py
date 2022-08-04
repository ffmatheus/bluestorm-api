from pydantic import BaseModel, Field
from typing import Optional


class PharmacySchema(BaseModel):

    NAME: str = Field(max_length=50)
    CITY: str = Field(max_length=50)

class PharmacyUpdateSchema(BaseModel):

    NAME: Optional[str] = Field(max_length=50)
    CITY: Optional[str] = Field(max_length=50)