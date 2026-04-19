import numpy as np


def extract_motion_surrogate(kspace_timeseries: np.ndarray) -> np.ndarray:
    """
    Extract a motion surrogate signal from a time series of k-space frames.

    Uses the central k-space line (DC component) across time as a proxy
    for bulk motion — breathing, cardiac motion, or patient movement.

    kspace_timeseries: shape (time, coils, height, width)
    Returns: 1D float array of length time — the motion surrogate signal.
    """
    center_col = kspace_timeseries.shape[-1] // 2
    dc = kspace_timeseries[:, :, :, center_col]
    surrogate = np.abs(dc).mean(axis=(1, 2))
    return surrogate


def sort_by_motion_phase(
    kspace_timeseries: np.ndarray,
    n_phases: int = 4,
) -> list[np.ndarray]:
    """
    Sort k-space frames into motion phases using the motion surrogate.

    Returns n_phases groups of frames, ordered from minimum to maximum
    motion surrogate value (e.g. end-exhale to end-inhale).

    Each group is averaged and reconstructed to produce a pseudo-4D volume.
    """
    surrogate = extract_motion_surrogate(kspace_timeseries)
    sorted_indices = np.argsort(surrogate)
    splits = np.array_split(sorted_indices, n_phases)
    phases = []
    for idx_group in splits:
        frames = kspace_timeseries[idx_group]
        avg_kspace = frames.mean(axis=0)
        phases.append(avg_kspace)
    return phases
