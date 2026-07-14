from datetime import date
from datetime import time

from pydantic import BaseModel
from pydantic import ConfigDict


class InterviewCreate(BaseModel):
    candidate_id: int
    interviewer_id: int
    interview_date: date
    interview_time: time
    interview_mode: str


class InterviewUpdate(BaseModel):
    interview_date: date | None = None
    interview_time: time | None = None
    interview_mode: str | None = None
    status: str | None = None


class InterviewResponse(BaseModel):
    id: int
    candidate_id: int
    interviewer_id: int
    interview_date: date
    interview_time: time
    interview_mode: str
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )