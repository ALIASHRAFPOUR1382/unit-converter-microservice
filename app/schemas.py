from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """
    Base schema for Todo
    """
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: Optional[bool] = Field(False, description="Task completion status")


class TodoCreate(TodoBase):
    """
    Schema for creating a new Todo
    """
    pass


class TodoUpdate(BaseModel):
    """
    Schema for updating Todo (all fields optional)
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    """
    Schema for API response (includes id and timestamps)
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For SQLAlchemy models (formerly orm_mode)


class TodoListResponse(BaseModel):
    """
    Schema for Todo list response with pagination
    """
    items: list[TodoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ConversionHistoryCreate(BaseModel):
    """
    Schema for creating conversion history
    """
    value: float
    from_unit: str
    to_unit: str
    result: float
    unit_type: str


class ConversionHistoryResponse(BaseModel):
    """
    Schema for conversion history response
    """
    id: int
    value: float
    from_unit: str
    to_unit: str
    result: float
    unit_type: str
    created_at: datetime

    class Config:
        from_attributes = True

