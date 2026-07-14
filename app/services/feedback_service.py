from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.feedback import Feedback
from app.models.interview import Interview

from app.schemas.feedback_schema import FeedbackCreate


def create_feedback(
    request: FeedbackCreate,
    db: Session,
    current_user: dict
):

    # Check interview exists
    interview = db.query(Interview).filter(
        Interview.id == request.interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    # Interview must be completed
    if interview.status != "Completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback can only be submitted after interview is completed."
        )

    # Only assigned interviewer or Admin
    if (
        current_user["role"] != "Admin"
        and interview.interviewer_id != current_user["id"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to submit feedback."
        )

    # One feedback per interview
    existing = db.query(Feedback).filter(
        Feedback.interview_id == request.interview_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback already submitted."
        )

    feedback = Feedback(
        interview_id=request.interview_id,
        technical_rating=request.technical_rating,
        communication_rating=request.communication_rating,
        remarks=request.remarks
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


def get_feedback(
    interview_id: int,
    db: Session,
    current_user: dict
):

    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found."
        )

    # Interviewer can only view their own interview feedback
    if (
        current_user["role"] == "Interviewer"
        and interview.interviewer_id != current_user["id"]
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized."
        )

    feedback = db.query(Feedback).filter(
        Feedback.interview_id == interview_id
    ).first()

    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found."
        )

    return feedback