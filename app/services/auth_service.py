from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth_schema import RegisterSchema
from app.hashing import hash_password, verify_password
from app.jwt_handler import create_access_token


VALID_ROLES = [
    "Admin",
    "HR",
    "Interviewer"
]


# ---------------------------------------------------
# Register User
# ---------------------------------------------------

def register_user(
    request: RegisterSchema,
    db: Session
):
    try:

        # Check username
        existing_username = db.query(User).filter(
            User.username == request.username
        ).first()

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )

        # Check email
        existing_email = db.query(User).filter(
            User.email == request.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists."
            )

        # Validate role
        if request.role not in VALID_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role must be one of {VALID_ROLES}"
            )

        # Create user
        new_user = User(
            username=request.username,
            email=request.email,
            password=hash_password(request.password),
            role=request.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {str(e)}"
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration Error: {str(e)}"
        )


# ---------------------------------------------------
# Login User (OAuth2)
# ---------------------------------------------------

def login_user(
    username: str,
    password: str,
    db: Session
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    if not verify_password(
        password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }