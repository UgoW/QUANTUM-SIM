# src/quantum_sim/errors/exceptions.py


class QuantumSimError(Exception):
    """Base class for exceptions in Quantum Sim."""
    pass

class InvalidParameterError(QuantumSimError):
    """Exception raised for invalid parameters."""
    def __init__(self: QuantumSimError, parameter, message: str ="Invalid parameter provided"):
        self.parameter = parameter
        self.message = message
        super().__init__(self.message)

    def __str__(self: QuantumSimError):
        return f"{self.message}: {self.parameter}"

class SimulationError(QuantumSimError):
    """Exception raised for errors during simulation."""
    def __init__(self: QuantumSimError, message: str="An error occurred during the simulation"):
        self.message = message
        super().__init__(self.message)

    def __str__(self: QuantumSimError):
        return self.message

