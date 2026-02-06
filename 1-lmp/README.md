# LAMMPS engine

## About LAMMPS

LAMMPS stands for "Large-scale Atomic/Molecular Massively Parallel Simulator". It is a widely used workhorse for materials science and soft matter because it scales well, offers many interaction models, and exposes a very flexible input language. In this exercise, you will see how LAMMPS scripts are structured and how GPU acceleration can speed up production runs.

LAMMPS is typically driven by a single input script. That script can read data files that contain positions and, if present, topology information (bonds, angles, dihedrals) plus atom types. This makes it easy to keep the workflow in one place and to swap inputs by changing a few commands.

## Goals

- Learn LAMMPS input structure (staged EM -> NPT -> production)
- Run CPU vs GPU production and compare runtime
- Use a PET ML potential through metatomic

## System

We use a small liquid water box with 32 molecules in periodic boundary conditions. The system is intentionally tiny so that you can iterate quickly during the hands-on session while still exercising a realistic workflow.

## Files

- `em.in`: energy minimization (fill TODOs)
- `npt.in`: NPT equilibration (fill TODOs)
- `prod.in`: production (fill TODOs)
- `prod-kk.in`: GPU production (write from scratch)
- `water.data`: pre-built liquid water system

## Setup

Symlink the model into this folder:

```
ln -s ../model.pt model.pt
```

LAMMPS binary:

```
/home/loche/repos/lab-cosmo/lammps/build/lmp
```

LAMMPS command reference:
https://docs.lammps.org/Commands_input.html

## Exercise

You will run a three-stage workflow on CPU and then reproduce the production stage on GPU. The goal is to get comfortable with the input structure and the restart flow between stages.

1. Fill the TODOs in `em.in`, `npt.in`, and `prod.in`.
	- EM: select a minimizer and tolerances
	- NPT: choose thermostat and barostat settings (target 450 K)
	- Production: read the NPT restart and write a trajectory
2. Run the CPU pipeline in order:

```
/home/loche/repos/lab-cosmo/lammps/build/lmp -in em.in
/home/loche/repos/lab-cosmo/lammps/build/lmp -in npt.in
/home/loche/repos/lab-cosmo/lammps/build/lmp -in prod.in
```

3. Write `prod-kk.in` from scratch using `prod.in` as reference. Use Kokkos and read the `npt.restart` file.
4. Run GPU production:

```
/home/loche/repos/lab-cosmo/lammps/build/lmp -k on g 1 -sf kk -in prod-kk.in
```

## Expected checks

- `em.restart` and `npt.restart` are written
- Temperature and pressure stabilize in the time average during NPT
- Production generates a trajectory file (for example `prod.lammpstrj`)
- GPU run is faster than CPU for production

## Outputs and logs

Watch the output during the run and review the log file afterwards. By default, LAMMPS writes a `log.lammps` file in the current directory. Instantaneous temperature and pressure fluctuate and are not meaningful on their own; check time-averaged values instead.

## Notes

- If you are new to LAMMPS, focus on the script layout and the flow of data between stages.
- If you are experienced, try to estimate a rough speedup factor from the CPU and GPU runs.
