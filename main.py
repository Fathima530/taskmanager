from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routes import auth, tasks

# Create all database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="""
## Task Management System

A REST API for managing tasks with user authentication.

### Features
- ✅ User Registration & Login
- ✅ JWT Authentication
- ✅ Create, Read, Update, Delete Tasks
- ✅ Filter Tasks by Status & Priority
- ✅ Search Tasks by Title
- ✅ Pagination Support

### How to use
1. Register a new account using **POST /api/auth/register**
2. Login using **POST /api/auth/login** to get your token
3. Click **Authorize** button above and enter: `Bearer <your_token>`
4. Now you can access all task endpoints!
    """,
    version="1.0.0",
)

# Allow frontend apps to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "Task Manager API is running!",
        "docs": "http://127.0.0.1:8000/docs",
        "version": "1.0.0"
    }
