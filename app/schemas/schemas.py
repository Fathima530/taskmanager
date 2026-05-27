from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


# ─── AUTH SCHEMAS ─────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    @validator("password")
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @validator("full_name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Full name cannot be empty")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ─── TASK SCHEMAS ─────────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "MEDIUM"   # LOW, MEDIUM, HIGH
    status: Optional[str] = "pending"    # pending, in_progress, completed

    @validator("priority")
    def validate_priority(cls, v):
        allowed = ["LOW", "MEDIUM", "HIGH"]
        if v.upper() not in allowed:
            raise ValueError(f"Priority must be one of {allowed}")
        return v.upper()

    @validator("status")
    def validate_status(cls, v):
        allowed = ["pending", "in_progress", "completed"]
        if v.lower() not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v.lower()

    @validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

    @validator("priority", pre=True, always=True)
    def validate_priority(cls, v):
        if v is None:
            return v
        allowed = ["LOW", "MEDIUM", "HIGH"]
        if v.upper() not in allowed:
            raise ValueError(f"Priority must be one of {allowed}")
        return v.upper()

    @validator("status", pre=True, always=True)
    def validate_status(cls, v):
        if v is None:
            return v
        allowed = ["pending", "in_progress", "completed"]
        if v.lower() not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v.lower()


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    status: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    total: int
    tasks: list[TaskResponse]
