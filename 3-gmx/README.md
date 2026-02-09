# GROMACS engine 🧬

## About GROMACS

GROMACS stands for "GROningen MAchine for Chemical Simulations". It originated in the biomolecular community and is known for being blazingly fast, having robust workflows, and providing strong analysis tools. In this exercise, you'll use it with ML potentials and compare full ML to ML/MM production.

<!-- TODO: Briefly explain ML/MM -->

GROMACS splits the workflow into multiple file types: a structure file (`.gro`), a topology file (`.top`, often with included `.itp` files), and a parameter file (`.mdp`). The preprocessor `grompp` combines these into a single binary input (`.tpr`) that `mdrun` uses for the simulation.

> **Pro tip** 💡: After each successful GROMACS command, take a moment to enjoy the "GROMACS reminds you" quotes at the end of the output. They range from profound to hilarious and are a beloved tradition in the community!

## Goals 🎯

- Learn staged GROMACS workflows (EM → NPT → production)
- Run full ML and ML/MM production and compare RMSF
- Use PET ML potentials through metatomic

## System 🧪

We use alanine dipeptide, a small biomolecular model system with two peptide bonds. It's basically the "hello world" of biomolecular simulations – simple enough to run quickly, but still shows meaningful conformational changes. Perfect for learning bio-style workflows even if proteins aren't usually your thing!

> **Visualization tip** 💡: Open `alanine-dipeptide.pdb` in [chemiscope](https://chemiscope.org/) or [OVITO](https://www.ovito.org/) to see the actual 3D structure!

## Files

- `alanine-dipeptide.pdb`: starting structure
- `em.mdp`: energy minimization (provided)
- `npt.mdp`: NPT equilibration (provided)
- `grompp.mdp`: production (full ML, provided)

## Setup

Change the directory to the GROMACS folder:

```bash
cd 3-gmx
```

Symlink the model into this folder:

```bash
ln -s ../model.pt model.pt
```

## Exercise 🏃

The workflow follows a standard biomolecular pipeline: build and solvate the system, minimize, equilibrate, then run production. You'll then copy the production MDP and switch the ML region to create an ML/MM run.

Set the GROMACS command once:

```bash
gmx=/home/loche/repos/lab-cosmo/gromacs/build/bin/gmx
```

### 1. Build topology (AMBER99SB-ILDN + SPC/E)

```
$gmx pdb2gmx -f alanine-dipeptide.pdb -o dipeptide.gro -p topol.top -i posre.itp -ff amber99sb-ildn -water spce
```

**What's happening here?** `pdb2gmx` reads your structure file (PDB format) and generates a topology that describes all the bonds, angles, and interactions. It's basically translating your structure into GROMACS language. The `-ff` flag picks the force field (AMBER99SB-ILDN, good for proteins) and `-water spce` chooses the water model (SPC/E).

> **Important note** 📝: Creating a topology from a structure file is actually a *very hard task*. `pdb2gmx` seems magical and works incredibly well, but it only works for biomolecular systems (peptides, proteins, nucleic acids). For general materials, you'd have to create topologies by hand (painful 😅) or... just use an MLIP 🤭

### 2. Define a box and solvate 💧

We now need to put our molecule in a box and fill it with water. This is crucial for MD because we want to simulate a realistic environment. The commands are:

```
$gmx editconf -f dipeptide.gro -o boxed.gro -c -d 0.4 -bt cubic
$gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top
```

**What's happening here?** 

```
                      ┌─────────────┐            ┌─────────────┐
                      │             │            │ ○  ○    ○   │
                      │ <- 0.4nm -> │            │    ○  ○     │
        x   ------>   │      x      │   ----->   │ ○   x   ○   │
                      │             │            │    ○   ○    │
                      │             │            │ ○   ○   ○   │
                      └─────────────┘            └─────────────┘
```

- `editconf`: Creates a simulation box around your molecule. The `-c` flag centers the molecule, `-d 1.0` puts the box edges 1.0 nm away from the molecule (so it doesn't see its own periodic image), and `-bt cubic` makes it a cube.
- `solvate`: Fills the box with water molecules! It takes a pre-equilibrated water box (`spc216.gro`) and places water molecules wherever they fit around your solute. It also updates `topol.top` to include all those water molecules in the topology.

### 3. Energy minimization ⚡

```bash
$gmx grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr
$gmx mdrun -deffnm em
```

The `-deffnm` option will set the default filename for all output files to `em`, so you'll get `em.gro`, `em.log`, etc.

Full MDP option reference:
https://manual.gromacs.org/current/user-guide/mdp-options.html

**What's happening?** Energy minimization removes any crazy overlaps or bad contacts in your starting structure. Think of it as gently relaxing the system before doing real dynamics.

> **If you hit a `grompp` error here**: double-check the choices you made in step 2 (box size and solvation). A box that is too small for the cutoff scheme will fail during preprocessing.

### 4. NPT equilibration 🌡️

```bash
$gmx grompp -f npt.mdp -c em.gro -p topol.top -o npt.tpr
$gmx mdrun -v -deffnm npt
```

**What's happening?** Now we run a short simulation at constant pressure and temperature to let the system equilibrate. The density will adjust to the right value, and everything will settle into a reasonable state before production.

### 5. Production (full ML) 🚀

```bash
$gmx grompp -f grompp.mdp -c npt.gro -p topol.top -o md.tpr
$gmx mdrun -v -deffnm md
```

**What's happening?** This is the real deal! The production run where we collect data using the ML potential for *everything* (dipeptide + water).

### 6. ML/MM production ⚡💧

- Copy the production MDP and change `metatomic-input-group` to the peptide. To figure out the name of the group you can create an index file with:

```bash
$gmx make_ndx -f npt.gro -o index.ndx
```

Just type `q` and hit enter to create no special group. Inspect the `index.ndx` file to find the name of the peptide group. Use that name in the MDP file and then run:

```bash
$gmx grompp -f grompp-mlmm.mdp -c npt.gro -p topol.top -o md-mlmm.tpr
```

How many atoms are in the ML region? How many are in the MM region? Check the terminal output from `grompp` to confirm that the ML/MM partitioning is correct. Then run:

```bash
$gmx mdrun -deffnm md-mlmm
```

Did you notice that the ML/MM production is faster than the full ML?

## Analysis 📊

Compare RMSF between full ML and ML/MM:

RMSF (root-mean-square fluctuation) measures how much each atom or residue jiggles around its average position over the trajectory. Higher RMSF = more floppy, lower = more rigid. It's super useful for comparing how different setups affect dynamics!

```bash
$gmx rmsf -f md.trr -s md.tpr -o rmsf-ml.xvg
```

Select the peptide group when prompted. Then do the same for the ML/MM run:

```bash
$gmx rmsf -f md-mlmm.trr -s md-mlmm.tpr -o rmsf-mlmm.xvg
```

You can compare the outputs by plotting them with `matplotlib` or any plotting tool you like.
Are the RMSF profiles similar? Where do they differ? This can give you insight into how the ML/MM partitioning affects the dynamics of the peptide.
