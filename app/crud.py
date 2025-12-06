from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app import models, schemas


def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
    """
    ایجاد یک Todo جدید
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
    دریافت یک Todo بر اساس ID
    """
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None
) -> tuple[List[models.Todo], int]:
    """
    دریافت لیست Todos با pagination و filtering
    
    Returns:
        tuple: (list of todos, total count)
    """
    query = db.query(models.Todo)
    
    # Filter بر اساس completed status
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)
    
    # دریافت تعداد کل
    total = query.count()
    
    # Sorting بر اساس created_at (جدیدترین اول)
    # Pagination
    todos = query.order_by(desc(models.Todo.created_at)).offset(skip).limit(limit).all()
    
    return todos, total


def update_todo(
    db: Session,
    todo_id: int,
    todo_update: schemas.TodoUpdate
) -> Optional[models.Todo]:
    """
    به‌روزرسانی یک Todo
    """
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    # به‌روزرسانی فیلدهایی که ارسال شده‌اند
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """
    حذف یک Todo
    Returns:
        bool: True اگر حذف شد، False اگر Todo پیدا نشد
    """
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return False
    
    db.delete(db_todo)
    db.commit()
    return True

