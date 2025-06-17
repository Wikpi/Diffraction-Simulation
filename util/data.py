import numpy as np
from numpy.typing import NDArray

### Data path constants

# Diffraction data for 79e-5 slit width 
dataPath: str = "data/diffraction_data_79e-5.dat"

## Data function

# Read data from file.
def readData(filePath: str) -> NDArray:
    """`readData` reads stored data from specified `filePath`."""

    data: NDArray = np.genfromtxt(filePath)

    return data