import pytest
import numpy as np
from quantum_sim.potentials.Potential import Potential
from quantum_sim.potentials.FreePotential import FreePotential
from quantum_sim.potentials.StepPotential import StepPotential
from quantum_sim.potentials.InfiniteWell import InfiniteWell


class TestPotentialCreation:
    """Test creation and basic properties of potential classes."""

    def test_free_potential_creation(self):
        """Test FreePotential instantiation."""
        pot = FreePotential()
        assert isinstance(pot, Potential)
        assert pot.parameters == {}
        assert str(pot) == "FreePotential: V(x) = 0"

    def test_free_potential_evaluation(self):
        """Test FreePotential evaluation."""
        pot = FreePotential()
        x_vals = np.array([-1.0, 0.0, 1.0, 5.0])
        V_vals = pot.evaluate(x_vals)
        np.testing.assert_array_equal(V_vals, np.zeros_like(x_vals))

    def test_step_potential_creation(self):
        """Test StepPotential instantiation."""
        x0, V0 = 2.0, 5.0
        pot = StepPotential(x0=x0, V0=V0)
        assert isinstance(pot, Potential)
        assert pot.parameters == {"x0": x0, "V0": V0}
        expected_str = f"StepPotential: V(x) = 0 for x < {x0}, V(x) = {V0} for x >= {x0}"
        assert str(pot) == expected_str

    def test_step_potential_evaluation(self):
        """Test StepPotential evaluation."""
        x0, V0 = 2.0, 5.0
        pot = StepPotential(x0=x0, V0=V0)
        x_vals = np.array([0.0, 1.9, 2.0, 2.1, 5.0])
        V_vals = pot.evaluate(x_vals)
        expected = np.array([0.0, 0.0, V0, V0, V0])
        np.testing.assert_array_equal(V_vals, expected)

    def test_infinite_well_creation(self):
        """Test InfiniteWell instantiation."""
        a, b, V_wall = -1.0, 1.0, 1e10
        pot = InfiniteWell(a=a, b=b, V_wall=V_wall)
        assert isinstance(pot, Potential)
        assert pot.parameters == {"a": a, "b": b, "V_wall": V_wall}
        expected_str = f"InfiniteWell: V(x) = 0 for {a} < x < {b}, V(x) = {V_wall} otherwise"
        assert str(pot) == expected_str

    def test_infinite_well_creation_invalid_bounds(self):
        """Test InfiniteWell with invalid bounds raises error."""
        with pytest.raises(ValueError, match="Left boundary 'a' must be less than right boundary 'b'"):
            InfiniteWell(a=1.0, b=1.0)

    def test_infinite_well_evaluation(self):
        """Test InfiniteWell evaluation."""
        a, b, V_wall = -1.0, 1.0, 1e10
        pot = InfiniteWell(a=a, b=b, V_wall=V_wall)
        x_vals = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
        V_vals = pot.evaluate(x_vals)
        expected = np.array([V_wall, 0.0, 0.0, 0.0, V_wall])
        np.testing.assert_array_equal(V_vals, expected)