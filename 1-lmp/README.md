# LAMMPS engine 💪

## About LAMMPS

LAMMPS stands for "Large-scale Atomic/Molecular Massively Parallel Simulator" (quite a mouthful, right? 😅). It's a widely used workhorse for materials science and soft matter because it scales like a beast, offers tons of interaction models, and has a super flexible input language. In this exercise, you'll see how LAMMPS scripts are structured and how GPU acceleration can seriously speed up production runs.

LAMMPS is typically driven by a single input script. That script can read data files containing positions and, if present, topology information (bonds, angles, dihedrals) plus atom types. This makes it easy to keep the workflow in one place and to swap inputs by changing just a few commands.

## Goals 🎯

- Learn LAMMPS input structure (staged EM → NPT → production)
- Run CPU vs GPU production and compare runtime (spoiler: GPU is fast ⚡)
- Use a PET ML potential through metatomic

## System 💧

We use a small liquid water box with 32 molecules in periodic boundary conditions. The system is intentionally tiny so you can iterate quickly during the hands-on session while still exercising a realistic workflow. Think of it as a speed-run version of real research! 🎮

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

## Exercise 🏃

You'll run a three-stage workflow on CPU and then reproduce the production stage on GPU. The goal is to get comfortable with the input structure and the restart flow between stages.

### 1. Fill the TODOs

Complete the missing parts in `em.in`, `npt.in`, and `prod.in`:
- **EM**: Select a minimizer and tolerances (how much energy change is good enough?)
- **NPT**: Choose thermostat and barostat settings (target 450 K 🌡️)
- **Production**: Read the NPT restart and write a trajectory (this is where the data comes from!)
### 2. Run the CPU pipeline

Execute the stages in order:

```
/home/loche/repos/lab-cosmo/lammps/build/lmp -in em.in
/home/loche/repos/lab-cosmo/lammps/build/lmp -in npt.in
/home/loche/repos/lab-cosmo/lammps/build/lmp -in prod.in
```

**What's happening?** Each stage builds on the previous one. EM relaxes the structure, NPT equilibrates at the right temperature and pressure, and production collects your actual data.

### 3. Write the GPU version

Write `prod-kk.in` from scratch using `prod.in` as reference. Use Kokkos (LAMMPS's GPU framework) and read the `npt.restart` file.

### 4. Run GPU production 🚀

```
/home/loche/repos/lab-cosmo/lammps/build/lmp -k on g 1 -sf kk -in prod-kk.in
```

**What's happening?** The `-k on g 1` tells LAMMPS to use 1 GPU, and `-sf kk` activates the Kokkos package. Watch it fly! ⚡

## Expected checks ✅

- `em.restart` and `npt.restart` are written
- Temperature and pressure stabilize in the time average during NPT (remember: instantaneous values are noisy!)
- Production generates a trajectory file (e.g., `prod.lammpstrj`)
- GPU run is faster than CPU for production (probably by a lot! 🚀)

## Outputs and logs 📝

Watch the output during the run and review the log file afterwards. By default, LAMMPS writes a `log.lammps` file in the current directory. Remember: instantaneous temperature and pressure jump around and don't mean much on their own – always check time-averaged values!

## Notes 📌

- If you're new to LAMMPS: focus on the script layout and the flow of data between stages.
- If you're experienced: try to estimate a rough speedup factor from the CPU and GPU runs. How many times faster is it?
- Most importantly: have fun and experiment! LAMMPS is super flexible once you get the hang of it. 😊
