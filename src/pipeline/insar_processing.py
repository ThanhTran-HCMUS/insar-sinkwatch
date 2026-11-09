"""
InSAR Processing Pipeline for NASA-ISRO NISAR Mission
Calculates interferometric phase difference and millimeter-scale surface displacement:
    Delta_d = (lambda / (4 * pi)) * Delta_phi
Where:
    - lambda = 24.24 cm (0.2424 m) for NISAR L-band SAR
    - Delta_phi = Interferometric phase difference (radians)
    - Delta_d = Line-of-sight surface displacement (meters / mm)
"""

import numpy as np

# NISAR L-band central wavelength in millimeters
NISAR_L_BAND_WAVELENGTH_MM = 242.4  # 24.24 cm

def generate_interferogram(slc_master: np.ndarray, slc_slave: np.ndarray) -> dict:
    """
    Forms complex interferogram: I = M * conj(S)
    Computes wrapped phase ([-pi, pi]) and spatial coherence (gamma).
    """
    complex_interferogram = slc_master * np.conj(slc_slave)
    wrapped_phase = np.angle(complex_interferogram)
    
    # Coherence calculation: gamma = |<M * S*>| / sqrt(<|M|^2> * <|S|^2>)
    abs_m = np.abs(slc_master)
    abs_s = np.abs(slc_slave)
    numerator = np.abs(complex_interferogram)
    denominator = np.sqrt(np.maximum(abs_m ** 2 * abs_s ** 2, 1e-10))
    coherence = np.clip(numerator / denominator, 0.0, 1.0)
    
    return {
        "complex": complex_interferogram,
        "wrapped_phase": wrapped_phase,
        "coherence": coherence
    }

def phase_to_displacement_mm(
    unwrapped_phase: np.ndarray,
    wavelength_mm: float = NISAR_L_BAND_WAVELENGTH_MM
) -> np.ndarray:
    """
    Converts unwrapped InSAR phase directly into Line-Of-Sight (LOS) 
    ground deformation in millimeters:
        displacement = (lambda / (4 * pi)) * unwrapped_phase
    Negative values indicate ground subsidence (sinking away from radar).
    Positive values indicate ground uplift (heaving).
    """
    displacement_mm = (wavelength_mm / (4.0 * np.pi)) * unwrapped_phase
    return displacement_mm

def goldstein_phase_filter(phase_field: np.ndarray, alpha: float = 0.5, window_size: int = 5) -> np.ndarray:
    """
    Goldstein InSAR phase filter for reducing decorrelation phase noise.
    Vectorized moving-window smoothing on real and imaginary phasor components.
    """
    cos_phase = np.cos(phase_field)
    sin_phase = np.sin(phase_field)
    
    pad_w = window_size // 2
    cos_pad = np.pad(cos_phase, pad_w, mode='reflect')
    sin_pad = np.pad(sin_phase, pad_w, mode='reflect')
    
    h, w = phase_field.shape
    # Fast 2D integral box smoothing
    int_cos = np.pad(cos_pad.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode='constant')
    int_sin = np.pad(sin_pad.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode='constant')
    
    r1 = np.arange(h)
    r2 = r1 + window_size
    c1 = np.arange(w)
    c2 = c1 + window_size
    
    R1, C1 = np.meshgrid(r1, c1, indexing='ij')
    R2, C2 = np.meshgrid(r2, c2, indexing='ij')
    
    N = window_size * window_size
    mean_cos = (int_cos[R2, C2] - int_cos[R1, C2] - int_cos[R2, C1] + int_cos[R1, C1]) / N
    mean_sin = (int_sin[R2, C2] - int_sin[R1, C2] - int_sin[R2, C1] + int_sin[R1, C1]) / N
    
    filtered_phase = np.arctan2(mean_sin, mean_cos)
    return filtered_phase

