import numpy as np
from numpy.typing import NDArray

### Data path constants

# Diffraction data for 79e-5 slit width 
dataPath: str = "data/diffraction_data_79e-5.dat"
dataPath620: str = "data/20250617_diffraction_meas1_620.dat"
dataPath650: str = "data/20250617_diffraction_meas2_650.dat"
dataPath700: str = "data/20250617_diffraction_meas3_700.dat"
dataPath750: str = "data/20250617_diffraction_meas4_750.dat"
dataPath800: str = "data/20250617_diffraction_meas5_800.dat"
dataPath850: str = "data/20250617_diffraction_meas6_850.dat"
dataPath900: str = "data/20250617_diffraction_meas7_900.dat"
dataPath950: str = "data/20250617_diffraction_meas8_950.dat"

savedDataPath: str = "data/saved/"

## Data function

# Read data from file.
def readData(filePath: str) -> NDArray:
    """`readData` reads stored data from specified `filePath`."""

    data: NDArray = np.genfromtxt(filePath)

    return data