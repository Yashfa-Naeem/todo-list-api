from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from ..database.schema import Task, User
from datetime import datetime, timezone

def get_task_counts(db: Session, user_id: int):
    total = db.query(Task).filter(Task.user_id == user_id).count()
    completed = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_completed == True
    ).count()
    remaining = total - completed
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "remaining_tasks": remaining
    }

def get_average_completed_per_day(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    
    completed_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_completed == True
    ).count()
    
    days_since_creation = (datetime.now(timezone.utc) - user.created_at).days
    
    if days_since_creation == 0:
        days_since_creation = 1
    
    average = round(completed_tasks / days_since_creation, 2)
    
    return {
        "average_tasks_completed_per_day": average,
        "days_since_account_creation": days_since_creation,
        "total_completed_tasks": completed_tasks
    }

def get_overdue_tasks(db: Session, user_id: int):
    now = datetime.now(timezone.utc)
    
    overdue_count = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_completed == False,
        Task.due_date < now
    ).count()
    
    return {
        "overdue_tasks_count": overdue_count
    }

def get_max_completed_day(db: Session, user_id: int):
    result = db.query(
        cast(Task.completed_at, Date).label("completion_date"),
        func.count(Task.id).label("count")
    ).filter(
        Task.user_id == user_id,
        Task.is_completed == True,
        Task.completed_at != None
    ).group_by(
        cast(Task.completed_at, Date)
    ).order_by(
        func.count(Task.id).desc()
    ).first()
    
    if not result:
        return {
            "date": None,
            "tasks_completed": 0
        }
    
    return {
        "date": str(result.completion_date),
        "tasks_completed": result.count
    }

def get_tasks_per_weekday(db: Session, user_id: int):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    
    weekdays = {
        "monday": 0,
        "tuesday": 0,
        "wednesday": 0,
        "thursday": 0,
        "friday": 0,
        "saturday": 0,
        "sunday": 0
    }
    
    for task in tasks:
        day = task.created_at.strftime("%A").lower()
        weekdays[day] += 1
    
    return weekdays