# GROMACS engine

## About GROMACS

GROMACS stands for "GROningen MAchine for Chemical Simulations". It originated in the biomolecular community and is known for very fast, robust workflows and providing strong analysis tools. In this exercise, you will use it with ML potentials and compare full ML to ML/MM production.

GROMACS splits the workflow into multiple file types: a structure file (`.gro`), a topology file (`.top`, often with included `.itp` files), and a parameter file (`.mdp`). The preprocessor `grompp` combines these into a single binary input (`.tpr`) that `mdrun` uses for the simulation.

## Goals

- Learn staged GROMACS workflows (EM -> NPT -> production)
- Run full ML and ML/MM production and compare RMSF
- Use PET ML potentials through metatomic

## System

We use alanine dipeptide, a small biomolecular model system with two peptide bonds. It is a classic test case in biomolecular simulation because it is simple enough to run quickly, yet still shows meaningful conformational changes. This makes it ideal for introducing bio-style workflows even if you have not worked with biomolecules before.

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

## Exercise

The workflow follows a standard biomolecular pipeline: build and solvate the system, minimize, equilibrate, then run production. You will then copy the production MDP and switch the ML region to create an ML/MM run.

Set the GROMACS command once:

```
GMX=/home/loche/repos/lab-cosmo/gmx/build/gmx
```

1. Build topology (AMBER99SB-ILDN + SPC/E):

```
$GMX pdb2gmx -f alanine-dipeptide.pdb -o dipeptide.gro -p topol.top -i posre.itp -ff amber99sb-ildn -water spce
```

2. Define a box and solvate:

```
$GMX editconf -f dipeptide.gro -o boxed.gro -c -d 1.0 -bt cubic
$GMX solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top
```

3. Energy minimization:

```
$GMX grompp -f em.mdp -c solvated.gro -p topol.top -o em.tpr
$GMX mdrun -deffnm em
```

4. NPT equilibration:

```
$GMX grompp -f npt.mdp -c em.gro -p topol.top -o npt.tpr
$GMX mdrun -deffnm npt
```

5. Production (full ML):

```
$GMX grompp -f grompp.mdp -c npt.gro -p topol.top -o md.tpr
$GMX mdrun -deffnm md
```

6. ML/MM production:

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

## Analysis

Compare RMSF between full ML and ML/MM:

RMSF (root-mean-square fluctuation) measures how much each atom or residue moves around its average position over the trajectory. In biomolecular simulations it is commonly used to identify flexible vs rigid regions, compare dynamics between conditions, and detect how modeling choices (like forcefields) affect local mobility.

```
$GMX rmsf -f md.xtc -s md.tpr -o rmsf-ml.xvg
$GMX rmsf -f md-mlmm.xtc -s md-mlmm.tpr -o rmsf-mlmm.xvg
```

## Expected checks

- `em.gro`, `npt.gro`, `md.xtc`, and `md-mlmm.xtc` are created
- RMSF differs mainly for the dipeptide region
- ML/MM production is faster than full ML

## Outputs and logs

Monitor the terminal output while the simulation runs, then check the log files. With `-deffnm em`, `npt`, and `md`, GROMACS writes `em.log`, `npt.log`, and `md.log`. Instantaneous temperature and pressure fluctuate and are not meaningful on their own; check time-averaged values instead.

## Notes

- If you are new to GROMACS, focus on how MDP files define each stage.
- If you are experienced, pay attention to how the ML/MM region is defined and how it affects RMSF.