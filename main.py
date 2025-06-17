import math
import numpy as np
from scipy.constants import pi
from numpy.typing import NDArray
import scipy.signal as signal
import matplotlib.pyplot as plt
from pathlib import Path

# Custom Packages
import params
import util.plot as plot
import util.data as dt
import util.tools as tools

# Beta function
def beta(slitWidth, theta: float) -> float:
    """`beta` returns the beta angle function for a given `theta`."""
    
    # k = (2 * pi) / lambda
    k: float = (2 * pi) / params.wavelength

    # beta = (k * b * sin(theta)) / 2
    return (k * slitWidth * math.sin(theta)) / 2

# Intenisty function
def intensity(I0: float, beta: float) -> float:
    """`intensity` returns the diffraction intensity function for a given `beta` angle and initial intensity `I0`."""

    # Ensure no errors during runtime
    if beta == 0:
        return I0
    
    # I = I0 * (sin(beta) / beta)**2
    return I0 * (math.sin(beta) / beta)**2 + 65.6 # Some random value?

# Compute theoretical diffraction pattern.
def diffractionPattern(I0: float, slitWidth, thetaRange: NDArray) -> list[float]:
    """`diffractionPattern` computes the full theoretical diffraction model intensity solutions for a given `thetaRange` and initial intensity `I0`."""
    
    # The final list of intensity solution points
    pattern: list[float] = []

    # Compute intensity for each new theta
    for theta in thetaRange:
        # First convert theta to beta
        newBeta: float = beta(slitWidth, theta)

        # From beta compute the intensity
        newIntensity: float = intensity(I0, newBeta)
        
        pattern.append(newIntensity)
    
    return pattern

# Main entry point for the diffraction simulation
def main() -> None:
    # Add more samples to get more comparison results
    samples: list[str] = [dt.dataPath]

    # Compute the comparison graph for every sample
    for sample in samples:
        # Clear any residue graphs from previous attempts
        plot.clearGraph() 

        # Get slitwidth from the saved filepath name i.e. data/diffraction_data_200.dat -> slitWidth = 200
        filepath: str = Path(sample).stem # Take the filepath without extension
        slitWidth: float = float(filepath.split("_")[-1])  # Take the part after the last underscore, which is defined to be the slit width

        # Measured 'real' data
        realData: NDArray = dt.readData(sample)
        # The measured highest data peak value index
        peakIndex: NDArray = tools.maxPeakIndex(realData)
        # Measured 'real' data x value range conversion to general theta expressions
        realThetaRange: NDArray = tools.pixelToTheta(realData[:, 0], peakIndex)
        # Measured 'real' data values
        realIntensity: NDArray = realData[:, 1]

        # Adjusted initial (amplitued) as to measured data
        I0: float = realData[peakIndex,1]
        # Using theta parameters define the simulation grid (in radians)
        modelThetaRange: NDArray = np.linspace(math.radians(params.minTheta), math.radians(params.maxTheta), params.thetaStep)
        # Theoretical model intensity values
        modelIntensity: list[float] = diffractionPattern(I0, slitWidth, modelThetaRange)

        ####### Intensity pattern comparing
        # plot.plotGraph(modelThetaRange, modelIntensity, label="Theoretical Pattern")
        # plot.plotGraph(realThetaRange, realIntensity, label="Measured Pattern")

        # plot.configureGraph("Comparing theoretical with measured diffraction pattern intenisty values.", "$\\theta$ (radians)", "I (volts)", True)
        # plot.displayGraph()
        #######

        # Find the minimas for both model and measured data
        modelMinima: list[list] = tools.predictMinima(slitWidth)
        realMinima: list[NDArray] = tools.findMinima(realThetaRange, realIntensity)

        initialGuess: NDArray = np.array([params.wavelength / slitWidth, 0.0])
        calibratedRealMinima = tools.solveMinimaUncertainty(realMinima[0], realMinima[1], initialGuess)

        # Fitted parameters
        slope, intercept = calibratedRealMinima[0]

        # print(calibratedRealMinima)

        # Comparing the minima values
        plot.plotGraph(realMinima[0], realMinima[1], "Measured minima")
        plot.plotGraph(realMinima[0], np.array(slope) * np.array(realMinima[0]) + np.array(intercept), "Measured calibrated minima")
        plot.plotGraph(modelMinima[0], modelMinima[1], "Theoretical Minima")
        
        plot.configureGraph("Comparing theoretical with measured diffraction minima values.", "n", "$\\theta$ (radians)", True)
        plot.displayGraph()

    return

main()