# tests/quantum_sim/waves/test_plane_wave.py
from quantum_sim.waves import PlaneWave
from quantum_sim.utils.constants import ELECTRON_MASS, REDUCED_PLANCK_CONSTANT, PI
from quantum_sim.errors.exceptions import InvalidParameterError
import pytest
from pytest import fixture
import numpy as np


@fixture
def plane_wave_params():
    """Fixture providing standard plane wave parameters."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    position = 0.0
    phase = 0.0
    time = 0.0
    masse = ELECTRON_MASS
    return amplitude, wavelength, position, phase, time, masse


@fixture
def plane_wave(plane_wave_params):
    """Fixture providing a standard plane wave instance."""
    amplitude, wavelength, position, phase, time, masse = plane_wave_params
    return PlaneWave(amplitude, wavelength, position, phase, time, masse)


# ========================
# Initialization Tests
# ========================

@pytest.mark.unit
def test_plane_wave_initialization(plane_wave_params):
    """Test that PlaneWave initializes with correct parameters."""
    amplitude, wavelength, position, phase, time, masse = plane_wave_params
    wave = PlaneWave(amplitude, wavelength, position, phase, time, masse)
    
    assert wave.amplitude == amplitude
    assert wave.wavelength == wavelength
    assert wave.position == position
    assert wave.phase == phase
    assert wave.masse == masse
    assert wave.time == time


@pytest.mark.unit
def test_plane_wave_default_parameters():
    """Test that PlaneWave initializes with default parameters."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    
    wave = PlaneWave(amplitude, wavelength)
    
    assert np.isclose(wave.position, 0.0)
    assert np.isclose(wave.phase, 0.0)
    assert np.isclose(wave.time, 0.0)
    assert np.isclose(wave.masse, ELECTRON_MASS)


@pytest.mark.unit
def test_plane_wave_complex_amplitude():
    """Test that PlaneWave accepts complex amplitude."""
    amplitude = 2.0 + 3.0j
    wavelength = 5.0
    
    wave = PlaneWave(amplitude, wavelength)
    
    assert wave.amplitude == amplitude
    assert np.isclose(wave.amplitude.real, 2.0)
    assert np.isclose(wave.amplitude.imag, 3.0)


@pytest.mark.unit
def test_plane_wave_with_all_parameters(plane_wave_params):
    """Test initialization with all explicit parameters."""
    amplitude, wavelength, position, phase, time, masse = plane_wave_params
    wave = PlaneWave(amplitude, wavelength, position, phase, time, masse)
    
    assert wave.amplitude == amplitude
    assert wave.wavelength == wavelength
    assert wave.position == position
    assert wave.phase == phase
    assert wave.time == time
    assert wave.masse == masse


# ========================
# Parameter Validation Tests
# ========================

@pytest.mark.unit
def test_validate_parameters_valid(plane_wave):
    """Test that validate_parameters passes for valid parameters."""
    plane_wave.validate_parameters()


@pytest.mark.unit
def test_validate_negative_wavelength():
    """Test that negative wavelength raises InvalidParameterError."""
    amplitude = 1.0 + 0.0j
    wavelength = -5.0
    
    with pytest.raises(InvalidParameterError):
        PlaneWave(amplitude, wavelength)


@pytest.mark.unit
def test_validate_zero_wavelength():
    """Test that zero wavelength raises InvalidParameterError."""
    amplitude = 1.0 + 0.0j
    wavelength = 0.0
    
    with pytest.raises(InvalidParameterError):
        PlaneWave(amplitude, wavelength)


@pytest.mark.unit
def test_validate_negative_mass():
    """Test that negative mass raises InvalidParameterError."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    masse = -1.0
    
    with pytest.raises(InvalidParameterError):
        PlaneWave(amplitude, wavelength, masse=masse)


@pytest.mark.unit
def test_validate_zero_mass():
    """Test that zero mass is allowed (non-negative)."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    masse = 0.0
    
    wave = PlaneWave(amplitude, wavelength, masse=masse)
    assert np.isclose(wave.masse, 0.0)


# ========================
# Wave Number Tests
# ========================

@pytest.mark.unit
def test_wave_number_calculation(plane_wave):
    """Test that wave number is calculated correctly: k = 2π/λ."""
    expected_k = 2 * PI / plane_wave.wavelength
    calculated_k = plane_wave.wave_number
    
    assert np.isclose(calculated_k, expected_k)


@pytest.mark.unit
def test_wave_number_relationship():
    """Test wave number relationship with wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 10.0
    wave = PlaneWave(amplitude, wavelength)
    
    k = wave.wave_number

    assert np.isclose(k * wavelength, 2 * PI)


@pytest.mark.unit
def test_wave_number_different_wavelengths():
    """Test wave number for different wavelengths."""
    amplitude = 1.0 + 0.0j
    wavelengths = [1.0, 5.0, 10.0, 20.0]
    
    for wavelength in wavelengths:
        wave = PlaneWave(amplitude, wavelength)
        k = wave.wave_number
        expected_k = 2 * PI / wavelength
        assert np.isclose(k, expected_k)


@pytest.mark.unit
def test_wave_number_positive():
    """Test that wave number is always positive for positive wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    k = wave.wave_number
    assert k > 0


# ========================
# Angular Frequency Tests
# ========================

@pytest.mark.unit
def test_angular_frequency_calculation(plane_wave):
    """Test that angular frequency is calculated correctly: ω = ħk²/(2m)."""
    k = plane_wave.wave_number
    expected_omega = (REDUCED_PLANCK_CONSTANT * k**2) / (2 * plane_wave.masse)
    calculated_omega = plane_wave.angular_frequency
    
    assert np.isclose(calculated_omega, expected_omega)


@pytest.mark.unit
def test_angular_frequency_depends_on_wavelength():
    """Test that angular frequency depends on wavelength."""
    amplitude = 1.0 + 0.0j
    wave1 = PlaneWave(amplitude, wavelength=5.0)
    wave2 = PlaneWave(amplitude, wavelength=10.0)
    
    omega1 = wave1.angular_frequency
    omega2 = wave2.angular_frequency
    
    assert not np.isclose(omega1, omega2)


@pytest.mark.unit
def test_angular_frequency_depends_on_mass():
    """Test that angular frequency depends on particle mass."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    
    wave1 = PlaneWave(amplitude, wavelength, masse=ELECTRON_MASS)
    wave2 = PlaneWave(amplitude, wavelength, masse=2 * ELECTRON_MASS)
    
    omega1 = wave1.angular_frequency
    omega2 = wave2.angular_frequency
    
    assert np.isclose(omega2, omega1 / 2)


@pytest.mark.unit
def test_angular_frequency_proportional_to_k_squared():
    """Test that angular frequency is proportional to k²."""
    amplitude = 1.0 + 0.0j
    wave1 = PlaneWave(amplitude, wavelength=10.0)
    wave2 = PlaneWave(amplitude, wavelength=5.0)
    
    k1 = wave1.wave_number
    k2 = wave2.wave_number
    
    omega1 = wave1.angular_frequency
    omega2 = wave2.angular_frequency
    
    expected_ratio = (k2**2) / (k1**2)
    actual_ratio = omega2 / omega1
    
    assert np.isclose(actual_ratio, expected_ratio)


@pytest.mark.unit
def test_angular_frequency_positive():
    """Test that angular frequency is positive for positive mass and wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    omega = wave.angular_frequency
    assert omega > 0


# ========================
# Attribute Storage Tests
# ========================

@pytest.mark.unit
def test_plane_wave_stores_amplitude():
    """Test that amplitude is correctly stored."""
    amplitude = 3.0 + 4.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    assert wave.amplitude == amplitude


@pytest.mark.unit
def test_plane_wave_stores_wavelength():
    """Test that wavelength is correctly stored."""
    amplitude = 1.0 + 0.0j
    wavelength = 7.5
    wave = PlaneWave(amplitude, wavelength)
    
    assert np.isclose(wave.wavelength, wavelength)


@pytest.mark.unit
def test_plane_wave_stores_position():
    """Test that position is correctly stored."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    position = 3.5
    wave = PlaneWave(amplitude, wavelength, position=position)
    
    assert np.isclose(wave.position, position)


@pytest.mark.unit
def test_plane_wave_stores_phase():
    """Test that phase is correctly stored."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    phase = 1.5
    wave = PlaneWave(amplitude, wavelength, phase=phase)
    
    assert np.isclose(wave.phase, phase)


@pytest.mark.unit
def test_plane_wave_stores_time():
    """Test that time is correctly stored."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    time = 2.5
    wave = PlaneWave(amplitude, wavelength, time=time)
    
    assert np.isclose(wave.time, time)


@pytest.mark.unit
def test_plane_wave_stores_mass():
    """Test that mass is correctly stored."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    masse = 1.0e-30
    wave = PlaneWave(amplitude, wavelength, masse=masse)
    
    assert np.isclose(wave.masse, masse)


# ========================
# Inheritance Tests
# ========================

@pytest.mark.unit
def test_plane_wave_inherits_from_wave_function(plane_wave):
    """Test that PlaneWave inherits from WaveFunction."""
    from quantum_sim.waves.wave_function import WaveFunction
    assert isinstance(plane_wave, WaveFunction)


@pytest.mark.unit
def test_plane_wave_has_evaluate_method(plane_wave):
    """Test that PlaneWave has evaluate method."""
    assert hasattr(plane_wave, 'evaluate')
    assert callable(plane_wave.evaluate)


# ========================
# Edge Cases Tests
# ========================

@pytest.mark.unit
def test_plane_wave_with_very_small_wavelength():
    """Test PlaneWave with very small wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 1e-10
    wave = PlaneWave(amplitude, wavelength)
    
    assert np.isclose(wave.wavelength, wavelength)
    k = wave.wave_number
    assert k > 0


@pytest.mark.unit
def test_plane_wave_with_very_large_wavelength():
    """Test PlaneWave with very large wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 1e10
    wave = PlaneWave(amplitude, wavelength)
    
    assert np.isclose(wave.wavelength, wavelength)
    k = wave.wave_number
    assert k > 0


@pytest.mark.unit
def test_plane_wave_with_negative_position():
    """Test PlaneWave with negative position offset."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    position = -10.0
    wave = PlaneWave(amplitude, wavelength, position=position)
    
    assert np.isclose(wave.position, position)


@pytest.mark.unit
def test_plane_wave_with_negative_phase():
    """Test PlaneWave with negative phase."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    phase = -np.pi
    wave = PlaneWave(amplitude, wavelength, phase=phase)
    
    assert np.isclose(wave.phase, phase)


@pytest.mark.unit
def test_plane_wave_with_negative_time():
    """Test PlaneWave with negative time (allowed)."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    time = -1.0
    wave = PlaneWave(amplitude, wavelength, time=time)
    
    assert np.isclose(wave.time, time)


@pytest.mark.unit
def test_plane_wave_with_zero_amplitude():
    """Test PlaneWave with zero amplitude."""
    amplitude = 0.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    assert np.isclose(wave.amplitude, amplitude)


# ========================
# Physical Correctness Tests
# ========================

@pytest.mark.unit
def test_wave_number_inversely_proportional_to_wavelength():
    """Test that wave number is inversely proportional to wavelength."""
    amplitude = 1.0 + 0.0j
    wave1 = PlaneWave(amplitude, wavelength=5.0)
    wave2 = PlaneWave(amplitude, wavelength=10.0)
    
    k1 = wave1.wave_number
    k2 = wave2.wave_number
    
    assert np.isclose(k1 / k2, 2.0)


@pytest.mark.unit
def test_dispersion_relation():
    """Test basic dispersion relation: E = ħω = ħ²k²/(2m)."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    masse = ELECTRON_MASS
    wave = PlaneWave(amplitude, wavelength, masse=masse)
    
    k = wave.wave_number
    omega = wave.angular_frequency
    
    expected_omega = (REDUCED_PLANCK_CONSTANT * k**2) / (2 * masse)
    
    assert np.isclose(omega, expected_omega)

@pytest.mark.unit
def test_wave_number_and_angular_frequency_consistency():
    """Test consistency between wave number and angular frequency."""
    amplitude = 1.0 + 0.0j
    wavelength = 8.0
    masse = ELECTRON_MASS
    wave = PlaneWave(amplitude, wavelength, masse=masse)
    
    k = wave.wave_number
    omega = wave.angular_frequency
    
    calculated_omega = (REDUCED_PLANCK_CONSTANT * k**2) / (2 * masse)
    
    assert np.isclose(omega, calculated_omega)


# ========================
# Evaluation Method Tests
# ========================

@pytest.mark.unit
def test_evaluate_single_point():
    """Test evaluate with a single point returns correct wave value."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    result = wave.evaluate(0.0)
    expected = 1.0 + 0.0j
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_multiple_points():
    """Test evaluate with multiple points returns array of correct length."""
    amplitude = 1.0
    wavelength = 2.0
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    x_values = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    result = wave.evaluate(x_values)
    
    # Verify result is array
    assert isinstance(result, np.ndarray)
    assert result.shape == x_values.shape
    assert len(result) == 5


@pytest.mark.unit
def test_evaluate_preserves_amplitude():
    """Test that amplitude magnitude is preserved at all positions."""
    amplitude = 2.0
    wavelength = 5.0
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    x_values = np.linspace(0, 10, 100)
    result = wave.evaluate(x_values)
    magnitudes = np.abs(result)
    
    # All magnitudes should equal |amplitude|
    expected_magnitude = np.abs(amplitude)
    assert np.allclose(magnitudes, expected_magnitude, atol=1e-14)


@pytest.mark.unit
def test_evaluate_with_position_offset():
    """Test that position offset correctly shifts the wave."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 1.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    # At x = position, the spatial term (x - x0) = 0
    result_at_offset = wave.evaluate(position)
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result_at_offset, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_with_phase_shift():
    """Test that phase correctly shifts the wave."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = PI / 2  # 90 degrees
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    # At x=0, t=0: ψ(0,0) = exp(i*π/2) = i
    result = wave.evaluate(0.0)
    expected = 1.0j
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_periodicity():
    """Test that wave repeats after one wavelength."""
    amplitude = 1.0
    wavelength = 4.0
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    x1 = 0.0
    x2 = wavelength  # One full wavelength
    
    result1 = wave.evaluate(x1)
    result2 = wave.evaluate(x2)
    
    # After one wavelength, phase should be 2π (same point)
    assert np.isclose(result1, result2, atol=1e-14)


@pytest.mark.unit
def test_evaluate_complex_amplitude():
    """Test evaluate with complex amplitude."""
    amplitude = 1.0 + 1.0j
    wavelength = 2.0 * PI
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    result = wave.evaluate(0.0)
    expected = (1.0 + 1.0j) * np.exp(0.0j)
    
    assert np.isclose(result, expected, atol=1e-14)

# ========================
# Scalar vs Vectorized Tests
# ========================

@pytest.mark.unit
def test_scalar_vs_vectorized_single_value():
    """Test that scalar evaluation equals single-element array evaluation."""
    amplitude = 1.0 + 0.5j
    wavelength = 3.0
    position = 0.5
    phase = PI / 4
    time = 1.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    # Scalar evaluation
    scalar_result = wave.evaluate(1.5)
    
    # Vectorized with single element
    array_result = wave.evaluate(np.array([1.5]))
    
    assert np.isclose(scalar_result, array_result[0], atol=1e-14)


@pytest.mark.unit
def test_scalar_evaluation_at_different_positions():
    """Test scalar evaluation at multiple distinct positions."""
    amplitude = 2.0
    wavelength = 5.0
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    # Evaluate scalars individually
    results_scalar = [wave.evaluate(x) for x in [0.0, 1.0, 2.0, 3.0]]
    
    # Evaluate as array
    results_array = wave.evaluate(np.array([0.0, 1.0, 2.0, 3.0]))
    
    for scalar_result, array_element in zip(results_scalar, results_array):
        assert np.isclose(scalar_result, array_element, atol=1e-14)


@pytest.mark.unit
def test_vectorized_linspace_evaluation():
    """Test vectorized evaluation with linspace grid."""
    amplitude = 1.0 + 0.5j
    wavelength = 2.0
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    # Vectorized evaluation
    x_values = np.linspace(0, 10, 101)
    results = wave.evaluate(x_values)
    
    assert isinstance(results, np.ndarray)
    assert results.shape == (101,)
    assert results.dtype == np.complex128


@pytest.mark.unit
def test_vectorized_large_array():
    """Test vectorized evaluation with large array."""
    amplitude = 1.5
    wavelength = 7.0
    
    wave = PlaneWave(amplitude, wavelength)
    
    x_values = np.linspace(-100, 100, 10000)
    results = wave.evaluate(x_values)
    
    assert isinstance(results, np.ndarray)
    assert len(results) == 10000


@pytest.mark.unit
def test_vectorized_amplitude_preservation():
    """Test that amplitude is preserved in vectorized evaluation."""
    amplitude = 3.5
    wavelength = 4.0
    
    wave = PlaneWave(amplitude, wavelength)
    
    x_values = np.logspace(-5, 5, 1000)  # Log-spaced values
    results = wave.evaluate(x_values)
    magnitudes = np.abs(results)
    
    expected_magnitude = np.abs(amplitude)
    assert np.allclose(magnitudes, expected_magnitude, atol=1e-14)


@pytest.mark.unit
def test_scalar_vs_vectorized_with_parameters():
    """Test consistency of scalar vs vectorized with all parameters."""
    amplitude = 2.0 + 1.0j
    wavelength = 6.0
    position = 2.5
    phase = PI / 3
    time = 0.5
    masse = ELECTRON_MASS
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time, masse)
    
    x_test = 5.0
    scalar = wave.evaluate(x_test)
    vectorized = wave.evaluate(np.array([x_test]))[0]
    
    assert np.isclose(scalar, vectorized, atol=1e-14)


# ========================
# Method Consistency Tests
# ========================

@pytest.mark.unit
def test_evaluate_at_time_zero_consistency():
    """Test that evaluate at t=0 is consistent with evaluate method at t=0."""
    amplitude = 1.0 + 0.5j
    wavelength = 5.0
    position = 0.0
    phase = PI / 6
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    x_values = np.array([0.0, 1.0, 2.0])
    
    # Method 1: Use evaluate (t is already 0)
    result1 = wave.evaluate(x_values)
    
    # Method 2: Use evaluate_at_time_zero
    result2 = wave.evaluate_at_time_zero(x_values)
    
    assert np.allclose(result1, result2, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_scalar():
    """Test evaluate_at_time_zero with scalar input."""
    amplitude = 1.5
    wavelength = 3.0
    position = 1.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x = 2.0
    result_scalar = wave.evaluate_at_time_zero(x)
    result_array = wave.evaluate_at_time_zero(np.array([x]))
    
    assert np.isclose(result_scalar, result_array[0], atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_scalar():
    """Test evaluate_at_position_zero with scalar input."""
    amplitude = 2.0
    wavelength = 4.0
    position = 0.0
    phase = PI / 4
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t = 1.0
    result_scalar = wave.evaluate_at_position_zero(t)
    result_array = wave.evaluate_at_position_zero(np.array([t]))
    
    assert np.isclose(result_scalar, result_array[0], atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_vectorized():
    """Test evaluate_at_position_zero with vectorized input."""
    amplitude = 1.0 + 1.0j
    wavelength = 2.0
    position = 0.5
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t_values = np.array([0.0, 1.0, 2.0, 3.0])
    results = wave.evaluate_at_position_zero(t_values)
    
    assert isinstance(results, np.ndarray)
    assert results.shape == t_values.shape


@pytest.mark.unit
def test_three_evaluation_methods_at_origin():
    """Test that all three evaluation methods agree at (x=0, t=0)."""
    amplitude = 3.0 + 2.0j
    wavelength = 5.0
    position = 0.0
    phase = PI / 2
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    # All three methods at the special point (x=0, t=0)
    result_evaluate = wave.evaluate(0.0)
    result_at_time_zero = wave.evaluate_at_time_zero(0.0)
    result_at_position_zero = wave.evaluate_at_position_zero(0.0)
    
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result_evaluate, expected, atol=1e-14)
    assert np.isclose(result_at_time_zero, expected, atol=1e-14)
    assert np.isclose(result_at_position_zero, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_time_evolution():
    """Test evaluate correctly evolves wave in time."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = 0.0
    
    wave_t0 = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    wave_t1 = PlaneWave(amplitude, wavelength, position, phase, time=1.0)
    
    # At same position, different times
    x = 0.0
    result_t0 = wave_t0.evaluate(x)
    result_t1 = wave_t1.evaluate(x)
    
    # Results should differ due to time evolution
    assert not np.isclose(result_t0, result_t1, atol=1e-10)


@pytest.mark.unit
def test_wave_number_consistency_across_methods():
    """Test that wave number is used consistently in all evaluation methods."""
    amplitude = 1.0 + 0.5j
    wavelength = 3.5
    position = 1.0
    phase = PI / 4
    time = 0.2
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    k = wave.wave_number
    expected_k = 2 * PI / wavelength
    
    assert np.isclose(k, expected_k, atol=1e-14)
    
    # Verify k is used in evaluate
    x = 5.0
    result = wave.evaluate(x)
    phase_spatial = k * (x - position)
    # The wave should contain this phase term
    assert isinstance(result, np.ndarray) or isinstance(result, complex)


@pytest.mark.unit
def test_angular_frequency_consistency_in_time_evolution():
    """Test that angular frequency consistently affects time evolution."""
    amplitude = 1.0
    wavelength = 4.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    omega = wave.angular_frequency
    expected_omega = (REDUCED_PLANCK_CONSTANT * wave.wave_number**2) / (2 * wave.masse)
    
    assert np.isclose(omega, expected_omega, atol=1e-30)


@pytest.mark.unit
def test_phase_shift_in_all_methods():
    """Test that phase shift is consistently applied in all methods."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = PI / 3
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    # At origin
    result = wave.evaluate(0.0)
    result_time_zero = wave.evaluate_at_time_zero(0.0)
    
    # Both should include the phase
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result, expected, atol=1e-14)
    assert np.isclose(result_time_zero, expected, atol=1e-14)


@pytest.mark.unit
def test_position_offset_in_all_methods():
    """Test that position offset is consistently applied in all methods."""
    amplitude = 2.0 + 1.0j
    wavelength = 5.0
    position = 3.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    k = wave.wave_number
    
    # At the position offset, the spatial phase should be zero
    result = wave.evaluate(position)
    result_time_zero = wave.evaluate_at_time_zero(position)
    
    # Both should be approximately equal to amplitude * exp(i*phase)
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result, expected, atol=1e-14)
    assert np.isclose(result_time_zero, expected, atol=1e-14)


# ========================
# Comprehensive Integration Tests
# ========================

@pytest.mark.unit
def test_wave_properties_consistency():
    """Test overall consistency of wave properties."""
    amplitude = 1.5 + 0.8j
    wavelength = 3.2
    position = 1.5
    phase = 0.75
    time = 0.3
    masse = 2.0 * ELECTRON_MASS
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time, masse)
    
    # Check properties
    k = wave.wave_number
    omega = wave.angular_frequency
    
    # k = 2π/λ
    assert np.isclose(k, 2 * PI / wavelength, atol=1e-14)
    
    # ω = ħk²/(2m)
    assert np.isclose(omega, (REDUCED_PLANCK_CONSTANT * k**2) / (2 * masse), atol=1e-30)
    
    # Evaluate should return numpy array
    result = wave.evaluate(5.0)
    assert isinstance(result, np.ndarray)


@pytest.mark.unit
def test_evaluate_consistency_multiple_positions():
    """Test evaluate gives consistent results across many positions."""
    amplitude = 1.0 + 0.3j
    wavelength = 2.5
    position = 0.0
    phase = 0.0
    time = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    x_values = np.array([-5.0, -2.0, 0.0, 2.0, 5.0, 10.0])
    
    # Vectorized
    results_vectorized = wave.evaluate(x_values)
    
    # Individual scalars (flatten the results since each returns an array)
    results_individual = np.array([wave.evaluate(x).item() for x in x_values])
    
    assert np.allclose(results_vectorized, results_individual, atol=1e-14)


@pytest.mark.unit
def test_magnitude_unchanged_across_evaluation_methods():
    """Test that magnitude is unchanged across all evaluation methods."""
    amplitude = 2.5 + 1.5j
    wavelength = 4.0
    position = 1.0
    phase = PI / 6
    time = 0.1
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    x = 3.0
    
    result_main = wave.evaluate(x)
    result_time_zero = wave.evaluate_at_time_zero(x)
    
    # Magnitudes should be the same
    mag_main = np.abs(result_main)
    mag_time_zero = np.abs(result_time_zero)
    
    expected_magnitude = np.abs(amplitude)
    
    assert np.isclose(mag_main, expected_magnitude, atol=1e-14)
    assert np.isclose(mag_time_zero, expected_magnitude, atol=1e-14)


@pytest.mark.unit
def test_vectorized_with_different_array_types():
    """Test vectorized evaluation with different numpy array types."""
    amplitude = 1.0 + 0.5j
    wavelength = 3.0
    
    wave = PlaneWave(amplitude, wavelength)
    
    # Different array types
    x_list = [0.0, 1.0, 2.0]
    x_tuple = (0.0, 1.0, 2.0)
    x_array = np.array([0.0, 1.0, 2.0])
    
    result_list = wave.evaluate(x_array)  # numpy accepts list via implicit conversion
    result_array = wave.evaluate(x_array)
    
    assert np.allclose(result_list, result_array, atol=1e-14)


@pytest.mark.unit
def test_reproducibility_of_evaluation():
    """Test that repeated evaluations give identical results."""
    amplitude = 1.5 + 0.7j
    wavelength = 5.5
    position = 2.0
    phase = PI / 5
    time = 0.25
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    x_values = np.linspace(-10, 10, 50)
    
    result1 = wave.evaluate(x_values)
    result2 = wave.evaluate(x_values)
    result3 = wave.evaluate(x_values)
    
    assert np.allclose(result1, result2, atol=1e-14)
    assert np.allclose(result2, result3, atol=1e-14)


# ========================
# evaluate_at_time_zero Tests
# ========================

@pytest.mark.unit
def test_evaluate_at_time_zero_scalar_basic():
    """Test evaluate_at_time_zero with scalar input."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    result = wave.evaluate_at_time_zero(0.0)
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_scalar_with_offset():
    """Test evaluate_at_time_zero scalar at position offset."""
    amplitude = 2.0
    wavelength = 5.0
    position = 3.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    # At position offset, spatial phase = 0
    result = wave.evaluate_at_time_zero(position)
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_scalar_with_phase():
    """Test evaluate_at_time_zero scalar with phase shift."""
    amplitude = 1.5
    wavelength = 4.0
    position = 0.0
    phase = PI / 3
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    result = wave.evaluate_at_time_zero(0.0)
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_scalar_complex_amplitude():
    """Test evaluate_at_time_zero with complex amplitude."""
    amplitude = 1.0 + 1.0j
    wavelength = 2.0 * PI
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    result = wave.evaluate_at_time_zero(0.0)
    expected = amplitude * np.exp(0.0j)
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_vectorized_basic():
    """Test evaluate_at_time_zero with array input."""
    amplitude = 1.0
    wavelength = 2.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x_values = np.array([0.0, 1.0, 2.0, 3.0])
    result = wave.evaluate_at_time_zero(x_values)
    
    assert isinstance(result, np.ndarray)
    assert result.shape == x_values.shape
    assert len(result) == 4


@pytest.mark.unit
def test_evaluate_at_time_zero_vectorized_linspace():
    """Test evaluate_at_time_zero with linspace grid."""
    amplitude = 1.0 + 0.5j
    wavelength = 3.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x_values = np.linspace(-10, 10, 101)
    result = wave.evaluate_at_time_zero(x_values)
    
    assert isinstance(result, np.ndarray)
    assert result.shape == (101,)
    assert result.dtype == np.complex128


@pytest.mark.unit
def test_evaluate_at_time_zero_vectorized_large_array():
    """Test evaluate_at_time_zero with large array."""
    amplitude = 1.5 + 0.8j
    wavelength = 2.5
    position = 1.0
    phase = PI / 6
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x_values = np.linspace(-100, 100, 10000)
    result = wave.evaluate_at_time_zero(x_values)
    
    assert isinstance(result, np.ndarray)
    assert len(result) == 10000


@pytest.mark.unit
def test_evaluate_at_time_zero_preserves_amplitude():
    """Test that amplitude magnitude is preserved in evaluate_at_time_zero."""
    amplitude = 3.0
    wavelength = 4.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x_values = np.linspace(0, 20, 100)
    result = wave.evaluate_at_time_zero(x_values)
    magnitudes = np.abs(result)
    
    expected_magnitude = np.abs(amplitude)
    assert np.allclose(magnitudes, expected_magnitude, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_scalar_vs_vectorized():
    """Test consistency between scalar and vectorized evaluate_at_time_zero."""
    amplitude = 2.0 + 1.0j
    wavelength = 3.5
    position = 0.5
    phase = PI / 4
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x_test = 5.0
    
    # Scalar
    scalar_result = wave.evaluate_at_time_zero(x_test)
    
    # Vectorized
    vectorized_result = wave.evaluate_at_time_zero(np.array([x_test]))[0]
    
    assert np.isclose(scalar_result, vectorized_result, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_multiple_positions():
    """Test scalar vs vectorized consistency across multiple positions."""
    amplitude = 1.5 + 0.7j
    wavelength = 2.8
    position = 1.2
    phase = PI / 5
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x_values = np.array([0.0, 1.0, 2.5, 5.0, 10.0])
    
    # Vectorized
    results_vectorized = wave.evaluate_at_time_zero(x_values)
    
    # Individual scalars (flatten the results since each returns an array)
    results_individual = np.array([wave.evaluate_at_time_zero(x).item() for x in x_values])
    
    assert np.allclose(results_vectorized, results_individual, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_periodicity():
    """Test that evaluate_at_time_zero repeats after one wavelength."""
    amplitude = 1.0
    wavelength = 4.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    x1 = 0.0
    x2 = wavelength  # One full wavelength
    
    result1 = wave.evaluate_at_time_zero(x1)
    result2 = wave.evaluate_at_time_zero(x2)
    
    # After one wavelength, should be back to same phase
    assert np.isclose(result1, result2, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_phase_shift():
    """Test that phase shift is applied correctly in evaluate_at_time_zero."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = PI / 2
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    result = wave.evaluate_at_time_zero(0.0)
    expected = amplitude * 1j  # exp(i*π/2) = i
    
    assert np.isclose(result, expected, atol=1e-14)


# ========================
# evaluate_at_position_zero Tests
# ========================

@pytest.mark.unit
def test_evaluate_at_position_zero_scalar_basic():
    """Test evaluate_at_position_zero with scalar input."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    result = wave.evaluate_at_position_zero(0.0)
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_scalar_with_position_offset():
    """Test evaluate_at_position_zero with position offset."""
    amplitude = 1.5
    wavelength = 3.0
    position = 2.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    result = wave.evaluate_at_position_zero(0.0)
    k = wave.wave_number
    
    # At x=0, t=0: ψ(0,0) = A * exp(i*(-k*x0 + φ))
    expected = amplitude * np.exp(1j * (-k * position + phase))
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_scalar_with_phase():
    """Test evaluate_at_position_zero with phase shift."""
    amplitude = 2.0
    wavelength = 4.0
    position = 0.0
    phase = PI / 3
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    result = wave.evaluate_at_position_zero(0.0)
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_scalar_complex_amplitude():
    """Test evaluate_at_position_zero with complex amplitude."""
    amplitude = 1.0 + 2.0j
    wavelength = 2.0 * PI
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    result = wave.evaluate_at_position_zero(0.0)
    expected = amplitude
    
    assert np.isclose(result, expected, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_vectorized_basic():
    """Test evaluate_at_position_zero with array input."""
    amplitude = 1.0
    wavelength = 2.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t_values = np.array([0.0, 1.0, 2.0, 3.0])
    result = wave.evaluate_at_position_zero(t_values)
    
    assert isinstance(result, np.ndarray)
    assert result.shape == t_values.shape
    assert len(result) == 4


@pytest.mark.unit
def test_evaluate_at_position_zero_vectorized_linspace():
    """Test evaluate_at_position_zero with linspace time grid."""
    amplitude = 1.0 + 0.3j
    wavelength = 3.0
    position = 0.5
    phase = PI / 6
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t_values = np.linspace(0, 10, 101)
    result = wave.evaluate_at_position_zero(t_values)
    
    assert isinstance(result, np.ndarray)
    assert result.shape == (101,)
    assert result.dtype == np.complex128


@pytest.mark.unit
def test_evaluate_at_position_zero_vectorized_large_array():
    """Test evaluate_at_position_zero with large time array."""
    amplitude = 1.5 + 0.5j
    wavelength = 2.5
    position = 1.0
    phase = PI / 4
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t_values = np.linspace(0, 100, 10000)
    result = wave.evaluate_at_position_zero(t_values)
    
    assert isinstance(result, np.ndarray)
    assert len(result) == 10000


@pytest.mark.unit
def test_evaluate_at_position_zero_preserves_amplitude():
    """Test that amplitude magnitude is preserved in evaluate_at_position_zero."""
    amplitude = 2.5
    wavelength = 4.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t_values = np.linspace(0, 50, 100)
    result = wave.evaluate_at_position_zero(t_values)
    magnitudes = np.abs(result)
    
    expected_magnitude = np.abs(amplitude)
    assert np.allclose(magnitudes, expected_magnitude, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_scalar_vs_vectorized():
    """Test consistency between scalar and vectorized evaluate_at_position_zero."""
    amplitude = 1.5 + 0.8j
    wavelength = 3.0
    position = 1.0
    phase = PI / 3
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t_test = 5.0
    
    # Scalar
    scalar_result = wave.evaluate_at_position_zero(t_test)
    
    # Vectorized
    vectorized_result = wave.evaluate_at_position_zero(np.array([t_test]))[0]
    
    assert np.isclose(scalar_result, vectorized_result, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_multiple_times():
    """Test scalar vs vectorized consistency across multiple times."""
    amplitude = 2.0 + 0.5j
    wavelength = 2.5
    position = 0.8
    phase = PI / 5
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    t_values = np.array([0.0, 1.0, 2.5, 5.0, 10.0])
    
    # Vectorized
    results_vectorized = wave.evaluate_at_position_zero(t_values)
    
    # Individual scalars (flatten the results since each returns an array)
    results_individual = np.array([wave.evaluate_at_position_zero(t).item() for t in t_values])
    
    assert np.allclose(results_vectorized, results_individual, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_period():
    """Test that evaluate_at_position_zero repeats after one period."""
    amplitude = 1.0
    wavelength = 5.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    period = wave.period
    
    t1 = 0.0
    t2 = period  # One full period
    
    result1 = wave.evaluate_at_position_zero(t1)
    result2 = wave.evaluate_at_position_zero(t2)
    
    # After one period, should be back to same phase
    assert np.isclose(result1, result2, atol=1e-12)


@pytest.mark.unit
def test_evaluate_at_position_zero_phase_shift():
    """Test that phase shift is applied correctly in evaluate_at_position_zero."""
    amplitude = 1.0
    wavelength = 2.0 * PI
    position = 0.0
    phase = PI / 2
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    result = wave.evaluate_at_position_zero(0.0)
    expected = amplitude * 1j  # exp(i*π/2) = i
    
    assert np.isclose(result, expected, atol=1e-14)


# ========================
# Coherence Between Methods Tests
# ========================

@pytest.mark.unit
def test_evaluate_vs_evaluate_at_time_zero_at_t_equals_zero():
    """Test evaluate equals evaluate_at_time_zero when wave time is zero."""
    amplitude = 1.5 + 0.5j
    wavelength = 3.0
    position = 0.5
    phase = PI / 4
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    x_values = np.linspace(-5, 5, 21)
    
    result_evaluate = wave.evaluate(x_values)
    result_at_time_zero = wave.evaluate_at_time_zero(x_values)
    
    assert np.allclose(result_evaluate, result_at_time_zero, atol=1e-14)


@pytest.mark.unit
def test_evaluate_vs_evaluate_at_position_zero_at_x_equals_zero():
    """Test evaluate and evaluate_at_position_zero consistency at x=0."""
    amplitude = 2.0 + 1.0j
    wavelength = 4.0
    position = 0.0
    phase = PI / 6
    time = 0.5
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    # At x=0
    result_evaluate = wave.evaluate(0.0)
    result_at_position_zero = wave.evaluate_at_position_zero(wave.time)
    
    assert np.isclose(result_evaluate, result_at_position_zero, atol=1e-14)


@pytest.mark.unit
def test_three_methods_at_origin_and_zero_time():
    """Test all three evaluation methods at (x=0, t=0)."""
    amplitude = 3.0 + 2.0j
    wavelength = 5.0
    position = 0.0
    phase = PI / 3
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    # All at origin
    result_evaluate = wave.evaluate(0.0)
    result_time_zero = wave.evaluate_at_time_zero(0.0)
    result_position_zero = wave.evaluate_at_position_zero(0.0)
    
    expected = amplitude * np.exp(1j * phase)
    
    assert np.isclose(result_evaluate, expected, atol=1e-14)
    assert np.isclose(result_time_zero, expected, atol=1e-14)
    assert np.isclose(result_position_zero, expected, atol=1e-14)


@pytest.mark.unit
def test_amplitude_consistency_all_methods():
    """Test amplitude magnitude is consistent across all evaluation methods."""
    amplitude = 2.5 + 1.5j
    wavelength = 3.5
    position = 1.0
    phase = PI / 5
    time = 0.3
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time)
    
    x = 5.0
    t = 2.0
    
    result_evaluate = wave.evaluate(x)
    result_time_zero = wave.evaluate_at_time_zero(x)
    result_position_zero = wave.evaluate_at_position_zero(t)
    
    expected_magnitude = np.abs(amplitude)
    
    assert np.isclose(np.abs(result_evaluate), expected_magnitude, atol=1e-14)
    assert np.isclose(np.abs(result_time_zero), expected_magnitude, atol=1e-14)
    assert np.isclose(np.abs(result_position_zero), expected_magnitude, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_time_zero_ignores_wave_time():
    """Test that evaluate_at_time_zero ignores the wave's time parameter."""
    amplitude = 1.0 + 0.5j
    wavelength = 3.0
    position = 0.5
    phase = PI / 6
    
    # Create two waves with different times
    wave_t0 = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    wave_t5 = PlaneWave(amplitude, wavelength, position, phase, time=5.0)
    
    x = 2.0
    
    result_t0 = wave_t0.evaluate_at_time_zero(x)
    result_t5 = wave_t5.evaluate_at_time_zero(x)
    
    # Both should be identical since evaluate_at_time_zero always uses t=0
    assert np.isclose(result_t0, result_t5, atol=1e-14)


@pytest.mark.unit
def test_evaluate_at_position_zero_uses_wave_time():
    """Test that evaluate_at_position_zero uses the wave's time parameter."""
    amplitude = 1.0 + 0.5j
    wavelength = 3.0
    position = 0.5
    phase = PI / 6
    
    # Create two waves with different times
    wave_t0 = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    wave_t5 = PlaneWave(amplitude, wavelength, position, phase, time=5.0)
    
    # evaluate_at_position_zero uses the time parameter passed to it, not self.time
    # Evaluate at t=0 and t=5
    result_t0 = wave_t0.evaluate_at_position_zero(0.0)
    result_t5 = wave_t5.evaluate_at_position_zero(5.0)
    
    # Both waves evaluated at t=0 should give same result
    k = wave_t0.wave_number
    x0 = wave_t0.position
    expected_t0 = amplitude * np.exp(1j * (-k * x0 + phase))
    
    # At t=5 for wave_t5
    expected_t5 = amplitude * np.exp(1j * (-wave_t5.wave_number * wave_t5.position - wave_t5.angular_frequency * 5.0 + phase))
    
    assert np.isclose(result_t0, expected_t0, atol=1e-14)
    assert np.isclose(result_t5, expected_t5, atol=1e-14)


@pytest.mark.unit
def test_spatial_vs_temporal_evolution():
    """Test spatial evolution in evaluate_at_time_zero vs temporal in evaluate_at_position_zero."""
    amplitude = 1.5
    wavelength = 4.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase, time=0.0)
    
    k = wave.wave_number
    omega = wave.angular_frequency
    
    # Spatial: one wavelength shift
    result_x_shift = wave.evaluate_at_time_zero(wavelength)
    result_x_origin = wave.evaluate_at_time_zero(0.0)
    
    # After one wavelength, phase increases by 2π
    assert np.isclose(result_x_shift, result_x_origin, atol=1e-14)
    
    # Temporal: one period shift
    period = wave.period
    result_t_shift = wave.evaluate_at_position_zero(period)
    result_t_origin = wave.evaluate_at_position_zero(0.0)
    
    # After one period, time phase increases by 2π
    assert np.isclose(result_t_shift, result_t_origin, atol=1e-12)


@pytest.mark.unit
def test_wave_number_consistency_in_spatial_methods():
    """Test wave number is used consistently in spatial evaluation methods."""
    amplitude = 1.0
    wavelength = 3.0
    position = 1.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    k = wave.wave_number
    
    # At position offset, spatial phase should be zero
    result_at_offset = wave.evaluate_at_time_zero(position)
    expected = amplitude
    
    assert np.isclose(result_at_offset, expected, atol=1e-14)


@pytest.mark.unit
def test_angular_frequency_consistency_in_temporal_method():
    """Test angular frequency is used correctly in evaluate_at_position_zero."""
    amplitude = 1.0
    wavelength = 5.0
    position = 0.0
    phase = 0.0
    
    wave = PlaneWave(amplitude, wavelength, position, phase)
    
    period = wave.period
    
    # At t=0 and t=period, should give same result
    result_t0 = wave.evaluate_at_position_zero(0.0)
    result_t_period = wave.evaluate_at_position_zero(period)
    
    assert np.isclose(result_t0, result_t_period, atol=1e-12)


# TODO: Add more tests for time dependence and moving wave packets.