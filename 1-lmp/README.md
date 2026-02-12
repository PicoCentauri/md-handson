# LAMMPS engine 💪

LAMMPS stands for "Large-scale Atomic/Molecular Massively Parallel Simulator". It's a
widely used workhorse for materials science because it scales well, offers tons of
interaction models, and has a flexible input language. In this exercise, you'll
see how LAMMPS scripts are structured and how its Kokkos on GPUs acceleration can
seriously speed up production runs.

Kokkos is a performance portability library that allows LAMMPS to run efficiently on
different hardware backends, including NVIDIA and AMD GPUs. By using Kokkos, you can get
significant speedups for MD simulations without changing your input scripts too much –
just a few flags to activate the GPU support! 🚀

LAMMPS is typically driven by a single input script. That script can read data files
containing positions and, if present, topology information including atom types. This
makes it easy to keep the workflow in one place and to swap inputs by changing just a
few commands. Atom types in LAMMPS are usually defined by integers starting from 1. This
means that an oxygen might be atom type 1, and a hydrogen might be atom type 2 or vice
versa depending how you set up your input file.

For details on the LAMMPS commands refer to: https://docs.lammps.org/Commands_input.html

> **Pro tip** 💡: LAMMPS has a *very* lively community. When you hit a problem and search 
> for solutions, you'll often find answers from Axel Kohlmeyer, one of the main LAMMPS 
> developers. His replies are legendary for being... *brutally honest*. His answers are 
> gold, but fair warning: his tone is not for the faint-hearted. Read his comments, 
> learn from them, but don't take it personally if he points out your mistake in capital 
> letters! 😅

## Goals 🎯

- Learn LAMMPS input structure (staged EM → NPT → production)
- Run CPU vs GPU production and compare runtime
- Use a PET-MAD ML potential through metatomic

## System 🌊

We use a small liquid water box with 32 molecules in periodic boundary conditions. The
system is intentionally tiny so you can iterate quickly during the hands-on session
while still exercising a realistic workflow. Think of it as a speed-run version of real
research! 🎮

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

You can use the help page to get information on the input commands and the installed
modules.

```bash
$lmp -h
```

LAMMPS is highly modular—most features are implemented as optional packages that one can
choose to compile in or leave out. This means you only pay for what you use, and
different builds can be tailored for different hardware or simulation types. For
example, the Kokkos package (used for GPU acceleration) is compiled in here, but other
builds might include different packages like special output formates, thermostats etc.
Installed modules are displayed with `$lmp -h`. For our build you will find a very
minimal list:

```
Installed packages:

EXTRA-FIX KOKKOS ML-METATOMIC 
```

## Exercise 🏃

You'll run a three-stage workflow on CPU and then reproduce the production stage on GPU.
The goal is to get comfortable with the input structure and the restart flow between
stages.

### 1. Fill the TODOs and let the atoms dance 💃

Complete the missing parts in `em.in`, `npt.in`, and `prod.in` and run each stage. After
each run, observe the output carefully!

#### 1a. Energy Minimization (EM)

Open `em.in` and complete the TODO: select a minimizer and set tolerances.

Run the minimization:

```bash
$lmp -in em.in
```

**What to observe:** Watch the potential energy decrease as the structure relaxes. The
minimizer is finding a *local* energy minimum by adjusting atomic positions. The
energy should drop significantly in the first iterations and then level off as the
system reaches a stable configuration.

**logs 📝** By default, LAMMPS writes a `log.lammps` file in the current directory which
display the same as on the terminal

#### 1b. NPT Equilibration

Open `npt.in` and complete the TODO: set up thermostat and barostat settings (target 450
K 🌡️ and 1.0 bar).

Run the equilibration:

```bash
$lmp -in npt.in
```

**What to observe:** Temperature and pressure both equilibrate to their targets. Note
that:
- Initial values may be far from 450 K since we start from a minimized (cold) structure
- Instantaneous values fluctuate strongly!
- Look at the time-averaged values (look at trends across many steps)
- The box volume may adjust as the system finds the right density our target pressure
  and temperature. You can compute the density if you like and compare to a literature
  value.
- Since we `read_restart` from the EM stage, the simulation continues seamlessly and the
  number of steps don't start from 0.

#### 1c. Production Run

Open `prod.in` and complete the TODO: read the restart from NPT and set up trajectory
output.

Run production:

```bash
$lmp -in prod.in
```

**What to observe:**
- The simulation continues from the NPT equilibrated state (restart continuity!)
- Temperature fluctuates around 450 K.
- The box dimensions should remain stable since we're running NVT (constant volume)
  after equilibration. You can adjust the `thermo` output to include the box dimensions if you like.
- A trajectory file `prod.lammpstrj` is written for later analysis
- Note the **Performance** at the end (~XXX ns/day on CPU) – write this down!

### 2. GPU-accelerated production run with Kokkos 🚀

Now that you have the CPU performance baseline, let's run the same production stage on
GPU and see the speedup!

Write a new input script `prod-kk.in` based on `prod.in` but with Kokkos GPU
acceleration:
- Change `atom_style atomic` to `atom_style atomic/kk`
- Add `package kokkos newton on neigh half` at the top
- Change `pair_style metatomic` to `pair_style metatomic/kk` and add `device cuda`
- Add `run_style verlet/kk` before the `run` command
- Use the `npt.restart` file to continue from the equilibrated state

Run the GPU version:

```bash
$lmp -k on g 1 -sf kk -in prod-kk.in
```

**What's happening?** The `-k on g 1` tells LAMMPS to use 1 GPU, and `-sf kk` activates
the Kokkos package. 

**What to observe:**
- Compare the **Performance** with the CPU run – you should see a significant speedup! ⚡
- The trajectory should be physically equivalent to the CPU run (same physics, just
  faster computation)
- How many times faster is the GPU? Calculate the speedup factor!
