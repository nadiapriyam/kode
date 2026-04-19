import h5py
import numpy as np


def load_kspace(filepath: str, slice_idx: int = 0) -> np.ndarray:
    """
    Load a single slice of raw k-space data from a fastMRI .h5 file.

    Returns a complex numpy array of shape (coils, height, width).
    """
    with h5py.File(filepath, 'r') as f:
        kspace = f['kspace'][slice_idx]  # shape: (coils, height, width, 2) or complex
        if kspace.dtype in [np.float32, np.float64]:
            kspace = kspace[..., 0] + 1j * kspace[..., 1]
    return kspace


def list_slices(filepath: str) -> int:
    """Return the number of slices in a fastMRI .h5 file."""
    with h5py.File(filepath, 'r') as f:
        return f['kspace'].shape[0]


def root_sum_of_squares(kspace: np.ndarray) -> np.ndarray:
    """
    Combine multi-coil k-space into a single image via RSS reconstruction.

    Applies IFFT per coil then combines with root-sum-of-squares.
    Returns a 2D float array (the reconstructed image).
    """
    images = np.fft.ifftshift(
        np.fft.ifft2(
            np.fft.ifftshift(kspace, axes=(-2, -1)),
            axes=(-2, -1)
        ),
        axes=(-2, -1)
    )
    return np.sqrt(np.sum(np.abs(images) ** 2, axis=0))
