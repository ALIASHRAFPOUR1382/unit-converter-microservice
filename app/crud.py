from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app import models, schemas


def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
    """
    Create a new Todo
    """
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed if todo.completed is not None else False
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    """
    Get a Todo by ID
    """
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None
) -> tuple[List[models.Todo], int]:
    """
    Get list of Todos with pagination and filtering
    
    Returns:
        tuple: (list of todos, total count)
    """
    query = db.query(models.Todo)
    
    # Filter by completed status
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)
    
    # Get total count
    total = query.count()
    
    # Sort by created_at (newest first)
    # Pagination
    todos = query.order_by(desc(models.Todo.created_at)).offset(skip).limit(limit).all()
    
    return todos, total


def update_todo(
    db: Session,
    todo_id: int,
    todo_update: schemas.TodoUpdate
) -> Optional[models.Todo]:
    """
    Update a Todo
    """
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    # Update fields that were sent
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """
    Delete a Todo
    Returns:
        bool: True if deleted, False if Todo not found
    """
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return False
    
    db.delete(db_todo)
    db.commit()
    return True

