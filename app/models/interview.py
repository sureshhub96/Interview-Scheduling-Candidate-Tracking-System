from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import Time

from sqlalchemy.orm import relationship

from app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id")
    )

    interviewer_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    interview_date = Column(
        Date,
        nullable=False
    )

    interview_time = Column(
        Time,
        nullable=False
    )

    interview_mode = Column(
        String(30),
        nullable=False
    )

    status = Column(
        String(30),
        default="Scheduled"
    )

    candidate = relationship(
        "Candidate",
        back_populates="interviews"
    )

    interviewer = relationship(
        "User"
    )

    feedback = relationship(
        "Feedback",
        back_populates="interview",
        uselist=False,
        cascade="all, delete"
    )