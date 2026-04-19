import numpy as np
from .io import root_sum_of_squares


def apply_frequency_mask(kspace: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Apply a 2D binary mask to k-space before reconstruction."""
    return kspace * mask[np.newaxis, :, :]


def low_frequency_mask(height: int, width: int, fraction: float = 0.1) -> np.ndarray:
    """
    Mask that keeps only the center (low frequency) region of k-space.
    fraction=0.1 keeps the central 10% — coarse structure, no fine detail.
    """
    mask = np.zeros((height, width), dtype=np.float32)
    cy, cx = height // 2, width // 2
    ry, rx = int(height * fraction / 2), int(width * fraction / 2)
    mask[cy - ry:cy + ry, cx - rx:cx + rx] = 1.0
    return mask


def high_frequency_mask(height: int, width: int, fraction: float = 0.1) -> np.ndarray:
    """
    Mask that removes the center and keeps only high frequency edges.
    Highlights boundaries and fine structural detail.
    """
    return 1.0 - low_frequency_mask(height, width, fraction)


def band_mask(height: int, width: int, inner: float = 0.05, outer: float = 0.3) -> np.ndarray:
    """
    Annular band mask — keeps frequencies between inner and outer radii.
    Useful for isolating specific tissue frequency ranges.
    """
    mask = np.zeros((height, width), dtype=np.float32)
    cy, cx = height // 2, width // 2
    y, x = np.ogrid[:height, :width]
    dist = np.sqrt(((y - cy) / height) ** 2 + ((x - cx) / width) ** 2)
    mask[(dist >= inner) & (dist <= outer)] = 1.0
    return mask


def selective_reconstruct(kspace: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Apply a frequency mask and reconstruct to image space.
    Returns a 2D float image.
    """
    masked = apply_frequency_mask(kspace, mask)
    return root_sum_of_squares(masked)
