import numpy as np
from .selective_reconstruct import low_frequency_mask, selective_reconstruct


def progressive_frames(kspace: np.ndarray, steps: int = 8) -> list[np.ndarray]:
    """
    Generate a sequence of reconstructed images from low to full frequency.

    Each frame adds more k-space data — showing how detail builds from
    coarse structure to full resolution as frequency coverage increases.

    Returns a list of 2D float images, length = steps.
    """
    _, height, width = kspace.shape
    fractions = [i / steps for i in range(1, steps + 1)]
    frames = []
    for frac in fractions:
        mask = low_frequency_mask(height, width, fraction=frac)
        frame = selective_reconstruct(kspace, mask)
        frames.append(frame)
    return frames
