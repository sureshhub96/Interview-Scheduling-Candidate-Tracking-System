from sqlalchemy.orm import Session
from sqlalchemy import and_

from fastapi import HTTPException, status

from app.models.interview import Interview
from app.models.candidate import Candidate
from app.models.user import User

from app.schemas.interview_schema import (
    InterviewCreate,
    InterviewUpdate
)


VALID_MODES = [
    "Online",
    "Offline"
]

VALID_STATUS = [
    "Scheduled",
    "Completed",
    "Cancelled",
    "Selected",
    "Rejected"
]


def create_interview(
    request: InterviewCreate,
    db: Session
):

    # Candidate exists?
    candidate = db.query(Candidate).filter(
        Candidate.id == request.candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    # Interviewer exists?
    interviewer = db.query(User).filter(
        User.id == request.interviewer_id
    ).first()

    if not interviewer:
        raise HTTPException(
            status_code=404,
            detail="Interviewer not found."
        )

    if interviewer.role != "Interviewer":
        raise HTTPException(
            status_code=400,
            detail="Assigned user is not an interviewer."
        )

    # Interview mode validation
    if request.interview_mode not in VALID_MODES:
        raise HTTPException(
            status_code=400,
            detail="Interview mode must be Online or Offline."
        )

    # Duplicate schedule check
    duplicate = db.query(Interview).filter(
        and_(
            Interview.candidate_id == request.candidate_id,
            Interview.interview_date == request.interview_date,
            Interview.interview_time == request.interview_time
        )
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Candidate already has an interview scheduled at this date and time."
        )

    interview = Interview(
        candidate_id=request.candidate_id,
        interviewer_id=request.interviewer_id,
        interview_date=request.interview_date,
        interview_time=request.interview_time,
        interview_mode=request.interview_mode,
        status="Scheduled"
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return interview


def get_interviews(
    db: Session,
    current_user: dict
):

    if current_user["role"] == "Interviewer":

        return db.query(Interview).filter(
            Interview.interviewer_id == current_user["id"]
        ).all()

    return db.query(Interview).all()


def get_interview(
    interview_id: int,
    db: Session,
    current_user: dict
):

    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    # Interviewer can view only assigned interview
    if (
        current_user["role"] == "Interviewer"
        and
        interview.interviewer_id != current_user["id"]
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized."
        )

    return interview


def update_interview(
    interview_id: int,
    request: InterviewUpdate,
    db: Session
):

    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    if request.status:

        if request.status not in VALID_STATUS:
            raise HTTPException(
                status_code=400,
                detail="Invalid interview status."
            )

    if request.interview_mode:

        if request.interview_mode not in VALID_MODES:
            raise HTTPException(
                status_code=400,
                detail="Invalid interview mode."
            )

    # Duplicate schedule check if date/time updated
    new_date = request.interview_date or interview.interview_date
    new_time = request.interview_time or interview.interview_time

    duplicate = db.query(Interview).filter(
        Interview.id != interview_id,
        Interview.candidate_id == interview.candidate_id,
        Interview.interview_date == new_date,
        Interview.interview_time == new_time
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Duplicate interview schedule."
        )

    update_data = request.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(interview, key, value)

    db.commit()
    db.refresh(interview)

    return interview


def filter_interviews(
    db: Session,
    status: str = None,
    interviewer_id: int = None,
    page: int = 1,
    limit: int = 10
):

    query = db.query(Interview)

    if status:
        query = query.filter(
            Interview.status == status
        )

    if interviewer_id:
        query = query.filter(
            Interview.interviewer_id == interviewer_id
        )

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()