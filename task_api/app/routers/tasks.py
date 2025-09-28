from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED,
             summary="Create a new task",
             description="Creates a new task with a title, an optional description, and a default status of 'pending'.")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)): # <--- ИСПРАВЛЕНО ЗДЕСЬ
    return crud.create_task(db=db, task=task)


@router.get("/", response_model=List[schemas.Task],
            summary="Get a list of tasks",
            description="Returns a list of all tasks. Can be filtered by status.")
def read_tasks(
    status: Optional[schemas.TaskStatus] = Query(None, description="Filter tasks by status"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    tasks = crud.get_tasks(db, status=status, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=schemas.Task,
            summary="Get a single task by ID",
            description="Returns a specific task based on its unique ID.")
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=schemas.Task,
            summary="Update a task",
            description="Updates a task's title, description, or status by its ID.")
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", response_model=schemas.Task,
               summary="Delete a task",
               description="Deletes a task by its ID and returns the deleted task's data.")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
