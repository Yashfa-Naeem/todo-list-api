from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import TaskCreate, TaskUpdate, TaskResponse
from ..auth.utils import get_current_user
from ..database.schema import User
from . import services
from typing import List
from fastapi.responses import FileResponse
from fastapi import File, UploadFile
from ..models.models import AttachmentResponse


router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.create_task(db, task, current_user.id)

@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_all_tasks(db, current_user.id)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_task_by_id(db, task_id, current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.update_task(db, task_id, task_update, current_user.id)

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.delete_task(db, task_id, current_user.id)



@router.post("/{task_id}/attachments", response_model=AttachmentResponse, status_code=201)
def attach_file(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.attach_file(db, task_id, current_user.id, file)

@router.get("/{task_id}/attachments", response_model=List[AttachmentResponse])
def get_attachments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_attachments(db, task_id, current_user.id)

@router.get("/{task_id}/attachments/{attachment_id}/download")
def download_file(
    task_id: int,
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attachment = services.download_file(db, task_id, attachment_id, current_user.id)
    
    # Create user-specific filename
    original_name = attachment.file_name
    name_parts = original_name.rsplit('.', 1)  # Split name and extension
    
    if len(name_parts) == 2:
        name, extension = name_parts
        new_filename = f"user_{current_user.id}_{name}.{extension}"
    else:
        new_filename = f"user_{current_user.id}_{original_name}"
    
    return FileResponse(
        path=attachment.file_path,
        filename=new_filename,  
        media_type="application/octet-stream"
    )

@router.get("/{task_id}/similar", response_model=List[TaskResponse])
def get_similar_tasks(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return services.get_similar_tasks(db, task_id, current_user.id)