from fastapi import FastAPI

from app.database import Base, engine

# Import all models before create_all()
from app.models.user import User
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.feedback import Feedback

# Import routers
from app.routes.auth import router as auth_router
from app.routes.candidate import router as candidate_router
from app.routes.interview import router as interview_router
from app.routes.feedback import router as feedback_router
from app.routes.reports import router as report_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Interview Scheduling & Candidate Tracking System",
    description="""
A FastAPI application for managing the complete interview lifecycle.

### Features
- JWT Authentication
- Role-Based Authorization (Admin, HR, Interviewer)
- Candidate Management
- Interview Scheduling
- Feedback Management
- Reports & Search
- Pagination
""",
    version="1.0.0"
)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Interview Scheduling & Candidate Tracking System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Authentication
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# Candidate Management
app.include_router(
    candidate_router,
    prefix="/candidates",
    tags=["Candidates"]
)

# Interview Management
app.include_router(
    interview_router,
    prefix="/interviews",
    tags=["Interviews"]
)

# Feedback Management
app.include_router(
    feedback_router,
    prefix="/feedback",
    tags=["Feedback"]
)

# Reports
app.include_router(
    report_router,
    prefix="/reports",
    tags=["Reports"]
)