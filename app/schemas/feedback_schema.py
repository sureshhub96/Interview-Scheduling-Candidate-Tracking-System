from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class FeedbackCreate(BaseModel):
    interview_id: int
    technical_rating: int = Field(..., ge=1, le=5)
    communication_rating: int = Field(..., ge=1, le=5)
    remarks: str | None = None


class FeedbackResponse(BaseModel):
    id: int
    interview_id: int
    technical_rating: int
    communication_rating: int
    remarks: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )