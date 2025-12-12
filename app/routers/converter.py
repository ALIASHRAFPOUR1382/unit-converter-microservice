from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Literal, List
from enum import Enum
from app.database import get_db
from app import crud, schemas
from math import ceil

router = APIRouter(prefix="/converter", tags=["converter"])


# Unit types
class LengthUnit(str, Enum):
    METER = "meter"
    KILOMETER = "kilometer"
    CENTIMETER = "centimeter"
    MILLIMETER = "millimeter"
    MILE = "mile"
    FOOT = "foot"
    INCH = "inch"
    YARD = "yard"


class WeightUnit(str, Enum):
    KILOGRAM = "kilogram"
    GRAM = "gram"
    POUND = "pound"
    OUNCE = "ounce"
    TON = "ton"


class TemperatureUnit(str, Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"


# Request/Response models
class ConvertRequest(BaseModel):
    value: float = Field(..., description="Value to convert")
    from_unit: str = Field(..., description="Source unit")
    to_unit: str = Field(..., description="Target unit")
    unit_type: Literal["length", "weight", "temperature"] = Field(..., description="Type of unit conversion")


class ConvertResponse(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    result: float
    unit_type: str


# Conversion functions
def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert length units"""
    # Convert to meters first
    to_meter = {
        "meter": 1.0,
        "kilometer": 1000.0,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "mile": 1609.34,
        "foot": 0.3048,
        "inch": 0.0254,
        "yard": 0.9144
    }
    
    # Convert from source unit to meters
    value_in_meters = value * to_meter.get(from_unit.lower(), 1.0)
    
    # Convert from meters to target unit
    from_meter = {
        "meter": 1.0,
        "kilometer": 0.001,
        "centimeter": 100.0,
        "millimeter": 1000.0,
        "mile": 0.000621371,
        "foot": 3.28084,
        "inch": 39.3701,
        "yard": 1.09361
    }
    
    return value_in_meters * from_meter.get(to_unit.lower(), 1.0)


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Convert weight units"""
    # Convert to kilograms first
    to_kilogram = {
        "kilogram": 1.0,
        "gram": 0.001,
        "pound": 0.453592,
        "ounce": 0.0283495,
        "ton": 1000.0
    }
    
    # Convert from source unit to kilograms
    value_in_kg = value * to_kilogram.get(from_unit.lower(), 1.0)
    
    # Convert from kilograms to target unit
    from_kilogram = {
        "kilogram": 1.0,
        "gram": 1000.0,
        "pound": 2.20462,
        "ounce": 35.274,
        "ton": 0.001
    }
    
    return value_in_kg * from_kilogram.get(to_unit.lower(), 1.0)


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature units"""
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    # Convert to Celsius first
    if from_unit_lower == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit_lower == "kelvin":
        celsius = value - 273.15
    else:  # celsius
        celsius = value
    
    # Convert from Celsius to target unit
    if to_unit_lower == "fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit_lower == "kelvin":
        return celsius + 273.15
    else:  # celsius
        return celsius


@router.post("/convert", response_model=ConvertResponse)
def convert_units(request: ConvertRequest):
    """
    Convert units between different measurement systems
    
    Supported unit types:
    - **length**: meter, kilometer, centimeter, millimeter, mile, foot, inch, yard
    - **weight**: kilogram, gram, pound, ounce, ton
    - **temperature**: celsius, fahrenheit, kelvin
    
    Example:
    ```json
    {
        "value": 100,
        "from_unit": "kilometer",
        "to_unit": "mile",
        "unit_type": "length"
    }
    ```
    """
    try:
        if request.unit_type == "length":
            result = convert_length(request.value, request.from_unit, request.to_unit)
        elif request.unit_type == "weight":
            result = convert_weight(request.value, request.from_unit, request.to_unit)
        elif request.unit_type == "temperature":
            result = convert_temperature(request.value, request.from_unit, request.to_unit)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported unit type: {request.unit_type}. Supported types: length, weight, temperature"
            )
        
        return ConvertResponse(
            value=request.value,
            from_unit=request.from_unit,
            to_unit=request.to_unit,
            result=round(result, 6),
            unit_type=request.unit_type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Conversion error: {str(e)}")


@router.get("/units")
def get_available_units():
    """
    Get list of available units for each conversion type
    """
    return {
        "length": [
            "meter", "kilometer", "centimeter", "millimeter",
            "mile", "foot", "inch", "yard"
        ],
        "weight": [
            "kilogram", "gram", "pound", "ounce", "ton"
        ],
        "temperature": [
            "celsius", "fahrenheit", "kelvin"
        ]
    }


@router.post("/history", response_model=schemas.ConversionHistoryResponse, status_code=201)
def save_conversion_history(
    conversion: schemas.ConversionHistoryCreate,
    db: Session = Depends(get_db)
):
    """
    Save a conversion to history
    """
    return crud.create_conversion_history(db=db, conversion=conversion)


@router.get("/history", response_model=List[schemas.ConversionHistoryResponse])
def get_conversion_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    """
    Get conversion history with pagination
    """
    skip = (page - 1) * page_size
    conversions, total = crud.get_conversion_history(db=db, skip=skip, limit=page_size)
    
    return conversions


@router.delete("/history/{history_id}", status_code=204)
def delete_conversion_history_item(
    history_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific conversion history item
    """
    success = crud.delete_conversion_history(db=db, history_id=history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversion history not found")
    return None


@router.delete("/history", status_code=200)
def clear_conversion_history(db: Session = Depends(get_db)):
    """
    Clear all conversion history
    """
    count = crud.clear_conversion_history(db=db)
    return {"message": f"Deleted {count} conversion history records"}


