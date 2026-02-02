import numpy as np


def trapz_norm_from_x(psi_x: np.ndarray, x: np.ndarray) -> float:
    """Compute normalization integral ∫|ψ(x)|^2 dx using trapezoidal rule.

    Returns the integral value (not the sqrt).
    """
    return float(np.trapz(np.abs(psi_x) ** 2, x))


def trapz_norm_from_k(phi_k: np.ndarray, k: np.ndarray) -> float:
    """Compute normalization integral ∫|φ(k)|^2 dk using trapezoidal rule.

    Returns the integral value (not the sqrt).
    """
    return float(np.trapz(np.abs(phi_k) ** 2, k))


def make_k_grid(k0: float = 0.0, sigma_k: float = 1.0, factor: float = 6.0, n_points: int = 2048) -> np.ndarray:
    """Create a symmetric k-grid around k0 spanning +/- factor * sigma_k."""
    k_max = abs(k0) + factor * max(1e-12, sigma_k)
    return np.linspace(k0 - k_max, k0 + k_max, n_points)
