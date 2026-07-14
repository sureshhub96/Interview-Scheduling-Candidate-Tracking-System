import re

from fastapi import HTTPException, status


PHONE_PATTERN = r"^[6-9]\d{9}$"

VALID_ROLES = [
    "Admin",
    "HR",
    "Interviewer"
]

VALID_INTERVIEW_STATUS = [
    "Scheduled",
    "Completed",
    "Cancelled",
    "Selected",
    "Rejected"
]

VALID_APPLICATION_STATUS = [
    "Applied",
    "Screening",
    "Interview Scheduled",
    "Selected",
    "Rejected"
]

VALID_INTERVIEW_MODE = [
    "Online",
    "Offline"
]


def validate_phone(phone: str):
    """
    Validate Indian mobile number.
    """

    if not re.fullmatch(PHONE_PATTERN, phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Enter a valid 10-digit Indian mobile number."
        )

    return phone


def validate_role(role: str):
    """
    Validate user role.
    """

    if role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of {VALID_ROLES}"
        )

    return role


def validate_interview_mode(mode: str):
    """
    Validate interview mode.
    """

    if mode not in VALID_INTERVIEW_MODE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview mode must be Online or Offline."
        )

    return mode


def validate_interview_status(status_value: str):
    """
    Validate interview status.
    """

    if status_value not in VALID_INTERVIEW_STATUS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Interview status must be one of {VALID_INTERVIEW_STATUS}"
        )

    return status_value


def validate_application_status(status_value: str):
    """
    Validate candidate application status.
    """

    if status_value not in VALID_APPLICATION_STATUS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Application status must be one of {VALID_APPLICATION_STATUS}"
        )

    return status_value


def validate_rating(rating: int):
    """
    Validate interview rating (1-5).
    """

    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5."
        )

    return rating