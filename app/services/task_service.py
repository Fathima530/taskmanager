from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.models import Task
from app.schemas.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate, user_id: int) -> Task:
    """Create a new task for the logged-in user."""
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=task_data.status,
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_all_tasks(
    db: Session,
    user_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    """Get all tasks for a user with optional filters and pagination."""
    query = db.query(Task).filter(Task.user_id == user_id)

    # Filter by status if provided
    if status:
        query = query.filter(Task.status == status.lower())

    # Filter by priority if provided
    if priority:
        query = query.filter(Task.priority == priority.upper())

    # Search by title if provided
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    total = query.count()

    # Pagination
    offset = (page - 1) * limit
    tasks = query.offset(offset).limit(limit).all()

    return {"total": total, "tasks": tasks}


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task:
    """Get a single task by ID. Only owner can access it."""
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: int) -> Task:
    """Update an existing task. Only owner can update."""
    task = get_task_by_id(db, task_id, user_id)

    # Only update fields that were provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.status is not None:
        task.status = task_data.status

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int) -> dict:
    """Delete a task. Only owner can delete."""
    task = get_task_by_id(db, task_id, user_id)
    db.delete(task)
    db.commit()
    return {"message": f"Task '{task.title}' deleted successfully"}
