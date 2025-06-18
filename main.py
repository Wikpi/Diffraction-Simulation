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
    samples: list[str] = [dt.dataPath620, dt.dataPath650, dt.dataPath700, dt.dataPath750]
    # samples: list[str] = [dt.dataPath]

    realSlitWidths: list = []
    modelSlitWidths: list = []

    # Compute the comparison graph for every sample
    for sample in samples:
        # Clear any residue graphs from previous attempts
        plot.clearGraph() 

        # Get slitwidth from the saved filepath name i.e. data/diffraction_data_200.dat -> slitWidth = 200
        filepath: str = Path(sample).stem # Take the filepath without extension
        slitWidth: float = float(filepath.split("_")[-1])  # Take the part after the last underscore, which is defined to be the slit width
        # slitWidth += 12

        slitWidth *= 1e-6 # Convert to meters

        # Measured 'real' data
        realData: NDArray = dt.readData(sample)

        # pick an odd window ≤ len(y)
        n = len(realData[:, 1])
        window_length = min(31, n if n % 2 == 1 else n - 1)
        polyorder     = 2 if window_length > 2 else 1

        # smooth intensity
        smoothedRealIntensity = signal.savgol_filter(realData[:, 1], window_length=window_length, polyorder=polyorder)

        # plot.plotGraph(realData[:,0], smoothedRealIntensity)

        # The measured highest data peak value index
        # peakIndex: NDArray = tools.maxPeakIndex(realData)
        # Measured 'real' data x value range conversion to general theta expressions
        # realThetaRange: NDArray = tools.pixelToTheta(realData[:, 0], peakIndex)

        ####### Intensity pattern comparing
        # Measured 'real' data values
        # realIntensity: NDArray = realData[:, 1]

        # Adjusted initial (amplitued) as to measured data
        # I0: float = realData[peakIndex,1]
        # Using theta parameters define the simulation grid (in radians)
        # modelThetaRange: NDArray = np.linspace(math.radians(params.minTheta), math.radians(params.maxTheta), params.thetaStep)
        # # Theoretical model intensity values
        # modelIntensity: list[float] = diffractionPattern(I0, slitWidth, modelThetaRange)

        # plot.plotGraph(modelThetaRange, modelIntensity, label="Theoretical Pattern")
        # plot.plotGraph(realThetaRange, realIntensity, label="Measured Pattern")

        # plot.configureGraph("Comparing theoretical with measured diffraction pattern intenisty values.", "$\\theta$ (radians)", "I (volts)", True)
        # plot.displayGraph()
        #######

        # Find the minimas for both model and measured data
        modelMinima: list[list] = tools.predictMinima(slitWidth)
        realMinima: list[NDArray] = tools.findMinima(realData[:, 0], smoothedRealIntensity)

        initialGuess: NDArray = np.array([params.wavelength / slitWidth])
        calibratedRealMinima = tools.solveMinimaUncertainty(realMinima[0], realMinima[1], initialGuess)

        # Fitted parameters
        slope = calibratedRealMinima[0]

        realSlitWidth: float = params.wavelength / slope
        
        # Store all slit widths for final comparing
        realSlitWidths.extend(realSlitWidth)
        modelSlitWidths.append(slitWidth)

        # Comparing the minima values
        # plot.plotGraph(realMinima[0], realMinima[1], "Measured minima") # Previous uncalibrated measured data
        plot.plotErrorGraph(realMinima[0], np.array(slope) * np.array(realMinima[0]), yerr=params.thetaMinimalUncertainty, label="Measured Calibrated Minima", markers="+")
        plot.plotErrorGraph(modelMinima[0], modelMinima[1], yerr=params.thetaMinimalUncertainty, label="Theoretical Minima", markers="o")
        
        plot.configureGraph("Comparing theoretical with measured diffraction minima values for slit width = %e" % slitWidth, "n", "$\\theta$ (radians)", True)
        
        plot.saveGraph(dt.savedDataPath, "Comparing theoretical with measured diffraction minima values for slit width = %e" % slitWidth)
        
        plot.displayGraph()

    plot.clearGraph()

    plot.plotErrorGraph(np.array(modelSlitWidths), np.array(realSlitWidths), xerr=params.slitUncertainty, yerr=params.slitUncertainty, label="Compared Minima Points")
    plot.plotGraph(np.array(modelSlitWidths), np.array(modelSlitWidths), label="Theoretical 45 degree ratio", line="--", markers="None")
     
    # Finding line of best fit and creating a polynomial object for it
    coeffs = np.polyfit(np.array(modelSlitWidths), np.array(realSlitWidths), 1)
    fitLine = np.poly1d(coeffs)

    # Plotting the line of best fit
    xFit = np.linspace(min(modelSlitWidths), max(modelSlitWidths), 100)
    yFit = fitLine(xFit)
    plot.plotGraph(xFit, yFit, label = "Line of Best Fit", line= "-", markers = "None")

    plot.configureGraph("Comparing the model slit width with calibrated real slit width for %d samples." % len(samples), "Model", "Measured", True)
    # plot.setGraphLimits(modelSlitWidths[-1], realSlitWidths[-1])
    # plot.setGraphTicks(modelSlitWidths, realSlitWidths)

    # Printing the final results
    print("The slope of the line of best fit is:", coeffs[0])
    print("The intercept of the line of best fit is: %e"%(coeffs[1],))
    
    plot.saveGraph(dt.savedDataPath, "Comparing the model slit width with calibrated real slit width for %d samples." % len(samples))

    plot.displayGraph()

    return

main()