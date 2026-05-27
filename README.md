# Task Manager API

A REST API backend built with **FastAPI** and **PostgreSQL** for managing tasks with JWT authentication.

---

## Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic Validation
- JWT Authentication (python-jose)
- Password Hashing (passlib/bcrypt)

---

## Project Structure

```
taskmanager/
├── app/
│   ├── config/         → App settings (.env reader)
│   ├── database/       → PostgreSQL connection
│   ├── models/         → SQLAlchemy database models
│   ├── schemas/        → Pydantic validation schemas
│   ├── routes/         → API endpoints
│   ├── services/       → Business logic
│   ├── utils/          → JWT and password helpers
│   └── middleware/     → Auth token verification
├── main.py             → App entry point
├── .env                → Environment variables
├── requirements.txt    → Python dependencies
└── README.md
```

---

## PostgreSQL Setup

1. Install PostgreSQL 16 from https://www.enterprisedb.com
2. Open pgAdmin or psql and run:

```sql
CREATE DATABASE taskmanager;
```

3. Update `.env` file with your PostgreSQL password:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/taskmanager
```

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/taskmanager.git
cd taskmanager

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file and add your config
# (see .env.example)

# 5. Run the server
uvicorn main:app --reload
```

---

## API Documentation

After running the server, open:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login and get JWT token |

### Tasks (Requires JWT Token)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/tasks/ | Create new task |
| GET | /api/tasks/ | Get all tasks |
| GET | /api/tasks/{id} | Get task by ID |
| PUT | /api/tasks/{id} | Update task |
| DELETE | /api/tasks/{id} | Delete task |

---

## Sample API Requests

### Register
```json
POST /api/auth/register
{
    "full_name": "John Doe",
    "email": "john@gmail.com",
    "password": "password123"
}
```

### Login
```json
POST /api/auth/login
{
    "email": "john@gmail.com",
    "password": "password123"
}
```

### Create Task
```json
POST /api/tasks/
Headers: Authorization: Bearer <your_token>
{
    "title": "Complete the project",
    "description": "Finish the FastAPI assessment",
    "priority": "HIGH",
    "status": "pending"
}
```

### Filter Tasks
```
GET /api/tasks/?status=pending&priority=HIGH&page=1&limit=10
```

### Search Tasks
```
GET /api/tasks/?search=project
```

---

## Author
Your Name — youremail@gmail.com
