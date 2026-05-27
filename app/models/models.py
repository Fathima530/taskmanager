from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    full_name  = Column(String(100), nullable=False)
    email      = Column(String(100), unique=True, nullable=False, index=True)
    password   = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One user can have many tasks
    tasks = relationship("Task", back_populates="owner", cascade="all, delete")


class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    priority    = Column(String(20), default="MEDIUM")   # LOW, MEDIUM, HIGH
    status      = Column(String(20), default="pending")  # pending, in_progress, completed
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

    # Each task belongs to one user
    owner = relationship("User", back_populates="tasks")
