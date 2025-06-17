import numpy as np
from numpy.typing import NDArray
from scipy.signal import find_peaks

# Custom packages
import params

# Find the highest peak value index.
def maxPeakIndex(data: NDArray) -> NDArray:
    """`maxPeakIndex` finds the highest (max height) intensity value index in the provided `data`."""

    return np.argmax(data[:, 1])

# Converts width values to angle values.
def pixelToTheta(pixelValues: NDArray, peakPixel: float) -> NDArray:
    """`pixelToTheta` converts given values from `pixelValues` in pixels to values in theta."""
    
    thetaStep: float = np.arctan(params.pixelWidth / params.slitDistance)

    # Offset all pixels in the dataset by the peak
    offsetPixels: NDArray = pixelValues - peakPixel
    
    thetaValues: NDArray = offsetPixels * thetaStep
    
    return thetaValues

# Finds the theoretical minima
def predictMinima() -> list[list]:
    """`predictMinima` computes the first n minima in the diffraction pattern, as per the theoretial formula"""

    # Final list of theoretical minima coordinates- first element is theta, second element is Intensity
    theoryMinima: list = [[], []]
    # Computing te fist n minima:
    for i in range(-params.n, params.n + 1):
        # Excluding n = 0 as it is the maxima
        if i == 0:
            continue
        
        minTheta: float = ((i * params.wavelength) / params.slitWidth)
        theoryMinima[0].append(i) 
        theoryMinima[1].append(minTheta)

    return theoryMinima

# Finds minima points
def findMinima(data: NDArray, peakPixel: float) -> tuple[NDArray, NDArray]:
    """`findMinima` finds all minima points in the given `data`"""
    
    pixelPositions = data[:, 0]
    intensities = data[:, 1]

    # Invert intensity to find minima as peaks in -intensity
    minimaIndices, _ = find_peaks(-intensities, distance=params.minimaDistance)

    # Convert pixel positions to theta using the same conversion
    theta_minima = pixelToTheta(pixelPositions[minimaIndices], peakPixel)
    intensity_minima = intensities[minimaIndices]

    return theta_minima, intensity_minima