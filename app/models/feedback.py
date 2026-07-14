from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        unique=True
    )

    technical_rating = Column(
        Integer,
        nullable=False
    )

    communication_rating = Column(
        Integer,
        nullable=False
    )

    remarks = Column(
        Text,
        nullable=True
    )

    interview = relationship(
        "Interview",
        back_populates="feedback"
    )