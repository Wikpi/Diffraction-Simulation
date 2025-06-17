import numpy as np
from scipy import odr
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
def predictMinima(slitWidth: float) -> list[list]:
    """`predictMinima` computes the first n minima in the diffraction pattern, as per the theoretial formula"""

    # Final list of theoretical minima: first element is a list of n values, second element is a list of minima values
    theoryMinima: list = [[], []]
    # Computing te fist n minima:
    for i in range(-params.n, params.n + 1):
        # Excluding n = 0 as it is the maxima
        if i == 0:
            continue
        
        minTheta: float = ((i * params.wavelength) / slitWidth)
        theoryMinima[0].append(i) 
        theoryMinima[1].append(minTheta)

    return theoryMinima

# Finds minima points
def findMinima(xValues: NDArray, yValues: NDArray) -> list[NDArray]:
    """`findMinima` finds all minima points in the given `yValues`."""

    # Invert intensity to find minima as peaks, using minimaDistance to reduce inaccuracy from noisiness
    minimaIndices, _ = find_peaks(-yValues, distance=params.minimaDistance)
    minimaValues: NDArray = xValues[minimaIndices]

    # Partial n count, meaning from center to one direction only (half of all n values)
    nPartial: int = int(np.size(minimaValues) / 2)
    nRange: list[int] = list(range(-nPartial, nPartial+1)) # Ensure to include last point

    # Final list of measured minima: first element is a list of n values, second element is a list of minima values
    return [nRange, minimaValues]

# Get minima slope.
def solveMinimaUncertainty(xValues: NDArray, yValues: NDArray, initial: NDArray) -> float:
    """`solveMinimaUncertainty` finds the minmaModel slope value for given `yValues` and `initial` guesses."""
    
    # Minima model
    def minimaModel(B, n) -> float:
        """`minimaModel` is the minima function."""

        return B[0] * n + B[1]
    
    # Compute full array datas for param uncertainties
    xErr: NDArray = np.full(len(xValues), params.nMinimalUncertainty, dtype=float)
    yErr: NDArray = np.full(len(yValues), params.thetaMinimalUncertainty, dtype=float)

    # ODR models
    data = odr.RealData(xValues, yValues, sx=xErr, sy=yErr)
    model = odr.Model(minimaModel)

    odrSetup = odr.ODR(data, model, beta0=initial)
    output = odrSetup.run()
    
    # Finall output list, first element is a list of computed values with no uncertainty: x and y, second element is their respective uncertainties.
    return [output.beta, output.sd_beta]