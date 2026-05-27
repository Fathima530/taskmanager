from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database.database import get_db
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.services.task_service import (
    create_task, get_all_tasks, get_task_by_id, update_task, delete_task
)
from app.middleware.auth_middleware import get_current_user
from app.models.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task. **Requires login.**

    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **priority**: LOW, MEDIUM, HIGH (default: MEDIUM)
    - **status**: pending, in_progress, completed (default: pending)
    """
    return create_task(db, task_data, current_user.id)


@router.get("/", response_model=TaskListResponse)
def get_tasks(
    status: Optional[str] = Query(None, description="Filter by status: pending, in_progress, completed"),
    priority: Optional[str] = Query(None, description="Filter by priority: LOW, MEDIUM, HIGH"),
    search: Optional[str] = Query(None, description="Search tasks by title"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of tasks per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks for logged-in user. **Requires login.**

    Supports filtering by **status**, **priority**, **search**, and **pagination**.
    """
    return get_all_tasks(db, current_user.id, status, priority, search, page, limit)


@router.get("/{task_id}", response_model=TaskResponse)
def get_single_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single task by ID. **Requires login.**

    Only the task owner can view it.
    """
    return get_task_by_id(db, task_id, current_user.id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a task. **Requires login.**

    Only the task owner can update it. All fields are optional.
    """
    return update_task(db, task_id, task_data, current_user.id)


@router.delete("/{task_id}")
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task. **Requires login.**

    Only the task owner can delete it.
    """
    return delete_task(db, task_id, current_user.id)
