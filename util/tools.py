import numpy as np
from numpy.typing import NDArray

# Custom packages
import params

# Find the highest peak value index.
def maxPeakIndex(data: NDArray) -> NDArray:
    """`maxPeakIndex` finds the highest (max height) intensity value index in the provided `data`."""

    return np.argmax(data[:, 1])

    # peakIntensity = max(list(data[:,1]))
    # peakPixel = np.where(data == peakIntensity)[0][0]

    # return peakPixel

# Converts width values to angle values.
def pixelToTheta(pixelValues: NDArray, peakPixel: float) -> NDArray:
    """`pixelToTheta` converts given values from `pixelValues` in pixels to values in theta."""
    
    thetaStep: float = np.arctan(params.pixelWidth / params.slitDistance)

    # Offset all pixels in the dataset by the peak
    offsetPixels: NDArray = pixelValues - peakPixel
    
    thetaValues: NDArray = offsetPixels * thetaStep
    
    return thetaValues