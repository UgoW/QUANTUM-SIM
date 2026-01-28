import numpy as np
import pytest
from quantum_sim.utils.constants import (
    PLANCK_CONSTANT,
    PI,
    REDUCED_PLANCK_CONSTANT,
    ELECTRON_MASS,
    SPEED_OF_LIGHT,
)


class TestPhysicalConstants:
    """Test suite for physical constants."""

    def test_planck_constant_value(self):
        """Test Planck constant has correct value in J·s."""
        assert PLANCK_CONSTANT == pytest.approx(6.62607015e-34)

    def test_planck_constant_positive(self):
        """Test Planck constant is positive."""
        assert PLANCK_CONSTANT > 0

    def test_pi_value(self):
        """Test PI constant matches numpy.pi."""
        assert PI == pytest.approx(np.pi)

    def test_reduced_planck_constant_value(self):
        """Test reduced Planck constant has correct value."""
        expected = PLANCK_CONSTANT / (2 * np.pi)
        assert REDUCED_PLANCK_CONSTANT == pytest.approx(expected)

    def test_reduced_planck_constant_positive(self):
        """Test reduced Planck constant is positive."""
        assert REDUCED_PLANCK_CONSTANT > 0

    def test_reduced_planck_constant_less_than_planck(self):
        """Test reduced Planck constant is less than Planck constant."""
        assert REDUCED_PLANCK_CONSTANT < PLANCK_CONSTANT

    def test_electron_mass_value(self):
        """Test electron mass has correct value in kg."""
        assert ELECTRON_MASS == pytest.approx(9.10938356e-31)

    def test_electron_mass_positive(self):
        """Test electron mass is positive."""
        assert ELECTRON_MASS > 0

    def test_speed_of_light_value(self):
        """Test speed of light has correct value in m/s."""
        assert SPEED_OF_LIGHT == pytest.approx(2.99792458e8)

    def test_speed_of_light_positive(self):
        """Test speed of light is positive."""
        assert SPEED_OF_LIGHT > 0

    def test_constants_are_numeric(self):
        """Test all constants are numeric types."""
        assert isinstance(PLANCK_CONSTANT, (int, float, np.number))
        assert isinstance(PI, (int, float, np.number))
        assert isinstance(REDUCED_PLANCK_CONSTANT, (int, float, np.number))
        assert isinstance(ELECTRON_MASS, (int, float, np.number))
        assert isinstance(SPEED_OF_LIGHT, (int, float, np.number))

    def test_planck_reduced_planck_relationship(self):
        """Test the mathematical relationship between Planck constants."""
        calculated_reduced = PLANCK_CONSTANT / (2 * PI)
        assert calculated_reduced == pytest.approx(REDUCED_PLANCK_CONSTANT)

    def test_physical_constants_order_of_magnitude(self):
        """Test physical constants have reasonable orders of magnitude."""
        # Planck constant should be very small
        assert 1e-35 < PLANCK_CONSTANT < 1e-30

        # Reduced Planck constant should be very small
        assert 1e-35 < REDUCED_PLANCK_CONSTANT < 1e-30

        # Electron mass should be very small
        assert 1e-32 < ELECTRON_MASS < 1e-29

        # Speed of light should be around 3e8
        assert 2.9e8 < SPEED_OF_LIGHT < 3.1e8
