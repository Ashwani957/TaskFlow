# TaskFlow - FastAPI Task Management Applications

A modern Task Management System built with **FastAPI**, **Jinja2 Templates**, and **PostgreSQL**.

## 🌟 Key Features
- **Integrated Frontend**: Complete UI for login, registration, and task CRUD.
- **Task Priority**: High, Medium, and Low priorities with status badges.
- **Due Dates**: Set deadlines and automatically see overdue tasks in red.
- **Smart Sorting**: Sort tasks by Newest First, Priority, or Due Date.
- **Authentication**: Modern authentication with JWT and secure browser cookies.

---

## 🚀 Getting Started

### 1. Environment Setup
Activate your Python virtual environment:

**PowerShell (Windows):**
```powershell
.\env\Scripts\Activate.ps1
```

**Git Bash / Linux / macOS:**
```bash
source env/Scripts/activate
```

### 2. Install Dependencies
```bash
pip install -r requirement.txt
```

### 3. Database Migration
Run the following script to add the new priority and due date columns to your database:
```bash
python migrate_add_columns.py
```

### 4. Run the Project
Start the combined frontend and backend server:
```bash
python main.py
```
*Or use uvicorn directly (with auto-reload enabled):*
```bash
env/Scripts/python.exe -m uvicorn main:app --reload
```

Then visit: 
**1. http://127.0.0.1:8000](http://127.0.0.1:8000)** 🌐
**2. https://taskflow-1-ox2g.onrender.com/tasks**

---

## 🏗️ Project Structure
- `main.py`: Application entry point and router integration.
- `src/frontend/`: Jinja2 frontend routes.
- `src/tasks/`: Task models, controllers, and schemas.
- `src/user/`: User authentication and registration.
- `templates/`: HTML templates.
- `static/`: CSS and frontend assets.
