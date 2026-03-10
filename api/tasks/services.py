from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..database.schema import Task
from ..models.models import TaskCreate, TaskUpdate
from datetime import datetime

def check_task_limit(db: Session, user_id: int):
    task_count = db.query(Task).filter(Task.user_id == user_id).count()
    if task_count >= 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task limit reached. Maximum 50 tasks allowed per user"
        )

def create_task(db: Session, task: TaskCreate, user_id: int):
    check_task_limit(db, user_id)
    
    new_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        user_id=user_id,
        is_completed=False
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_all_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task_by_id(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

def update_task(db: Session, task_id: int, task_update: TaskUpdate, user_id: int):
    task = get_task_by_id(db, task_id, user_id)
    
    if task_update.title is not None:
        task.title = task_update.title
    
    if task_update.description is not None:
        task.description = task_update.description
    
    if task_update.due_date is not None:
        task.due_date = task_update.due_date
    
    if task_update.is_completed is not None:
        task.is_completed = task_update.is_completed
        if task_update.is_completed:
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None
    
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id, user_id)
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


import os
import shutil
from fastapi import UploadFile
from ..database.schema import TaskAttachment

def attach_file(db: Session, task_id: int, user_id: int, file: UploadFile):
    # First check if task exists and belongs to user
    task = get_task_by_id(db, task_id, user_id)
    
    # Create folder for this user if it doesn't exist
    upload_dir = f"uploads/{user_id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file to uploads folder
    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Save file info to database
    new_attachment = TaskAttachment(
        task_id=task_id,
        user_id=user_id,
        file_name=file.filename,
        file_path=file_path
    )
    
    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)
    return new_attachment

def get_attachments(db: Session, task_id: int, user_id: int):
    # First check if task exists and belongs to user
    get_task_by_id(db, task_id, user_id)
    
    # Get all attachments for this task
    return db.query(TaskAttachment).filter(
        TaskAttachment.task_id == task_id,
        TaskAttachment.user_id == user_id
    ).all()

def download_file(db: Session, task_id: int, attachment_id: int, user_id: int):
    # First check if task exists and belongs to user
    get_task_by_id(db, task_id, user_id)
    
    # Get attachment from database
    attachment = db.query(TaskAttachment).filter(
        TaskAttachment.id == attachment_id,
        TaskAttachment.task_id == task_id,
        TaskAttachment.user_id == user_id
    ).first()
    
    # If attachment not found, raise error
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )
    
    # Check if file exists on server
    if not os.path.exists(attachment.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server"
        )
    
    return attachment

def get_similar_tasks(db: Session, task_id: int, user_id: int):
    # Get the target task
    target_task = get_task_by_id(db, task_id, user_id)
    
    # Get all tasks for this user (except the target task)
    all_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.id != task_id
    ).all()
    
    # Extract words from target task (title + description)
    target_text = f"{target_task.title} {target_task.description or ''}".lower()
    target_words = set(target_text.split())
    
    similar_tasks = []
    
    for task in all_tasks:
        # Extract words from current task
        task_text = f"{task.title} {task.description or ''}".lower()
        task_words = set(task_text.split())
        
        # Check if all words from target exist in current task
        if target_words.issubset(task_words):
            similar_tasks.append(task)
            continue
        
        # Check if all words from current task exist in target
        if task_words.issubset(target_words):
            similar_tasks.append(task)
    
    return similar_tasks