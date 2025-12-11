from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas
from app.database import get_db
from math import ceil

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=schemas.TodoResponse, status_code=201)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new Todo
    
    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **completed**: Completion status (default: false)
    """
    return crud.create_todo(db=db, todo=todo)


@router.get("", response_model=schemas.TodoListResponse)
def get_todos(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    db: Session = Depends(get_db)
):
    """
    Get list of Todos with pagination and filtering
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of items per page (max 100)
    - **completed**: Filter by status (true/false/null for all)
    """
    skip = (page - 1) * page_size
    todos, total = crud.get_todos(db=db, skip=skip, limit=page_size, completed=completed)
    
    total_pages = ceil(total / page_size) if total > 0 else 0
    
    return schemas.TodoListResponse(
        items=todos,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a Todo by ID
    """
    db_todo = crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo_full(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """
    Full update of a Todo (PUT)
    """
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.patch("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo_partial(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """
    Partial update of a Todo (PATCH)
    You can send only the fields you want to update
    """
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a Todo
    """
    success = crud.delete_todo(db=db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None

