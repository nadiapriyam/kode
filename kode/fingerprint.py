import numpy as np


def radial_profile(kspace: np.ndarray) -> np.ndarray:
    """
    Compute the radial power profile of k-space (RSS across coils).

    Bins the 2D power spectrum by distance from center.
    Returns a 1D array — the k-space "fingerprint" curve.
    """
    power = np.sum(np.abs(kspace) ** 2, axis=0)
    height, width = power.shape
    cy, cx = height // 2, width // 2
    y, x = np.ogrid[:height, :width]
    radius = np.sqrt((y - cy) ** 2 + (x - cx) ** 2).astype(int)

    max_r = min(cy, cx)
    profile = np.zeros(max_r)
    counts = np.zeros(max_r)

    for r in range(max_r):
        ring = power[radius == r]
        if len(ring) > 0:
            profile[r] = ring.mean()
            counts[r] = len(ring)

    return profile


def energy_ratio(kspace: np.ndarray, low_fraction: float = 0.1) -> float:
    """
    Ratio of low-frequency energy to total energy.

    High ratio = smooth / uniform tissue.
    Low ratio = high-frequency content (edges, fine structure, pathology).
    """
    power = np.sum(np.abs(kspace) ** 2, axis=0)
    height, width = power.shape
    cy, cx = height // 2, width // 2
    y, x = np.ogrid[:height, :width]
    dist = np.sqrt(((y - cy) / height) ** 2 + ((x - cx) / width) ** 2)

    low_mask = dist <= low_fraction
    return float(power[low_mask].sum() / power.sum())


def asymmetry_score(kspace: np.ndarray) -> float:
    """
    Measure left-right asymmetry in k-space power.

    Healthy brains are roughly symmetric. Asymmetry may indicate
    lesions, motion artifacts, or structural anomalies.
    """
    power = np.sum(np.abs(kspace) ** 2, axis=0)
    left = power[:, :power.shape[1] // 2]
    right = power[:, power.shape[1] // 2:]
    right_flipped = np.fliplr(right)
    min_w = min(left.shape[1], right_flipped.shape[1])
    diff = np.abs(left[:, :min_w] - right_flipped[:, :min_w])
    return float(diff.mean() / power.mean())
