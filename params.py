
# Max theta for which to compute intensity (in degrees)
maxTheta: float = 2
# Min theta for which to compute intensity (in degrees)
minTheta: float = -maxTheta # Has to be symmetrical so inverse of maxTheta
# Step at which to compute theta range values (in degrees)
thetaStep: float = 500
# The distance between slit and screen (in meters)
slitDistance: float = 83e-2
# The total amount of pixels that were preconfigured for the CCD screen
pixelCount: int = 3678
# Wavelength of the laser (in meters)
wavelength: float = 635e-9
# Pixel width (in meters)
pixelWidth: float = 8e-6
# Number of theoretical minima to calculate
n: float = 32
# The distance between each new consecutive minima point. This is introduced to reduce redundancy from noisiness
minimaDistance: float = 50
# Uncertainty for n (x axis)
nMinimalUncertainty: float = 0.1
# Uncertainty for theta (y axis)
thetaMinimalUncertainty: float = 1.16 * 10e-8 #10e-5
# Unvertainty for the slits (x and y axis)
slitUncertainty: float = 10e-6