from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator, ValidationError, ValidationInfo
from typing import Literal, List
from enum import Enum
from app.database import get_db
from app import crud, schemas
from math import ceil, isnan, isinf

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


# Valid unit sets
VALID_LENGTH_UNITS = {"meter", "kilometer", "centimeter", "millimeter", "mile", "foot", "inch", "yard"}
VALID_WEIGHT_UNITS = {"kilogram", "gram", "pound", "ounce", "ton"}
VALID_TEMPERATURE_UNITS = {"celsius", "fahrenheit", "kelvin"}

# Request/Response models
class ConvertRequest(BaseModel):
    value: float = Field(..., description="Value to convert")
    from_unit: str = Field(..., description="Source unit")
    to_unit: str = Field(..., description="Target unit")
    unit_type: Literal["length", "weight", "temperature"] = Field(..., description="Type of unit conversion")
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, v: float) -> float:
        """Validate that value is a valid number"""
        if isnan(v):
            raise ValueError("Value cannot be NaN (Not a Number)")
        if isinf(v):
            raise ValueError("Value cannot be Infinity")
        # Check for extremely large values that might cause overflow
        if abs(v) > 1e15:
            raise ValueError(f"Value {v} is too large. Maximum allowed value is 1e15")
        return v
    
    @field_validator('from_unit', 'to_unit')
    @classmethod
    def validate_unit(cls, v: str, info: ValidationInfo) -> str:
        """Validate unit based on unit_type"""
        if not v or not isinstance(v, str):
            raise ValueError("Unit must be a non-empty string")
        return v.strip().lower()
    
    def model_post_init(self, __context):
        """Validate units match the unit_type"""
        from_unit_lower = self.from_unit.lower()
        to_unit_lower = self.to_unit.lower()
        
        if self.unit_type == "length":
            valid_units = VALID_LENGTH_UNITS
            unit_type_name = "length"
        elif self.unit_type == "weight":
            valid_units = VALID_WEIGHT_UNITS
            unit_type_name = "weight"
        elif self.unit_type == "temperature":
            valid_units = VALID_TEMPERATURE_UNITS
            unit_type_name = "temperature"
        else:
            raise ValueError(f"Invalid unit_type: {self.unit_type}")
        
        if from_unit_lower not in valid_units:
            raise ValueError(
                f"Invalid source unit '{self.from_unit}' for {unit_type_name}. "
                f"Valid units: {', '.join(sorted(valid_units))}"
            )
        
        if to_unit_lower not in valid_units:
            raise ValueError(
                f"Invalid target unit '{self.to_unit}' for {unit_type_name}. "
                f"Valid units: {', '.join(sorted(valid_units))}"
            )
        
        if from_unit_lower == to_unit_lower:
            raise ValueError(f"Source and target units cannot be the same: {self.from_unit}")


class ConvertResponse(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    result: float
    unit_type: str


# Conversion functions
def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert length units with validation"""
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    # Validate units
    if from_unit_lower not in VALID_LENGTH_UNITS:
        raise ValueError(f"Invalid source unit for length: '{from_unit}'. Valid units: {', '.join(sorted(VALID_LENGTH_UNITS))}")
    if to_unit_lower not in VALID_LENGTH_UNITS:
        raise ValueError(f"Invalid target unit for length: '{to_unit}'. Valid units: {', '.join(sorted(VALID_LENGTH_UNITS))}")
    
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
    conversion_factor = to_meter[from_unit_lower]
    value_in_meters = value * conversion_factor
    
    # Check for overflow
    if isinf(value_in_meters) or isnan(value_in_meters):
        raise ValueError(f"Calculation overflow: {value} {from_unit} results in invalid value")
    
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
    
    result = value_in_meters * from_meter[to_unit_lower]
    
    # Validate result
    if isinf(result) or isnan(result):
        raise ValueError(f"Calculation result is invalid: {result}")
    
    return result


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Convert weight units with validation"""
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    # Validate units
    if from_unit_lower not in VALID_WEIGHT_UNITS:
        raise ValueError(f"Invalid source unit for weight: '{from_unit}'. Valid units: {', '.join(sorted(VALID_WEIGHT_UNITS))}")
    if to_unit_lower not in VALID_WEIGHT_UNITS:
        raise ValueError(f"Invalid target unit for weight: '{to_unit}'. Valid units: {', '.join(sorted(VALID_WEIGHT_UNITS))}")
    
    # Convert to kilograms first
    to_kilogram = {
        "kilogram": 1.0,
        "gram": 0.001,
        "pound": 0.453592,
        "ounce": 0.0283495,
        "ton": 1000.0
    }
    
    # Convert from source unit to kilograms
    conversion_factor = to_kilogram[from_unit_lower]
    value_in_kg = value * conversion_factor
    
    # Check for overflow
    if isinf(value_in_kg) or isnan(value_in_kg):
        raise ValueError(f"Calculation overflow: {value} {from_unit} results in invalid value")
    
    # Convert from kilograms to target unit
    from_kilogram = {
        "kilogram": 1.0,
        "gram": 1000.0,
        "pound": 2.20462,
        "ounce": 35.274,
        "ton": 0.001
    }
    
    result = value_in_kg * from_kilogram[to_unit_lower]
    
    # Validate result
    if isinf(result) or isnan(result):
        raise ValueError(f"Calculation result is invalid: {result}")
    
    return result


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature units with validation"""
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    # Validate units
    if from_unit_lower not in VALID_TEMPERATURE_UNITS:
        raise ValueError(f"Invalid source unit for temperature: '{from_unit}'. Valid units: {', '.join(sorted(VALID_TEMPERATURE_UNITS))}")
    if to_unit_lower not in VALID_TEMPERATURE_UNITS:
        raise ValueError(f"Invalid target unit for temperature: '{to_unit}'. Valid units: {', '.join(sorted(VALID_TEMPERATURE_UNITS))}")
    
    # Convert to Celsius first
    try:
        if from_unit_lower == "fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit_lower == "kelvin":
            # Absolute zero check for Kelvin
            if value < 0:
                raise ValueError(f"Invalid temperature: Kelvin cannot be negative. Received: {value} K")
            celsius = value - 273.15
        else:  # celsius
            celsius = value
        
        # Validate intermediate result
        if isinf(celsius) or isnan(celsius):
            raise ValueError(f"Calculation error: {value} {from_unit} results in invalid Celsius value")
        
        # Convert from Celsius to target unit
        if to_unit_lower == "fahrenheit":
            result = celsius * 9 / 5 + 32
        elif to_unit_lower == "kelvin":
            result = celsius + 273.15
            # Validate Kelvin result (cannot be negative)
            if result < 0:
                raise ValueError(f"Conversion result is invalid: {result} K (below absolute zero)")
        else:  # celsius
            result = celsius
        
        # Validate final result
        if isinf(result) or isnan(result):
            raise ValueError(f"Calculation result is invalid: {result}")
        
        return result
    except ZeroDivisionError:
        raise ValueError("Division by zero error in temperature conversion")
    except OverflowError:
        raise ValueError(f"Temperature conversion overflow for value: {value} {from_unit}")


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
        # Validate input value
        if isnan(request.value):
            raise HTTPException(
                status_code=400,
                detail="Invalid input: Value cannot be NaN (Not a Number)"
            )
        if isinf(request.value):
            raise HTTPException(
                status_code=400,
                detail="Invalid input: Value cannot be Infinity"
            )
        
        # Perform conversion based on unit type
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
        
        # Validate result before returning
        if isnan(result) or isinf(result):
            raise HTTPException(
                status_code=500,
                detail=f"Calculation error: Result is invalid (NaN or Infinity). Please check your input values."
            )
        
        return ConvertResponse(
            value=request.value,
            from_unit=request.from_unit,
            to_unit=request.to_unit,
            result=round(result, 6),
            unit_type=request.unit_type
        )
    except ValidationError as e:
        # Pydantic validation errors
        error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        raise HTTPException(
            status_code=422,
            detail=f"Validation error: {'; '.join(error_messages)}"
        )
    except ValueError as e:
        # Value errors from conversion functions
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except OverflowError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Calculation overflow: The result is too large to compute. {str(e)}"
        )
    except ZeroDivisionError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Division by zero error: {str(e)}"
        )
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during conversion: {str(e)}. Please check your input and try again."
        )


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


