from fastapi import APIRouter, Depends, status

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session


from app.database import get_db

from app.schemas.auth_schema import (
    RegisterSchema,
    TokenSchema
)


from app.services.auth_service import (
    register_user,
    login_user
)



router = APIRouter()



@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    request: RegisterSchema,
    db: Session = Depends(get_db)
):

    return register_user(
        request,
        db
    )




@router.post(
    "/login",
    response_model=TokenSchema
)
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    return login_user(
        username=form_data.username,
        password=form_data.password,
        db=db
    )