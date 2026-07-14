from pydantic import BaseModel, EmailStr



# Registration Schema

class RegisterSchema(BaseModel):

    username: str

    email: EmailStr

    password: str

    role: str



# OAuth2 Token Response

class TokenSchema(BaseModel):

    access_token: str

    token_type: str = "bearer"



# Current User Response

class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    role: str



    class Config:

        from_attributes = True