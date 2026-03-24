from src.tasks.dtos import TaskSchema, MultipleCond
from sqlalchemy.orm import Session 
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.user.models import UserModel 


def create_task(body: TaskSchema, db: Session, user: UserModel):
    if db is None:
        raise HTTPException(500, detail="Database session is None in create_task")
    data = body.model_dump()
    new_task = TaskModel(**data, user_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    

def get_tasks(db: Session, user: UserModel):
    if db is None:
        raise HTTPException(500, detail="Database session is None in get_tasks")
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()
    return tasks


def getTaskById(id: int, db: Session):
    if db is None:
        raise HTTPException(500, detail="Database session is None in getTaskById")
    task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not task:
        raise HTTPException(404, detail=f"Task id is Incorrect {id}")
    return {
        "status": "Fetch By Id",
        "data": task
    }


def getByMulCond(body: MultipleCond, db: Session):
    if db is None:
        raise HTTPException(500, detail="Database session is None in getByMulCond")
    data = body.model_dump()
    tasks = db.query(TaskModel).filter(
        TaskModel.title == data["title"],
        TaskModel.is_completed == data["is_completed"]
    ).all()
     
    if not tasks:
        return {"status": "Not Found"}
    return {
        "status": "Fetched By MultipleCondition",
        "data": tasks
    }


def update_tasks(body: TaskSchema, task_id: int, db: Session, user: UserModel):
    if db is None:
        raise HTTPException(500, detail="Database session is None in update_tasks")
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail=f"Task cannot find for particular id {task_id}")
    
    if one_task.user_id != user.id:
        raise HTTPException(401, detail="You do not have access to edit it")

    body_data = body.model_dump()
    for field, value in body_data.items():
        setattr(one_task, field, value)
    
    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    
    return {
        "Status": "Task Updated Successfully",
        "data": one_task
    }


def delete_task(task_id: int, db: Session, user: UserModel):
    if db is None:
        raise HTTPException(500, detail="Database session is None in delete_task")
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail=f"Id:{task_id} not found")
    
    if one_task.user_id != user.id:
        raise HTTPException(401, detail="You do not have access to delete this task")
    
    db.delete(one_task)
    db.commit()
    return None
