from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """
    Schema پایه برای Todo
    """
    title: str = Field(..., min_length=1, max_length=200, description="عنوان وظیفه")
    description: Optional[str] = Field(None, max_length=1000, description="توضیحات وظیفه")
    completed: Optional[bool] = Field(False, description="وضعیت انجام وظیفه")


class TodoCreate(TodoBase):
    """
    Schema برای ایجاد Todo جدید
    """
    pass


class TodoUpdate(BaseModel):
    """
    Schema برای به‌روزرسانی Todo (همه فیلدها اختیاری)
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    """
    Schema برای پاسخ API (شامل id و timestamps)
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # برای SQLAlchemy models (قبلاً orm_mode)


class TodoListResponse(BaseModel):
    """
    Schema برای پاسخ لیست Todos با pagination
    """
    items: list[TodoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

