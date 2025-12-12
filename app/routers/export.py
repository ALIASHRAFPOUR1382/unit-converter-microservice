from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime
import os
from pathlib import Path

router = APIRouter(prefix="/export", tags=["export"])


def create_excel_file(todos: list, conversions: list) -> str:
    """
    Create Excel file with todos and conversion history
    Returns the file path
    """
    wb = Workbook()
    
    # Remove default sheet if it exists
    if len(wb.sheetnames) > 0:
        wb.remove(wb.active)
    
    header_fill = PatternFill(start_color="667eea", end_color="667eea", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    # Create Todos sheet (only if there are todos or if we want to create empty sheet)
    if todos or not conversions:
        todos_sheet = wb.create_sheet("Todos", 0)
        
        # Headers for Todos
        todos_headers = ["ID", "Title", "Description", "Completed", "Created At", "Updated At"]
        todos_sheet.append(todos_headers)
        
        # Style headers
        for cell in todos_sheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Add todos data
        for todo in todos:
            todos_sheet.append([
                todo.id,
                todo.title,
                todo.description or "",
                "Yes" if todo.completed else "No",
                todo.created_at.strftime("%Y-%m-%d %H:%M:%S") if todo.created_at else "",
                todo.updated_at.strftime("%Y-%m-%d %H:%M:%S") if todo.updated_at else ""
            ])
        
        # Auto-adjust column widths for Todos
        for column in todos_sheet.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            todos_sheet.column_dimensions[column_letter].width = adjusted_width
    
    # Create Conversion History sheet (only if there are conversions or if we want to create empty sheet)
    if conversions or not todos:
        conv_sheet = wb.create_sheet("Conversion History", 1 if todos else 0)
        
        # Headers for Conversion History
        conv_headers = ["ID", "Value", "From Unit", "To Unit", "Result", "Unit Type", "Created At"]
        conv_sheet.append(conv_headers)
        
        # Style headers
        for cell in conv_sheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Add conversion data
        for conv in conversions:
            conv_sheet.append([
                conv.id,
                conv.value,
                conv.from_unit,
                conv.to_unit,
                conv.result,
                conv.unit_type,
                conv.created_at.strftime("%Y-%m-%d %H:%M:%S") if conv.created_at else ""
            ])
        
        # Auto-adjust column widths for Conversion History
        for column in conv_sheet.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            conv_sheet.column_dimensions[column_letter].width = adjusted_width
    
    # Save to temporary file
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    exports_dir = BASE_DIR / "exports"
    exports_dir.mkdir(exist_ok=True)
    
    filename = f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = exports_dir / filename
    
    wb.save(filepath)
    
    return str(filepath)


@router.get("/excel")
def export_to_excel(db: Session = Depends(get_db)):
    """
    Export all database data (Todos and Conversion History) to Excel file
    
    Returns an Excel file with two sheets:
    - Todos: All todo items
    - Conversion History: All conversion records
    """
    try:
        # Get all todos
        todos, _ = crud.get_todos(db=db, skip=0, limit=10000)
        
        # Get all conversion history
        conversions, _ = crud.get_conversion_history(db=db, skip=0, limit=10000)
        
        # Create Excel file
        filepath = create_excel_file(todos, conversions)
        
        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating Excel file: {str(e)}")


@router.get("/excel/todos")
def export_todos_to_excel(db: Session = Depends(get_db)):
    """
    Export only Todos to Excel file
    """
    try:
        todos, _ = crud.get_todos(db=db, skip=0, limit=10000)
        filepath = create_excel_file(todos, [])
        
        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating Excel file: {str(e)}")


@router.get("/excel/conversions")
def export_conversions_to_excel(db: Session = Depends(get_db)):
    """
    Export only Conversion History to Excel file
    """
    try:
        conversions, _ = crud.get_conversion_history(db=db, skip=0, limit=10000)
        filepath = create_excel_file([], conversions)
        
        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating Excel file: {str(e)}")
