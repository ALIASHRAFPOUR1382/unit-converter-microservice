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
    ایجاد یک Todo جدید
    
    - **title**: عنوان وظیفه (اجباری)
    - **description**: توضیحات وظیفه (اختیاری)
    - **completed**: وضعیت انجام (پیش‌فرض: false)
    """
    return crud.create_todo(db=db, todo=todo)


@router.get("", response_model=schemas.TodoListResponse)
def get_todos(
    page: int = Query(1, ge=1, description="شماره صفحه"),
    page_size: int = Query(10, ge=1, le=100, description="تعداد آیتم در هر صفحه"),
    completed: Optional[bool] = Query(None, description="فیلتر بر اساس وضعیت انجام"),
    db: Session = Depends(get_db)
):
    """
    دریافت لیست Todos با pagination و filtering
    
    - **page**: شماره صفحه (شروع از 1)
    - **page_size**: تعداد آیتم در هر صفحه (حداکثر 100)
    - **completed**: فیلتر بر اساس وضعیت (true/false/null برای همه)
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
    دریافت یک Todo بر اساس ID
    """
    db_todo = crud.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo پیدا نشد")
    return db_todo


@router.put("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo_full(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """
    به‌روزرسانی کامل یک Todo (PUT)
    """
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo پیدا نشد")
    return db_todo


@router.patch("/{todo_id}", response_model=schemas.TodoResponse)
def update_todo_partial(
    todo_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(get_db)
):
    """
    به‌روزرسانی جزئی یک Todo (PATCH)
    می‌توانید فقط فیلدهای مورد نظر را ارسال کنید
    """
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo_update=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo پیدا نشد")
    return db_todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    """
    حذف یک Todo
    """
    success = crud.delete_todo(db=db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo پیدا نشد")
    return None

