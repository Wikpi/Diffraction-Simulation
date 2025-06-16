# Package imports
import numpy as np
import os
import matplotlib.pyplot as plt
from numpy.typing import NDArray

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

# Plot the simulation graph.
def plotGraph(xAxis: NDArray, yAxis: NDArray, label: str = "New Graph") -> None:
    """`plotGraph` computes the simulation graph values."""

    plt.plot(xAxis, yAxis, label=label)

    # Get all major plot ticks based on overall x axis 
    indices = np.linspace(0, xAxis.size-1, 5, dtype=int)
    tickValues = np.round(xAxis[indices], 2)

    ax = plt.gca()
    ax.set_xlim(tickValues[0], tickValues[-1]) # Enforce hard limits for plot from -L ro L
    ax.set_xticks(tickValues) # Show major tick marks

# Display the graph to screen.
def displayGraph() -> None:
    """`displayGraph` shows the computed simulation graph to the screen."""

    plt.legend()

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