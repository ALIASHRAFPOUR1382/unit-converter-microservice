from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class Todo(Base):
    """
    Todo model for storing tasks
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"


class ConversionHistory(Base):
    """
    Conversion history model for storing unit conversions
    """
    __tablename__ = "conversion_history"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    from_unit = Column(String, nullable=False)
    to_unit = Column(String, nullable=False)
    result = Column(Float, nullable=False)
    unit_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<ConversionHistory(id={self.id}, {self.value} {self.from_unit} -> {self.result} {self.to_unit})>"

