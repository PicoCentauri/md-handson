# GROMACS engine 🧬

## About GROMACS

GROMACS stands for "GROningen MAchine for Chemical Simulations" (yes, really 😄). It originated in the biomolecular community and is known for being blazingly fast, having robust workflows, and providing strong analysis tools. In this exercise, you'll use it with ML potentials and compare full ML to ML/MM production.

GROMACS splits the workflow into multiple file types: a structure file (`.gro`), a topology file (`.top`, often with included `.itp` files), and a parameter file (`.mdp`). The preprocessor `grompp` combines these into a single binary input (`.tpr`) that `mdrun` uses for the simulation.

> **Pro tip** 💡: After each successful GROMACS command, take a moment to enjoy the "GROMACS reminds you" quotes at the end of the output. They range from profound to hilarious and are a beloved tradition in the community!

## Goals 🎯

- Learn staged GROMACS workflows (EM → NPT → production)
- Run full ML and ML/MM production and compare RMSF
- Use PET ML potentials through metatomic

## System 🧪

We use alanine dipeptide, a small biomolecular model system with two peptide bonds. It's basically the "hello world" of biomolecular simulations – simple enough to run quickly, but still shows meaningful conformational changes. Perfect for learning bio-style workflows even if proteins aren't usually your thing!

<!-- Add ascii art of the dipeptide and encourage people to visualize it with chemiscope or ovito -->

## Files

- `alanine-dipeptide.pdb`: starting structure
- `em.mdp`: energy minimization (provided)
- `npt.mdp`: NPT equilibration (provided)
- `grompp.mdp`: production (full ML, provided)

## Setup

Symlink the model into this folder:

```
ln -s ../model.pt model.pt
```

GROMACS binary:

```
/home/loche/repos/lab-cosmo/gmx/build/gmx
```

MDP option reference:
https://manual.gromacs.org/current/user-guide/mdp-options.html

## Exercise 🏃

The workflow follows a standard biomolecular pipeline: build and solvate the system, minimize, equilibrate, then run production. You'll then copy the production MDP and switch the ML region to create an ML/MM run.

Set the GROMACS command once:

```
GMX=/home/loche/repos/lab-cosmo/gmx/build/gmx
```

### 1. Build topology (AMBER99SB-ILDN + SPC/E)

```
$GMX pdb2gmx -f alanine-dipeptide.pdb -o dipeptide.gro -p topol.top -i posre.itp -ff amber99sb-ildn -water spce
```

**What's happening here?** `pdb2gmx` reads your structure file (PDB format) and generates a topology that describes all the bonds, angles, and interactions. It's basically translating your structure into GROMACS language. The `-ff` flag picks the force field (AMBER99SB-ILDN, good for proteins) and `-water spce` chooses the water model (SPC/E).

> **Important note** 📝: Creating a topology from a structure file is actually a *very hard task*. `pdb2gmx` seems magical and works incredibly well, but it only works for biomolecular systems (peptides, proteins, nucleic acids). For general materials, you'd have to create topologies by hand (painful 😅) or... just use an MLIP 🤭

### 2. Define a box and solvate 💧

<!-- add ascii arte of the process: show box creation centering -->

```
$GMX editconf -f dipeptide.gro -o boxed.gro -c -d 1.0 -bt cubic
$GMX solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top
```

**What's happening here?** 
- `editconf`: Creates a simulation box around your molecule. The `-c` flag centers the molecule, `-d 1.0` puts the box edges 1.0 nm away from the molecule (so it doesn't see its own periodic image), and `-bt cubic` makes it a cube.
- `solvate`: Fills the box with water molecules! It takes a pre-equilibrated water box (`spc216.gro`) and places water molecules wherever they fit around your solute. It also updates `topol.top` to include all those water molecules in the topology.

### 3. Energy minimization ⚡

```
$GMX grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr
$GMX mdrun -deffnm em
```

**What's happening?** Energy minimization removes any crazy overlaps or bad contacts in your starting structure. Think of it as gently relaxing the system before doing real dynamics.

### 4. NPT equilibration 🌡️

```
$GMX grompp -f npt.mdp -c em.gro -p topol.top -o npt.tpr
$GMX mdrun -deffnm npt
```

**What's happening?** Now we run a short simulation at constant pressure and temperature to let the system equilibrate. The density will adjust to the right value, and everything will settle into a reasonable state before production.

### 5. Production (full ML) 🚀

```
$GMX grompp -f grompp.mdp -c npt.gro -p topol.top -o md.tpr
$GMX mdrun -deffnm md
```

**What's happening?** This is the real deal! The production run where we collect data using the ML potential for *everything* (dipeptide + water).

### 6. ML/MM production ⚡💧

- Copy the production MDP and change `metatomic-input-group` to `Dipeptide`.
- Create an index group named `Dipeptide` (ACE + ALA + NME):

```
$GMX make_ndx -f npt.gro -o index.ndx
```

Then run:

```
$GMX grompp -f grompp-mlmm.mdp -c npt.gro -p topol.top -n index.ndx -o md-mlmm.tpr
$GMX mdrun -deffnm md-mlmm
```

## Analysis 📊

Compare RMSF between full ML and ML/MM:

RMSF (root-mean-square fluctuation) measures how much each atom or residue jiggles around its average position over the trajectory. Higher RMSF = more floppy, lower = more rigid. It's super useful for comparing how different setups affect dynamics!

```
$GMX rmsf -f md.xtc -s md.tpr -o rmsf-ml.xvg
$GMX rmsf -f md-mlmm.xtc -s md-mlmm.tpr -o rmsf-mlmm.xvg
```

## Expected checks ✅

- `em.gro`, `npt.gro`, `md.xtc`, and `md-mlmm.xtc` are created
- RMSF differs mainly for the dipeptide region
- ML/MM production is faster than full ML (because less ML = less compute 🎉)

## Outputs and logs 📝

Monitor the terminal output while the simulation runs, then check the log files. With `-deffnm em`, `npt`, and `md`, GROMACS writes `em.log`, `npt.log`, and `md.log`. Remember: instantaneous temperature and pressure jump around like crazy and don't mean much – always look at time-averaged values!

## Notes 📌

- If you're new to GROMACS: focus on understanding how MDP files define each stage of the workflow.
- If you're experienced: pay attention to how the ML/MM region is defined and how it affects RMSF.
- Most importantly: have fun and don't stress if something doesn't work the first time – debugging is part of the learning process! 😊