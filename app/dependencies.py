from fastapi import Depends, HTTPException, status

from app.jwt_handler import verify_token


def get_current_user(
    current_user: dict = Depends(verify_token)
):
    return current_user


def admin_only(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )

    return current_user


def hr_only(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "HR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="HR access required."
        )

    return current_user


def interviewer_only(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "Interviewer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Interviewer access required."
        )

    return current_user


def admin_or_hr(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] not in ["Admin", "HR"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or HR access required."
        )

    return current_user


def admin_or_interviewer(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] not in ["Admin", "Interviewer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Interviewer access required."
        )

    return current_user