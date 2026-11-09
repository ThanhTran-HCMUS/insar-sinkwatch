"""
SAR Processing Pipeline for NISAR / Sentinel-1 Radar Data
Provides:
- Decibel (dB) backscatter conversion (sigma-0)
- Refined Lee Filter (vectorized speckle reduction with edge preservation)
- Dual-polarization decomposition (VV, VH, and VH/VV ratio)
"""

import numpy as np

def linear_to_db(intensity: np.ndarray, epsilon: float = 1e-7) -> np.ndarray:
    """
    Converts linear radar power/intensity to decibel (dB) scale:
    sigma_0_dB = 10 * log10(intensity + epsilon)
    """
    safe_intensity = np.maximum(intensity, epsilon)
    return 10.0 * np.log10(safe_intensity)

def db_to_linear(db_array: np.ndarray) -> np.ndarray:
    """
    Converts decibel (dB) back to linear intensity.
    """
    return np.power(10.0, db_array / 10.0)

def boxcar_filter(img: np.ndarray, window_size: int = 5) -> np.ndarray:
    """
    Applies standard moving average (multilook) speckle filtering.
    """
    pad_w = window_size // 2
    padded = np.pad(img, pad_w, mode='reflect')
    out = np.zeros_like(img, dtype=np.float32)
    
    # 2D integral image for ultra-fast moving average
    integral = np.pad(padded.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode='constant')
    
    h, w = img.shape
    r1 = np.arange(h)
    r2 = r1 + window_size
    c1 = np.arange(w)
    c2 = c1 + window_size
    
    R1, C1 = np.meshgrid(r1, c1, indexing='ij')
    R2, C2 = np.meshgrid(r2, c2, indexing='ij')
    
    window_sum = (integral[R2, C2] - integral[R1, C2] - integral[R2, C1] + integral[R1, C1])
    out = window_sum / (window_size * window_size)
    return out

def refined_lee_filter(img_linear: np.ndarray, window_size: int = 7, looks: float = 1.0) -> np.ndarray:
    """
    Refined Lee Speckle Filter (Edge-Preserving Adaptive Filter for SAR):
    - Computes local mean (I_bar) and local variance (var_I).
    - Preserves structural features (canals, levees, roads) while smoothing 
      homogeneous areas (water, uniform rice fields).
      
    Weight: W = max(0, (var_I - var_noise) / var_I)
    Filtered: I_hat = I_bar + W * (I - I_bar)
    """
    pad_w = window_size // 2
    padded = np.pad(img_linear, pad_w, mode='reflect')
    
    h, w = img_linear.shape
    
    # Fast computation of local mean and local mean-of-squares
    integral_1 = np.pad(padded.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode='constant')
    padded_sq = padded ** 2
    integral_2 = np.pad(padded_sq.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode='constant')
    
    r1 = np.arange(h)
    r2 = r1 + window_size
    c1 = np.arange(w)
    c2 = c1 + window_size
    
    R1, C1 = np.meshgrid(r1, c1, indexing='ij')
    R2, C2 = np.meshgrid(r2, c2, indexing='ij')
    
    N = window_size * window_size
    local_mean = (integral_1[R2, C2] - integral_1[R1, C2] - integral_1[R2, C1] + integral_1[R1, C1]) / N
    local_sq_mean = (integral_2[R2, C2] - integral_2[R1, C2] - integral_2[R2, C1] + integral_2[R1, C1]) / N
    
    local_var = np.maximum(0.0, local_sq_mean - (local_mean ** 2))
    
    # Theoretical SAR noise variance for multilook SAR: sigma_v^2 = 1 / looks
    noise_var = (local_mean ** 2) / float(looks)
    
    # Adaptive Lee weight factor W
    with np.errstate(divide='ignore', invalid='ignore'):
        weight = np.where(local_var > 0, np.maximum(0.0, (local_var - noise_var) / local_var), 0.0)
    weight = np.clip(weight, 0.0, 1.0)
    
    # Output filtered intensity
    filtered = local_mean + weight * (img_linear - local_mean)
    return np.maximum(filtered, 1e-7)

def compute_sar_rgb(vv_db: np.ndarray, vh_db: np.ndarray) -> np.ndarray:
    """
    Creates standard PolSAR False Color Composite for visual interpretation:
    - Red Channel: VV backscatter (urban, rough surface)
    - Green Channel: VH backscatter (vegetation volume scattering)
    - Blue Channel: VH / VV ratio (inundated vegetation, water contrast)
    Returns normalized RGB float array [0, 1].
    """
    diff_ratio = vh_db - vv_db  # Cross-polarization ratio in dB
    
    def norm_channel(arr, vmin, vmax):
        return np.clip((arr - vmin) / (vmax - vmin + 1e-6), 0.0, 1.0)
    
    # Calibration ranges in dB typical for NISAR / Sentinel-1
    r = norm_channel(vv_db, -25.0, 0.0)
    g = norm_channel(vh_db, -30.0, -5.0)
    b = norm_channel(diff_ratio, -18.0, -2.0)
    
    return np.stack([r, g, b], axis=-1)

