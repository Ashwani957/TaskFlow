from fastapi import APIRouter, Request, Depends, Form, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.tasks import controller as task_controller
from src.user import controller as user_controller
from src.user.dtos import LoginSchema, UserSchema
from src.utils.helpers import is_authenticated
from src.user.models import UserModel
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_current_user_safe(request: Request, db: Session = Depends(get_db)):
    try:
        if db is None:
            return None
        return is_authenticated(request, db)
    except:
        return None

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, user: UserModel = Depends(get_current_user_safe)):
    if user:
        return RedirectResponse(url="/tasks")
    return templates.TemplateResponse(request=request, name="login.html", context={"user": user})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user: UserModel = Depends(get_current_user_safe)):
    if user:
        return RedirectResponse(url="/tasks")
    return templates.TemplateResponse(request=request, name="login.html", context={"user": user})

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        login_data = LoginSchema(username=username, password=password)
        result = user_controller.login_user(login_data, db)
        token = result["token"]
        
        # Redirect to tasks and set cookie
        redirect = RedirectResponse(url="/tasks", status_code=status.HTTP_303_SEE_OTHER)
        redirect.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
        return redirect
    except Exception as e:
        return templates.TemplateResponse(request=request, name="login.html", context={
            "error": str(e.detail) if hasattr(e, "detail") else "Invalid credentials",
            "user": None
        })

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, user: UserModel = Depends(get_current_user_safe)):
    if user:
        return RedirectResponse(url="/tasks")
    return templates.TemplateResponse(request=request, name="register.html", context={"user": user})

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form("User"), # Default name if not provided in form
    db: Session = Depends(get_db)
):
    try:
        user_data = UserSchema(username=username, email=email, password=password, name=name)
        user_controller.register(user_data, db)
        return RedirectResponse(url="/login?msg=Registered successfully", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        return templates.TemplateResponse(request=request, name="register.html", context={
            "error": str(e.detail) if hasattr(e, "detail") else "Registration failed",
            "user": None
        })

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response

@router.get("/tasks", response_class=HTMLResponse)
async def list_tasks(
    request: Request, 
    sort: str = "created_at",
    db: Session = Depends(get_db), 
    user: UserModel = Depends(is_authenticated)
):
    if db is None:
        raise HTTPException(500, detail="Database session is None in list_tasks")
    tasks_query = db.query(task_controller.TaskModel).filter(task_controller.TaskModel.user_id == user.id)
    
    if sort == "priority_desc":
        # Custom sort logic: high -> medium -> low
        from sqlalchemy import case
        tasks_query = tasks_query.order_by(
            case(
                (task_controller.TaskModel.priority == "high", 1),
                (task_controller.TaskModel.priority == "medium", 2),
                (task_controller.TaskModel.priority == "low", 3),
                else_=4
            )
        )
    elif sort == "due_date":
        tasks_query = tasks_query.order_by(task_controller.TaskModel.due_date.asc().nullslast())
    else: # Default: newest first
        tasks_query = tasks_query.order_by(task_controller.TaskModel.created_at.desc())
        
    tasks = tasks_query.all()
    from datetime import datetime
    return templates.TemplateResponse(request=request, name="index.html", context={
        "tasks": tasks, 
        "user": user, 
        "sort": sort,
        "today": datetime.now().date()
    })

@router.get("/tasks/create", response_class=HTMLResponse)
async def create_task_page(request: Request, user: UserModel = Depends(is_authenticated)):
    return templates.TemplateResponse(request=request, name="task_form.html", context={"user": user, "task": None})

@router.post("/tasks/create")
async def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    priority: str = Form("medium"),
    due_date: str = Form(None),
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
    from src.tasks.dtos import TaskSchema
    from datetime import datetime
    dt = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
    task_data = TaskSchema(title=title, description=description, priority=priority, due_date=dt)
    task_controller.create_task(task_data, db, user)
    return RedirectResponse(url="/tasks", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/tasks/edit/{task_id}", response_class=HTMLResponse)
async def edit_task_page(task_id: int, request: Request, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    result = task_controller.getTaskById(task_id, db)
    task = result["data"] if isinstance(result, dict) and "data" in result else result
    return templates.TemplateResponse(request=request, name="task_form.html", context={"user": user, "task": task})

@router.post("/tasks/edit/{task_id}")
async def edit_task(
    task_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    is_completed: str = Form(None),
    priority: str = Form("medium"),
    due_date: str = Form(None),
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated)
):
    from src.tasks.dtos import TaskSchema
    from datetime import datetime
    completed = is_completed is not None and is_completed == "on"
    dt = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
    task_data = TaskSchema(title=title, description=description, is_completed=completed, priority=priority, due_date=dt)
    task_controller.update_tasks(task_data, task_id, db, user)
    return RedirectResponse(url="/tasks", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/tasks/delete/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    task_controller.delete_task(task_id, db, user)
    return RedirectResponse(url="/tasks", status_code=status.HTTP_303_SEE_OTHER)
