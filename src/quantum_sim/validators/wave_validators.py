# src/quantum_sim/validators/wave_validators.py
from ..errors.exceptions import InvalidParameterError

def validate_positive(value, parameter_name="value"):
    """Validate that the given value is positive."""
    if value <= 0:
        raise InvalidParameterError(parameter=parameter_name, message="Value must be positive")
    return True

def validate_non_negative(value, parameter_name="value"):
    """Validate that the given value is non-negative."""
    if value < 0:
        raise InvalidParameterError(parameter=parameter_name, message="Value must be non-negative")
    return True

def validate_range(value, min_value, max_value, parameter_name="value"):
    """Validate that the given value is within the specified range [min_value, max_value]."""
    if not (min_value <= value <= max_value):
        raise InvalidParameterError(
            parameter=parameter_name,
            message=f"Value must be between {min_value} and {max_value}"
        )
    return True
