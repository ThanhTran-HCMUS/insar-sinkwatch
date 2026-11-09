"""
AI & Automated Change Detection Engine for SAR Data
Implements:
- Multi-temporal Log-Ratio Difference Analysis: Delta_sigma0 = I_post_dB - I_pre_dB
- Pure-NumPy Adaptive Otsu Thresholding for automated water mask segmentation
- Inundation Classification:
    * 0: Stable Land / Dry Vegetation
    * 1: Permanent Water (Pre-existing river/canal)
    * 2: Newly Inundated Flood Water (Disaster extent)
    * 3: Flooded Vegetation (NISAR L-band double-bounce signature)
"""

import numpy as np

def otsu_threshold(image_1d: np.ndarray, num_bins: int = 256) -> float:
    """
    Computes optimal threshold using Otsu's bimodal maximum variance criterion.
    Pure NumPy implementation without external OpenCV/scikit-image requirement.
    """
    valid_pixels = image_1d[np.isfinite(image_1d)]
    if len(valid_pixels) == 0:
        return 0.0
    
    min_val, max_val = np.min(valid_pixels), np.max(valid_pixels)
    if min_val == max_val:
        return float(min_val)
        
    counts, bin_edges = np.histogram(valid_pixels, bins=num_bins, range=(min_val, max_val))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    
    total = len(valid_pixels)
    weight1 = np.cumsum(counts) / total
    weight2 = 1.0 - weight1
    
    # Avoid zero division
    valid_idx = (weight1 > 0) & (weight2 > 0)
    if not np.any(valid_idx):
        return float(np.mean(valid_pixels))
        
    cumsum_val = np.cumsum(counts * bin_centers)
    mean1 = cumsum_val / (np.cumsum(counts) + 1e-10)
    mean2 = (cumsum_val[-1] - cumsum_val) / (total - np.cumsum(counts) + 1e-10)
    
    between_class_variance = weight1 * weight2 * ((mean1 - mean2) ** 2)
    between_class_variance[~valid_idx] = -1.0
    
    optimal_idx = np.argmax(between_class_variance)
    return float(bin_centers[optimal_idx])

def detect_surface_inundation(
    pre_sar_db: np.ndarray,
    post_sar_db: np.ndarray,
    water_threshold_db: float = -18.0,
    change_threshold_db: float = -3.5,
    auto_threshold: bool = True
) -> dict:
    """
    Multi-temporal SAR change detection and flood segmentation.
    
    Parameters:
    - pre_sar_db: Baseline radar image in dB scale.
    - post_sar_db: Post-event (disaster/flood) radar image in dB scale.
    - water_threshold_db: Backscatter cutoff for open water (typically -16 to -20 dB).
    - change_threshold_db: Backscatter drop threshold indicating new inundation (typically -3 to -5 dB).
    - auto_threshold: If True, uses Otsu adaptive algorithm to fine-tune water cutoff.
    
    Returns:
    - Dictionary with classification mask, change difference map, and statistics.
    """
    # 1. Backscatter difference in dB (equivalent to log-ratio in linear scale)
    delta_db = post_sar_db - pre_sar_db
    
    # 2. Automated adaptive thresholding if enabled
    computed_water_th = water_threshold_db
    if auto_threshold:
        # Detect water mode from the post-event image
        suggested_th = otsu_threshold(post_sar_db.flatten())
        # Constrain threshold to realistic physical SAR bounds for water (-24 dB to -14 dB)
        computed_water_th = float(np.clip(suggested_th, -24.0, -14.0))
    
    # 3. Identify Permanent Water vs. New Inundation
    # Permanent water: Low backscatter in both pre and post images
    permanent_water = (pre_sar_db < computed_water_th) & (post_sar_db < computed_water_th)
    
    # New flood water: Post backscatter is low, and experienced significant backscatter drop
    newly_flooded = (post_sar_db < computed_water_th) & (delta_db < change_threshold_db) & (~permanent_water)
    
    # Flooded vegetation (NISAR L-band signature):
    # In L-band, standing water beneath vegetation creates trunk-water corner reflectors (double bounce)
    # causing a marked INCREASE in backscatter (delta_db > +3 dB) in wetland areas
    flooded_vegetation = (delta_db > 3.0) & (pre_sar_db > -16.0) & (post_sar_db > -12.0)
    
    # 4. Composite Categorical Mask
    # 0 = Non-flooded land / dry vegetation
    # 1 = Permanent water bodies (pre-existing rivers/lakes)
    # 2 = Newly inundated open water (flood zones)
    # 3 = Flooded vegetation / saturated wetlands
    classification_mask = np.zeros(pre_sar_db.shape, dtype=np.uint8)
    classification_mask[permanent_water] = 1
    classification_mask[newly_flooded] = 2
    classification_mask[flooded_vegetation] = 3
    
    total_pixels = pre_sar_db.size
    new_flood_pixels = int(np.sum(classification_mask == 2))
    perm_water_pixels = int(np.sum(classification_mask == 1))
    flooded_veg_pixels = int(np.sum(classification_mask == 3))
    
    return {
        "classification_mask": classification_mask,
        "delta_db": delta_db,
        "water_threshold_db": computed_water_th,
        "change_threshold_db": change_threshold_db,
        "new_flood_pixels": new_flood_pixels,
        "permanent_water_pixels": perm_water_pixels,
        "flooded_vegetation_pixels": flooded_veg_pixels,
        "total_pixels": total_pixels
    }

