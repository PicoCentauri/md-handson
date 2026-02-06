# Molecular Dynamics Engine Hands-on Tutorial

This hands-on session introduces three MD engines through short, guided exercises on the Kuma cluster. You will run the same ML potential with different engines and compare workflows, performance, and outputs.

Before asking the instructor for help, try:
- A quick web search
- Asking an LLM
- Discussing with your partner

## Session setup

Start an interactive Slurm session:

```
srun --time=02:00:00 --nodes=1 --ntasks=1 --mem-per-gpu=90G --gres=gpu:1 --partition=l40 --pty /bin/bash
```

This starts a 2-hour interactive session with one node, one task, one GPU, and 90 GB GPU memory on the `l40` partition, and opens a shell on the allocated node.

Load modules:

```
module purge
module load gcc
module load openmpi/5.0.3-cuda
```

Create a virtual environment and install tools:

```
python -m venv .venv
source .venv/bin/activate
pip install metatrain ipi
```

Fetch the PET ML potential once in the repo root:

```
mtt export https://huggingface.co/lab-cosmo/upet/resolve/main/models/pet-mad-s-v1.0.2.ckpt -o model.pt
```

You will symlink or copy `model.pt` into each engine folder as needed.

Reference solutions are available in the `solutions/` folder.

## Simulation conditions

The PET-MAD potential is trained with PBE-sol reference data, so we run the simulations at 450 K in this hands-on. Instantaneous temperature and pressure fluctuate strongly in MD; only time-averaged values should match the target conditions.

## What is a topology?

In MD, a topology describes how atoms are connected and which interaction parameters apply. It typically includes bonded terms (bonds, angles, dihedrals) and nonbonded parameters (charges, atom types). The structure file provides coordinates, while the topology provides the force field definition.

## Why not use ASE for MD here?

ASE is excellent for prototyping and single-point calculations, but it is not optimized for long, high-performance MD runs. MD engines provide faster kernels, more flexible integration schemes, and better-tested thermostat and barostat implementations. For this session, we focus on engine-level workflows and performance rather than high-level wrappers.

## Engine overview

| Engine | Focus | Why it matters |
| --- | --- | --- |
| LAMMPS | Materials workhorse, GPU performance | Flexible input scripts and scalable performance |
| i-PI | Advanced sampling, PIMD | Decouples force engines and enables path integrals |
| GROMACS | Biomolecular MD, ML/MM | Mature bio workflows with hybrid ML/MM support |
