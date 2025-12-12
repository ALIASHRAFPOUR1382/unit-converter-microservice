#!/usr/bin/env python3
# Interactive unit converter
# Run this to convert units interactively

def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert length units"""
    to_meter = {
        "meter": 1.0, "m": 1.0,
        "kilometer": 1000.0, "km": 1000.0,
        "centimeter": 0.01, "cm": 0.01,
        "millimeter": 0.001, "mm": 0.001,
        "mile": 1609.34, "mi": 1609.34,
        "foot": 0.3048, "ft": 0.3048,
        "inch": 0.0254, "in": 0.0254,
        "yard": 0.9144, "yd": 0.9144
    }
    
    value_in_meters = value * to_meter.get(from_unit.lower(), 1.0)
    
    from_meter = {
        "meter": 1.0, "m": 1.0,
        "kilometer": 0.001, "km": 0.001,
        "centimeter": 100.0, "cm": 100.0,
        "millimeter": 1000.0, "mm": 1000.0,
        "mile": 0.000621371, "mi": 0.000621371,
        "foot": 3.28084, "ft": 3.28084,
        "inch": 39.3701, "in": 39.3701,
        "yard": 1.09361, "yd": 1.09361
    }
    
    return value_in_meters * from_meter.get(to_unit.lower(), 1.0)


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Convert weight units"""
    to_kilogram = {
        "kilogram": 1.0, "kg": 1.0,
        "gram": 0.001, "g": 0.001,
        "pound": 0.453592, "lb": 0.453592,
        "ounce": 0.0283495, "oz": 0.0283495,
        "ton": 1000.0, "t": 1000.0
    }
    
    value_in_kg = value * to_kilogram.get(from_unit.lower(), 1.0)
    
    from_kilogram = {
        "kilogram": 1.0, "kg": 1.0,
        "gram": 1000.0, "g": 1000.0,
        "pound": 2.20462, "lb": 2.20462,
        "ounce": 35.274, "oz": 35.274,
        "ton": 0.001, "t": 0.001
    }
    
    return value_in_kg * from_kilogram.get(to_unit.lower(), 1.0)


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature units"""
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()
    
    if from_unit_lower in ["fahrenheit", "f"]:
        celsius = (value - 32) * 5 / 9
    elif from_unit_lower in ["kelvin", "k"]:
        celsius = value - 273.15
    else:  # celsius, c
        celsius = value
    
    if to_unit_lower in ["fahrenheit", "f"]:
        return celsius * 9 / 5 + 32
    elif to_unit_lower in ["kelvin", "k"]:
        return celsius + 273.15
    else:  # celsius, c
        return celsius


def main():
    print("=" * 60)
    print("Unit Converter - Interactive Mode")
    print("=" * 60)
    print()
    print("Available unit types:")
    print("  1. length (meter, kilometer, mile, foot, etc.)")
    print("  2. weight (kilogram, gram, pound, etc.)")
    print("  3. temperature (celsius, fahrenheit, kelvin)")
    print()
    print("Type 'quit' or 'exit' to stop")
    print("=" * 60)
    print()
    
    while True:
        try:
            # Get unit type
            unit_type = input("Enter unit type (length/weight/temperature): ").strip().lower()
            if unit_type in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            if unit_type not in ["length", "weight", "temperature"]:
                print("Invalid unit type! Please enter: length, weight, or temperature")
                print()
                continue
            
            # Get value
            value_str = input("Enter value to convert: ").strip()
            if value_str in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            value = float(value_str)
            
            # Get from unit
            from_unit = input(f"Enter source unit: ").strip()
            if from_unit.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            # Get to unit
            to_unit = input(f"Enter target unit: ").strip()
            if to_unit.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            
            # Convert
            if unit_type == "length":
                result = convert_length(value, from_unit, to_unit)
            elif unit_type == "weight":
                result = convert_weight(value, from_unit, to_unit)
            else:  # temperature
                result = convert_temperature(value, from_unit, to_unit)
            
            # Display result
            print()
            print("-" * 60)
            print(f"Result: {value} {from_unit} = {result:.6f} {to_unit}")
            print("-" * 60)
            print()
            
        except ValueError:
            print("Error: Invalid number! Please enter a valid number.")
            print()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()


if __name__ == "__main__":
    main()


