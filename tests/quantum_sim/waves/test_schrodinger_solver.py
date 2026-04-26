import numpy as np
import pytest

from quantum_sim.waves import PlaneWave, SchrodingerSolver, WavePacket
import quantum_sim.waves.schrodinger_solver as solver_module


@pytest.fixture
def solver():
    return SchrodingerSolver(
        x_min=-10.0,
        x_max=10.0,
        n_points=101,
        absorbing_boundaries=True,
        absorb_width=2.0,
        gamma_cap=1e-3,
    )


@pytest.mark.unit
def test_solver_init_validates_domain_bounds():
    with pytest.raises(ValueError, match="x_min"):
        SchrodingerSolver(x_min=1.0, x_max=1.0)


@pytest.mark.unit
def test_solver_init_validates_minimum_number_of_points():
    with pytest.raises(ValueError, match="n_points"):
        SchrodingerSolver(x_min=-1.0, x_max=1.0, n_points=2)


@pytest.mark.unit
def test_solver_init_validates_positive_mass():
    with pytest.raises(ValueError, match="mass"):
        SchrodingerSolver(x_min=-1.0, x_max=1.0, mass=0.0)


@pytest.mark.unit
def test_build_laplacian_has_expected_shape_and_stencil(solver):
    lap = solver._laplacian
    assert lap.shape == (solver.n_points, solver.n_points)

    center = solver.n_points // 2
    row = lap.getrow(center).toarray().ravel()
    expected = np.zeros(solver.n_points)
    expected[center - 1] = 1.0 / solver.dx**2
    expected[center] = -2.0 / solver.dx**2
    expected[center + 1] = 1.0 / solver.dx**2

    assert np.allclose(row, expected)


@pytest.mark.unit
def test_cap_is_zero_in_center_and_positive_at_edges(solver):
    cap = solver._cap
    center = solver.n_points // 2

    assert cap[0] > 0
    assert cap[-1] > 0
    assert cap[center] == 0


@pytest.mark.unit
def test_cap_is_all_zero_when_absorbing_boundaries_disabled():
    no_cap_solver = SchrodingerSolver(
        x_min=-5.0,
        x_max=5.0,
        n_points=51,
        absorbing_boundaries=False,
    )
    assert np.allclose(no_cap_solver._cap, 0.0)


@pytest.mark.unit
def test_set_potential_validates_shape(solver):
    with pytest.raises(ValueError, match="shape"):
        solver.set_potential(np.zeros(solver.n_points - 1))


@pytest.mark.unit
def test_set_potential_accepts_valid_array(solver):
    V = np.linspace(0.0, 1.0, solver.n_points)
    solver.set_potential(V)
    assert np.allclose(solver._V, V)


@pytest.mark.unit
def test_init_from_array_validates_shape(solver):
    with pytest.raises(ValueError, match="shape"):
        solver.init_from_array(np.ones(solver.n_points - 1, dtype=complex))


@pytest.mark.unit
def test_init_from_array_normalize_true_produces_unit_norm(solver):
    psi0 = np.exp(-0.5 * (solver.x_grid / 2.0) ** 2)
    solver.init_from_array(psi0, normalize=True)

    norm = np.trapezoid(np.abs(solver._psi_0) ** 2) * solver.dx
    assert np.isclose(norm, 1.0, atol=1e-6)


@pytest.mark.unit
def test_init_from_array_raises_for_non_normalizable_input(solver):
    with pytest.raises(ValueError, match="Cannot normalise"):
        solver.init_from_array(np.zeros(solver.n_points, dtype=complex), normalize=True)


@pytest.mark.unit
def test_init_from_array_without_normalization_keeps_values(solver):
    psi0 = np.linspace(0.0, 1.0, solver.n_points) + 1j * np.linspace(1.0, 0.0, solver.n_points)
    solver.init_from_array(psi0, normalize=False)

    assert np.allclose(solver._psi_0, psi0)


@pytest.mark.unit
def test_init_from_packet_sets_normalized_initial_state(solver):
    packet = WavePacket([PlaneWave(amplitude=1.0 + 0.0j, wave_number=1.5)])
    solver.init_from_packet(packet)

    norm = np.trapezoid(np.abs(solver._psi_0) ** 2) * solver.dx
    assert np.isclose(norm, 1.0, atol=1e-6)


@pytest.mark.unit
def test_rhs_returns_expected_shape_and_dtype(solver):
    psi = np.exp(-0.5 * (solver.x_grid / 2.0) ** 2).astype(complex)
    rhs = solver._rhs(0.0, psi)

    assert rhs.shape == (solver.n_points,)
    assert np.iscomplexobj(rhs)


@pytest.mark.unit
def test_solve_raises_if_initial_state_not_set(solver):
    with pytest.raises(RuntimeError, match="Initial state"):
        solver.solve(t_final=0.1, dt=0.01)


@pytest.mark.unit
def test_solve_validates_positive_times(solver):
    psi0 = np.exp(-0.5 * (solver.x_grid / 2.0) ** 2)
    solver.init_from_array(psi0)

    with pytest.raises(ValueError, match="t_final"):
        solver.solve(t_final=0.0, dt=0.01)

    with pytest.raises(ValueError, match="dt"):
        solver.solve(t_final=0.1, dt=0.0)


@pytest.mark.unit
def test_solve_validates_absorb_width_vs_domain():
    too_wide_solver = SchrodingerSolver(
        x_min=-1.0,
        x_max=1.0,
        n_points=51,
        absorb_width=1.0,
    )
    psi0 = np.exp(-0.5 * (too_wide_solver.x_grid / 0.2) ** 2)
    too_wide_solver.init_from_array(psi0)

    with pytest.raises(ValueError, match="absorb_width"):
        too_wide_solver.solve(t_final=0.1, dt=0.01)


@pytest.mark.unit
def test_solve_returns_expected_result_shapes(solver):
    psi0 = np.exp(-0.5 * (solver.x_grid / 2.0) ** 2)
    solver.init_from_array(psi0)

    result = solver.solve(t_final=0.02, dt=0.01)

    assert set(result.keys()) == {"x", "t", "psi", "prob"}
    assert result["x"].shape == (solver.n_points,)
    assert result["t"].shape == (3,)
    assert result["psi"].shape == (solver.n_points, 3)
    assert result["prob"].shape == (solver.n_points, 3)
    assert np.allclose(result["prob"], np.abs(result["psi"]) ** 2)


@pytest.mark.unit
def test_solve_raises_runtime_error_when_integrator_fails(solver, monkeypatch):
    psi0 = np.exp(-0.5 * (solver.x_grid / 2.0) ** 2)
    solver.init_from_array(psi0)

    class FailingSolution:
        success = False
        message = "integration failed"

    def fake_solve_ivp(*args, **kwargs):
        return FailingSolution()

    monkeypatch.setattr(solver_module, "solve_ivp", fake_solve_ivp)

    with pytest.raises(RuntimeError, match="Solver failed"):
        solver.solve(t_final=0.02, dt=0.01)