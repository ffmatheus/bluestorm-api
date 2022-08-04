from pydantic import BaseModel, Field


class UserSchema(BaseModel):

    USERNAME: str = Field(max_length=50)
    PASSWORD: str = Field(max_length=256)

