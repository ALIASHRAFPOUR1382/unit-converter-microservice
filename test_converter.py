#!/usr/bin/env python3
# Simple unit converter test script
# Run this to test conversions without server

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


def convert(value: float, from_unit: str, to_unit: str, unit_type: str) -> float:
    """Main conversion function"""
    if unit_type == "length":
        return convert_length(value, from_unit, to_unit)
    elif unit_type == "weight":
        return convert_weight(value, from_unit, to_unit)
    elif unit_type == "temperature":
        return convert_temperature(value, from_unit, to_unit)
    else:
        raise ValueError(f"Unsupported unit type: {unit_type}")


# Test examples
if __name__ == "__main__":
    print("=" * 50)
    print("Unit Converter Test")
    print("=" * 50)
    print()
    
    # Test 1: Length conversion
    print("Test 1: Length Conversion")
    print("-" * 50)
    value = 100
    from_unit = "kilometer"
    to_unit = "mile"
    result = convert(value, from_unit, to_unit, "length")
    print(f"{value} {from_unit} = {result:.2f} {to_unit}")
    print()
    
    # Test 2: Weight conversion
    print("Test 2: Weight Conversion")
    print("-" * 50)
    value = 50
    from_unit = "kilogram"
    to_unit = "pound"
    result = convert(value, from_unit, to_unit, "weight")
    print(f"{value} {from_unit} = {result:.2f} {to_unit}")
    print()
    
    # Test 3: Temperature conversion
    print("Test 3: Temperature Conversion")
    print("-" * 50)
    value = 25
    from_unit = "celsius"
    to_unit = "fahrenheit"
    result = convert(value, from_unit, to_unit, "temperature")
    print(f"{value}° {from_unit} = {result:.2f}° {to_unit}")
    print()
    
    # Test 4: More examples
    print("Test 4: More Examples")
    print("-" * 50)
    tests = [
        (10, "meter", "foot", "length"),
        (5, "kilogram", "gram", "weight"),
        (0, "celsius", "fahrenheit", "temperature"),
        (100, "celsius", "kelvin", "temperature"),
    ]
    
    for value, from_unit, to_unit, unit_type in tests:
        result = convert(value, from_unit, to_unit, unit_type)
        print(f"{value} {from_unit} = {result:.2f} {to_unit}")
    
    print()
    print("=" * 50)
    print("All tests completed!")
    print("=" * 50)


