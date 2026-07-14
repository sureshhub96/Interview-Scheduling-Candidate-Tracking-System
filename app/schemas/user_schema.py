from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )