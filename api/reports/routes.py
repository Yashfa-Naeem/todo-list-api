from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..auth.utils import get_current_user
from ..database.schema import User
from . import services

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/task-counts")
def get_task_counts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_task_counts(db, current_user.id)

@router.get("/average-completed-per-day")
def get_average_completed_per_day(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_average_completed_per_day(db, current_user.id)

@router.get("/overdue-tasks")
def get_overdue_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_overdue_tasks(db, current_user.id)

@router.get("/max-completed-day")
def get_max_completed_day(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_max_completed_day(db, current_user.id)

@router.get("/tasks-per-weekday")
def get_tasks_per_weekday(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_tasks_per_weekday(db, current_user.id)