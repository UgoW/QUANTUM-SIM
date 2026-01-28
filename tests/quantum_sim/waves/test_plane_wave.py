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
# Momentum Tests
# ========================

@pytest.mark.unit
def test_momentum_calculation(plane_wave):
    """Test that momentum is calculated correctly: p = ħk."""
    k = plane_wave.wave_number
    expected_p = REDUCED_PLANCK_CONSTANT * k
    calculated_p = plane_wave.momentum
    
    assert np.isclose(calculated_p, expected_p)


@pytest.mark.unit
def test_momentum_positive():
    """Test that momentum is positive for positive wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    p = wave.momentum
    assert p > 0


# ========================
# Energy Tests
# ========================

@pytest.mark.unit
def test_energy_calculation(plane_wave):
    """Test that energy is calculated correctly: E = p²/(2m)."""
    p = plane_wave.momentum
    expected_e = p**2 / (2 * plane_wave.masse)
    calculated_e = plane_wave.energy
    
    assert np.isclose(calculated_e, expected_e)


@pytest.mark.unit
def test_energy_positive():
    """Test that energy is positive for non-zero wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    e = wave.energy
    assert e > 0


@pytest.mark.unit
def test_energy_increases_with_wavelength_decrease():
    """Test that energy increases when wavelength decreases."""
    amplitude = 1.0 + 0.0j
    wave1 = PlaneWave(amplitude, wavelength=10.0)
    wave2 = PlaneWave(amplitude, wavelength=5.0)
    
    assert wave2.energy > wave1.energy


# ========================
# Phase Velocity Tests
# ========================

@pytest.mark.unit
def test_phase_velocity_calculation(plane_wave):
    """Test that phase velocity is calculated correctly: v_p = ω/k."""
    k = plane_wave.wave_number
    omega = plane_wave.angular_frequency
    expected_vp = omega / k
    calculated_vp = plane_wave.phase_velocity
    
    assert np.isclose(calculated_vp, expected_vp)


@pytest.mark.unit
def test_phase_velocity_positive():
    """Test that phase velocity is positive."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    vp = wave.phase_velocity
    assert vp > 0


# ========================
# Period Tests
# ========================

@pytest.mark.unit
def test_period_calculation(plane_wave):
    """Test that period is calculated correctly: T = 2π/ω."""
    omega = plane_wave.angular_frequency
    expected_t = 2 * PI / omega
    calculated_t = plane_wave.period
    
    assert np.isclose(calculated_t, expected_t)


@pytest.mark.unit
def test_period_positive():
    """Test that period is positive for positive wavelength."""
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    wave = PlaneWave(amplitude, wavelength)
    
    t = wave.period
    assert t > 0


@pytest.mark.unit
def test_period_inversely_proportional_to_angular_frequency():
    """Test that period is inversely related to angular frequency."""
    amplitude = 1.0 + 0.0j
    wave1 = PlaneWave(amplitude, wavelength=5.0)
    wave2 = PlaneWave(amplitude, wavelength=10.0)
    
    period1 = wave1.period
    period2 = wave2.period
    omega1 = wave1.angular_frequency
    omega2 = wave2.angular_frequency
    
    # T1 * ω1 ≈ T2 * ω2 = 2π
    assert np.isclose(period1 * omega1, period2 * omega2)