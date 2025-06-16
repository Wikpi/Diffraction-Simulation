import numpy as np
from numpy.typing import NDArray

# Read data from file.
def readData(filePath: str) -> NDArray:
    """`readData` reads stored data from specified `filePath`."""

    data: NDArray = np.genfromtxt(filePath)

    return data