# tests/quantum_sim/errors/test_exceptions.py
from quantum_sim.errors import *
import pytest

@pytest.mark.unit
def test_quantum_sim_error():
    with pytest.raises(QuantumSimError):
        raise QuantumSimError("Base error")

@pytest.mark.unit
def test_quantum_sim_error_subclass_invalid_parameter():
    with pytest.raises(QuantumSimError):
        raise InvalidParameterError("test_param")

@pytest.mark.unit
def test_quantum_sim_error_subclass_simulation():
    with pytest.raises(QuantumSimError):
        raise SimulationError("Simulation failed")

@pytest.mark.unit
def test_invalid_parameter_error():
    parameter = "invalid_value"
    message = "Parameter is not valid"
    with pytest.raises(InvalidParameterError) as exc_info:
        raise InvalidParameterError(parameter, message)
    assert str(exc_info.value) == f"{message}: {parameter}"

@pytest.mark.unit
def test_invalid_parameter_error_default_message():
    parameter = "invalid_value"
    with pytest.raises(InvalidParameterError) as exc_info:
        raise InvalidParameterError(parameter)
    assert str(exc_info.value) == f"Invalid parameter provided: {parameter}"

@pytest.mark.unit
def test_invalid_parameter_error_no_parameter():
    with pytest.raises(InvalidParameterError) as exc_info:
        raise InvalidParameterError(None)
    assert str(exc_info.value) == "Invalid parameter provided: None"

@pytest.mark.unit
def test_invalid_parameter_attributes_with_message():
    parameter = "invalid_value"
    message = "Parameter is not valid"
    with pytest.raises(InvalidParameterError) as exc_info:
        raise InvalidParameterError(parameter, message)
    assert exc_info.value.parameter == parameter
    assert exc_info.value.message == message

@pytest.mark.unit
def test_simulation_error():
    message = "Simulation failed due to unknown error"
    with pytest.raises(SimulationError) as exc_info:
        raise SimulationError(message)
    assert str(exc_info.value) == message

@pytest.mark.unit
def test_simulation_error_default_message():
    with pytest.raises(SimulationError) as exc_info:
        raise SimulationError()
    assert str(exc_info.value) == "An error occurred during the simulation"

@pytest.mark.unit
def test_invalid_parameter_attributes_with_message():
    parameter = "invalid_value"
    message = "Parameter is not valid"
    with pytest.raises(InvalidParameterError) as exc_info:
        raise InvalidParameterError(parameter, message)
    assert exc_info.value.parameter == parameter
    assert exc_info.value.message == message

@pytest.mark.unit
def test_invalid_parameter_attributes_default_message():
    parameter = "invalid_value"
    with pytest.raises(InvalidParameterError) as exc_info:
        raise InvalidParameterError(parameter)
    assert exc_info.value.parameter == parameter
    assert exc_info.value.message == "Invalid parameter provided"

@pytest.mark.unit
def test_simulation_error_message_attribute_default():
    with pytest.raises(SimulationError) as exc_info:
        raise SimulationError()
    assert exc_info.value.message == "An error occurred during the simulation"
    