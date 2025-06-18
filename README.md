# Diffraction Slit Width Comparison Simulation

This collection of simulations implements finite-difference solutions to the one-dimensional, time-independent Schrödinger equation for a variety of bound‐state potentials. The goal is to compare numerical eigenvalues and eigenfunctions against known theoretical results and to explore how different potentials influence the spectrum of allowed energy levels.

## Objectives

* Compute theoretical diffraction minima pattern points
* Measure and find real diffraction minima pattern points
* Compare both theoretical and measured (calibrated) minima points to determine any leftover uncertainties and accurate results

## Requirements

- Python 3.8 or later  
- NumPy  
- SciPy  
- Matplotlib

For simplicity requirements can be achived by running (NOT IMPLEMENTED YET):

```bash
make update
```

which installs and updated all neccessary system packages for the simulation.

## Usage

From project root directory run the specified makefile simulation command:

1. **Infinite Well SImulation:**

```bash
make run
```

or if make is not installed:

```bash
python3 main.py
```


* To clean any previous simulation data:

```bash
make clean
```