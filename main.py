import math
import numpy as np
from scipy.constants import pi
from numpy.typing import NDArray
import scipy.signal as signal

# Custom Packages
import params
import util.plot as plot
import util.data as dt
import util.constants as cst
import util.tools as tools

# Beta function
def beta(theta: float) -> float:
    """`beta` returns the beta angle function for a given `theta`."""
    
    # k = (2 * pi) / lambda
    k: float = (2 * pi) / params.wavelength

    # beta = (k * b * sin(theta)) / 2
    return (k * params.slitWidth * math.sin(theta)) / 2

# Intenisty function
def intensity(I0: float, beta: float) -> float:
    """`intensity` returns the diffraction intensity function for a given `beta` angle and initial intensity `I0`."""

    # Ensure no errors during runtime
    if beta == 0:
        return I0
    
    # I = I0 * (sin(beta) / beta)**2
    return I0 * (math.sin(beta) / beta)**2 + 65.6 # Some random value?

# Compute theoretical diffraction pattern.
def diffractionPattern(I0: float, thetaRange: NDArray) -> list:
    """`diffractionPattern` computes the full theoretical diffraction model intensity solutions for a given `thetaRange` and initial intensity `I0`."""
    
    # The final list of intensity solution points
    pattern: list = []

    # Compute intensity for each new theta
    for theta in thetaRange:
        # First convert theta to beta
        newBeta: float = beta(theta)

        # From beta compute the intensity
        newIntensity: float = intensity(I0, newBeta)
        
        pattern.append(newIntensity)
    
    return pattern

# def getMinima(data: NDArray, distance: float, peakPixel: float) -> tuple[NDArray, NDArray]:
#     pixelPositions = data[:, 0]
#     intensities = data[:, 1]

#     # Invert intensity to find minima as peaks in -intensity
#     inverted = -intensities
#     minima_indices, _ = signal.find_peaks(inverted, distance=80)

#     # Convert pixel positions to theta using the same conversion
#     theta_minima = tools.pixelToTheta(pixelPositions[minima_indices], distance, peakPixel)
#     intensity_minima = intensities[minima_indices]

#     return theta_minima, intensity_minima


# Main entry point for the diffraction simulation
def main() -> None:
    # Measured or 'real' data
    realData: NDArray = dt.readData(cst.dataPath)
    # The measured data peak value index
    peakIndex: NDArray = tools.maxPeakIndex(realData)
    # Measured 'real' data x value range conversion to general theta expressions
    realThetaRange: NDArray = tools.pixelToTheta(realData[:, 0], peakIndex)
    
    # minima = getMinima(realData, slitWidthB, peakPixel)
    
    # Adjusted initial (amplitued) as to measured data
    I0: float = realData[peakIndex,1]
    # Using theta parameters define the simulation grid (in radians)
    modelThetaRange: NDArray = np.linspace(math.radians(-params.maxTheta), math.radians(params.maxTheta), params.thetaStep)
    # Theoretical model intensity values
    intensityData: list = diffractionPattern(I0, modelThetaRange)

    plot.plotGraph(modelThetaRange, intensityData)
    plot.plotGraph(realThetaRange, realData[:,1])

    # plt.scatter(minima[0], minima[1])
    # plot.plotGraph(range(-int(0.5* np.size(minima[0])), int(0.5* np.size(minima[0]))+1), minima[0])
    
    plot.displayGraph()

    return

main()