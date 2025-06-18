# Package imports
import numpy as np
import os
import matplotlib.pyplot as plt
from numpy.typing import NDArray

import util.data as dt
import params

# Clear graph.
def clearGraph() -> None:
    """`clearGraph` clears the current simulation graph of any inserted values."""

    plt.clf()

# Congiure graph parameters.
def configureGraph(title: str, xLabel: str, yLabel: str, showGrid: bool = False) -> None:
    """`configureGraph` sets simulation graph parameters."""
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)

    plt.grid(showGrid)

def setGraphLimits(right: float, top: float):
    plt.xlim(right=right)  # sets max limit of x-axis
    plt.ylim(top=top)    # sets max limit of y-axis

def setGraphTicks(xValues: NDArray = [], yValues: NDArray = []):
    if len(xValues) != 0:
        plt.xticks(xValues)
    
    if len(yValues) != 0:
        plt.yticks(yValues)

# Plot the simulation graph.
def plotGraph(xAxis: NDArray, yAxis: NDArray, label: str = "New Graph", line="None", markers: str = "*") -> None:
    """`plotGraph` computes the simulation graph values."""

    plt.plot(xAxis, yAxis, label=label, marker=markers, linestyle=line)

def plotErrorGraph(xAxis: NDArray, yAxis: NDArray, xerr: float = 0, yerr: float = 0, label: str = "New Graph", line="None", markers: str = "*") -> None:
    """`plotGraph` computes the simulation graph values."""

    plt.errorbar(xAxis, yAxis, xerr=xerr, yerr=yerr, fmt="o", ecolor = "black")

# Display the graph to screen.
def displayGraph(title: str = "New Title", save=False) -> None:
    """`displayGraph` shows the computed simulation graph to the screen."""

    plt.legend()

    if save:
        saveGraph(dt.savedDataPath, title)

    plt.show()

# Save graph to file.
def saveGraph(outputPath: str = "data", graphName: str = "new-graph") -> None:
    """`saveGraph` saves the computed simulation graph to `outputPath/graphName`."""

    # Check if output path exists
    os.makedirs(outputPath, exist_ok=True)

    filename: str = os.path.join(outputPath, "%s.png" % graphName)
    
    # Make sure that the legend is always present in the saved figures
    plt.legend()

    plt.savefig(filename)