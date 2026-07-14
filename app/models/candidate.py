from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from sqlalchemy.orm import relationship

from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )

    experience = Column(
        Float,
        nullable=False
    )

    skill_set = Column(
        String(255),
        nullable=False
    )

    application_status = Column(
        String(50),
        default="Applied"
    )

    interviews = relationship(
        "Interview",
        back_populates="candidate",
        cascade="all, delete"
    )