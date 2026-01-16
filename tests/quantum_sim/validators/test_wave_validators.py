# tests/quantum_sim/validators/test_wave_validators.py
from quantum_sim.validators import (
    validate_positive,
    validate_non_negative,
    validate_range,
)
from quantum_sim.errors import InvalidParameterError
import pytest

@pytest.mark.unit
@pytest.mark.parametrize("value", [1, 0.1, 100])
def test_validate_positive_valid(value):
    assert validate_positive(value) is True

@pytest.mark.unit
@pytest.mark.parametrize("value", [0, -1, -0.0001])
def test_validate_positive_invalid(value):
    with pytest.raises(InvalidParameterError) as exc_info:
        validate_positive(value)
    assert exc_info.value.parameter == "value"
    assert exc_info.value.message == "Value must be positive"
    assert "Value must be positive" in str(exc_info.value)

@pytest.mark.unit
def test_validate_positive_custom_parameter_name():
    with pytest.raises(InvalidParameterError) as exc_info:
        validate_positive(-5, parameter_name="length")
    assert exc_info.value.parameter == "length"

@pytest.mark.unit
@pytest.mark.parametrize("value", [0, 1, 1.5])
def test_validate_non_negative_valid(value):
    assert validate_non_negative(value) is True

@pytest.mark.unit
@pytest.mark.parametrize("value", [-0.1, -1])
def test_validate_non_negative_invalid(value):
    with pytest.raises(InvalidParameterError) as exc_info:
        validate_non_negative(value, parameter_name="x")
    assert exc_info.value.parameter == "x"
    assert exc_info.value.message == "Value must be non-negative"

@pytest.mark.unit
@pytest.mark.parametrize("value,minv,maxv", [(5, 0, 10), (0, 0, 0), (3.5, 1.5, 4.0)])
def test_validate_range_valid(value, minv, maxv):
    assert validate_range(value, minv, maxv) is True

@pytest.mark.unit
@pytest.mark.parametrize("value,minv,maxv", [(-1, 0, 5), (6, 0, 5), (10.1, 0, 10)])
def test_validate_range_invalid(value, minv, maxv):
    with pytest.raises(InvalidParameterError) as exc_info:
        validate_range(value, minv, maxv, parameter_name="range_param")
    assert exc_info.value.parameter == "range_param"
    assert f"Value must be between {minv} and {maxv}" == exc_info.value.message
    assert f"between {minv} and {maxv}" in str(exc_info.value)

@pytest.mark.unit
def test_validate_range_type_error():
    with pytest.raises(TypeError):
        validate_range("a", 0, 10)


