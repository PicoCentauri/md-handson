# LAMMPS engine 💪

## About LAMMPS

LAMMPS stands for "Large-scale Atomic/Molecular Massively Parallel Simulator". It's a widely used workhorse for materials science because it scales well, offers tons of interaction models, and has a super flexible input language. In this exercise, you'll see how LAMMPS scripts are structured and how its Kokkos on GPUs acceleration can seriously speed up production runs.

Kokkos is a performance portability library that allows LAMMPS to run efficiently on different hardware backends, including NVIDIA and AMD GPUs. By using Kokkos, you can get significant speedups for MD simulations without changing your input scripts too much – just a few flags to activate the GPU support! 🚀

LAMMPS is typically driven by a single input script. That script can read data files containing positions and, if present, topology information (bonds, angles, dihedrals) plus atom types. This makes it easy to keep the workflow in one place and to swap inputs by changing just a few commands.

For details on the LAMMPS commands refer to:
https://docs.lammps.org/Commands_input.html

## Goals 🎯

- Learn LAMMPS input structure (staged EM → NPT → production)
- Run CPU vs GPU production and compare runtime (spoiler: GPU is fast ⚡)
- Use a PET-MAD ML potential through metatomic

## System 🌊

We use a small liquid water box with 32 molecules in periodic boundary conditions. The system is intentionally tiny so you can iterate quickly during the hands-on session while still exercising a realistic workflow. Think of it as a speed-run version of real research! 🎮

## Files

- `em.in`: energy minimization (fill TODOs)
- `npt.in`: NPT equilibration (fill TODOs)
- `prod.in`: production (fill TODOs)
- `prod-kk.in`: GPU production (write from scratch)
- `water.data`: pre-built liquid water system

## Setup

Change the directory to the LAMMPS folder:

```bash
cd 1-lmp
```

Symlink the model into this folder:

```bash
ln -s ../model.pt model.pt
```

Create an alias for the LAMMPS binary:

```bash
lmp=/home/loche/repos/lab-cosmo/lammps/build/lmp
```

You can use the help page to get information on the input commands and the installed modules.

```bash
$lmp -h
```

LAMMPS is highly modular—most features are implemented as optional packages that one can choose to compile in or leave out. This means you only pay for what you use, and different builds can be tailored for different hardware or simulation types. For example, the Kokkos package (used for GPU acceleration) is compiled in here, but other builds might include different packages like special output formates, thermostats etc. Installed modules are displayed with `$lmp -h`. For our build you will find a very minimal list:

```
Installed packages:

KOKKOS ML-METATOMIC 
```

## Exercise 🏃

You'll run a three-stage workflow on CPU and then reproduce the production stage on GPU. The goal is to get comfortable with the input structure and the restart flow between stages.

### 1. Fill the TODOs and let the atoms dance 💃

 <!-- TODO:
 
 I think we should restructure this section. one subsection for each step: in EM step, NPT and prod and let the students explain what they see: for EM the potential energy goes down, for npt temperature and pressure equilibrate. Also since we restart from a restart file they should see the continuity of the simulation by the steps, during production the box but the temperature fluctuates.
 
 
 We also need a bit for comment lines what the commands are doing in the input files: em.in, npt.in, prod.in -->

Complete the missing parts in `em.in`, `npt.in`, and `prod.in`:
- **EM**: Select a minimizer and tolerances (how much energy change is good enough?)
- **NPT**: Choose thermostat and barostat settings (target 450 K 🌡️)
- **Production**: Read the NPT restart and write a trajectory (this is where the data comes from!)
### 2. Run the CPU pipeline

Execute the stages in order:

```bash
$lmp -in em.in
$lmp -in npt.in
$lmp -in prod.in
```

**What's happening?** Each stage builds on the previous one. EM relaxes the structure, NPT equilibrates at the right temperature and pressure, and production collects your actual data.

### 3. Write the GPU version for the production stage

From the production run note the Performance which should be around 1.8 ns/day. Now, let's run the same production stage on GPU using Kokkos. First, write a new input script `prod-kk.in` based on `prod.in` but with the necessary modifications to activate Kokkos and read the restart file from the NPT stage.

Write `prod-kk.in` from scratch using `prod.in` as reference. Use Kokkos (LAMMPS's GPU framework) and read the `npt.restart` file.

### 4. Run GPU production 🚀

```bash
$lmp -k on g 1 -sf kk -in prod-kk.in
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
