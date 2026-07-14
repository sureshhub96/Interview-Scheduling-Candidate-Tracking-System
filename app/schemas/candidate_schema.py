import re

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import ConfigDict
from pydantic import field_validator


class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    experience: float
    skill_set: str


    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if not re.fullmatch(r"^[6-9]\d{9}$", value):
            raise ValueError("Invalid phone number.")

        return value


class CandidateUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    experience: float | None = None
    skill_set: str | None = None
    application_status: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if value is None:
            return value

        if not re.fullmatch(r"^[6-9]\d{9}$", value):
            raise ValueError("Invalid phone number.")

        return value


class CandidateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    experience: float
    skill_set: str
    application_status: str

    model_config = ConfigDict(
        from_attributes=True
    )