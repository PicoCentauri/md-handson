# i-PI Hands-on Demo: Replica Exchange MD with Machine Learning Potentials

This repository contains a demo for running Replica Exchange Molecular Dynamics (REMD) using **i-PI** and a machine learning potential. The demo uses a **PET** (Point Edge Transformer) model for a "nano soup" system.

## Prerequisites

To run this demo, you need to have `i-pi` and the `metatomic` driver installed. You can install them via pip:

```bash
pip install i-pi metatomic[torch]
```

## Demo Components

- **`nano_soup-*.xyz`**: 16 initial configurations for the REMD simulation.
- **`pet-mad-s-v1.5.0-rc1.pt`**: A pre-trained PET model used to calculate forces and energies.
- **`input-remd_direct.xml`**: i-PI input file using the "direct" interface (forcefield evaluated within the i-PI process).
- **`input-remd_socket.xml`**: i-PI input file using the "socket" interface (requires external drivers).
- **`run_driver.sh`**: A script to launch the `i-pi-driver-py` with the `metatomic` model.
- **`run_scripting.py`**: A Python script demonstrating the `InteractiveSimulation` API.

## How to Run

### 1. Socket Mode (Client-Server)
This is the original i-PI concept, running in client-server modes and allowing
for parallelization across multiple machines or processes.

1. **Start the i-PI server:**
   ```bash
   i-pi input-remd_socket.xml &
   ```
2. **Start the driver(s):**
   ```bash
   bash run_driver.sh
   ```
   *Note: You can run the driver multiple times in different terminals to speed up the simulation if you have enough CPU/GPU resources.*

### 2. Direct Mode
This is the simplest way to run, as it doesn't require managing separate driver processes.

```bash
i-pi input-remd_direct.xml
```

### 3. Interactive Scripting
This demonstrates how to use i-PI as a library within a Python script. The script runs a few steps, shuffles the structures manually, and then continues.

```bash
python run_scripting.py
```

## Monitoring the Simulation

The simulation will produce output files with the prefix `soup-nano_direct` or `soup-nano_socket`:
- `*.out`: Thermodynamic properties (step, time, potential energy, temperature, etc.)
- `*.pos_*.xyz`: Atomic trajectories.
- `*.checkpoint`: Restart files.

You can check the progress by looking at the `.out` files:
```bash
tail -f soup-nano_direct.out
```
