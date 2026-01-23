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
    calculated_k = plane_wave.wave_number()
    
    assert np.isclose(calculated_k, expected_k)


@pytest.mark.unit
def test_wave_number_relationship():
    """Test wave number relationship with wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 10.0
    wave = PlaneWave(amplitude, wavelength)
    
    k = wave.wave_number()

    assert np.isclose(k * wavelength, 2 * PI)


@pytest.mark.unit
def test_wave_number_different_wavelengths():
    """Test wave number for different wavelengths."""
    amplitude = 1.0 + 0.0j
    wavelengths = [1.0, 5.0, 10.0, 20.0]
    
    for wavelength in wavelengths:
        wave = PlaneWave(amplitude, wavelength)
        k = wave.wave_number()
        expected_k = 2 * PI / wavelength
        assert np.isclose(k, expected_k)


@pytest.mark.unit
def test_wave_number_positive():
    """Test that wave number is always positive for positive wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    k = wave.wave_number()
    assert k > 0


# ========================
# Angular Frequency Tests
# ========================

@pytest.mark.unit
def test_angular_frequency_calculation(plane_wave):
    """Test that angular frequency is calculated correctly: ω = ħk²/(2m)."""
    k = plane_wave.wave_number()
    expected_omega = (REDUCED_PLANCK_CONSTANT * k**2) / (2 * plane_wave.masse)
    calculated_omega = plane_wave.angular_frequency()
    
    assert np.isclose(calculated_omega, expected_omega)


@pytest.mark.unit
def test_angular_frequency_depends_on_wavelength():
    """Test that angular frequency depends on wavelength."""
    amplitude = 1.0 + 0.0j
    wave1 = PlaneWave(amplitude, wavelength=5.0)
    wave2 = PlaneWave(amplitude, wavelength=10.0)
    
    omega1 = wave1.angular_frequency()
    omega2 = wave2.angular_frequency()
    
    assert not np.isclose(omega1, omega2)


@pytest.mark.unit
def test_angular_frequency_depends_on_mass():
    """Test that angular frequency depends on particle mass."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    
    wave1 = PlaneWave(amplitude, wavelength, masse=ELECTRON_MASS)
    wave2 = PlaneWave(amplitude, wavelength, masse=2 * ELECTRON_MASS)
    
    omega1 = wave1.angular_frequency()
    omega2 = wave2.angular_frequency()
    
    assert np.isclose(omega2, omega1 / 2)


@pytest.mark.unit
def test_angular_frequency_proportional_to_k_squared():
    """Test that angular frequency is proportional to k²."""
    amplitude = 1.0 + 0.0j
    wave1 = PlaneWave(amplitude, wavelength=10.0)
    wave2 = PlaneWave(amplitude, wavelength=5.0)
    
    k1 = wave1.wave_number()
    k2 = wave2.wave_number()
    
    omega1 = wave1.angular_frequency()
    omega2 = wave2.angular_frequency()
    
    expected_ratio = (k2**2) / (k1**2)
    actual_ratio = omega2 / omega1
    
    assert np.isclose(actual_ratio, expected_ratio)


@pytest.mark.unit
def test_angular_frequency_positive():
    """Test that angular frequency is positive for positive mass and wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    omega = wave.angular_frequency()
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
    k = wave.wave_number()
    assert k > 0


@pytest.mark.unit
def test_plane_wave_with_very_large_wavelength():
    """Test PlaneWave with very large wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 1e10
    wave = PlaneWave(amplitude, wavelength)
    
    assert np.isclose(wave.wavelength, wavelength)
    k = wave.wave_number()
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
    
    k1 = wave1.wave_number()
    k2 = wave2.wave_number()
    
    assert np.isclose(k1 / k2, 2.0)


@pytest.mark.unit
def test_dispersion_relation():
    """Test basic dispersion relation: E = ħω = ħ²k²/(2m)."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    masse = ELECTRON_MASS
    wave = PlaneWave(amplitude, wavelength, masse=masse)
    
    k = wave.wave_number()
    omega = wave.angular_frequency()
    
    expected_omega = (REDUCED_PLANCK_CONSTANT * k**2) / (2 * masse)
    
    assert np.isclose(omega, expected_omega)

@pytest.mark.unit
def test_wave_number_and_angular_frequency_consistency():
    """Test consistency between wave number and angular frequency."""
    amplitude = 1.0 + 0.0j
    wavelength = 8.0
    masse = ELECTRON_MASS
    wave = PlaneWave(amplitude, wavelength, masse=masse)
    
    k = wave.wave_number()
    omega = wave.angular_frequency()
    
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

# TODO: Add more tests for time dependence and moving wave packets.