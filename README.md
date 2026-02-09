# Molecular Dynamics Engine Hands-on Tutorial 🔬

This hands-on session introduces three MD engines through short, guided exercises on the Kuma cluster. You'll run the same ML potential with different engines and compare workflows, performance, and outputs. The systems we will study are liquid water and an alanine dipeptide simulations the PET-MAD potential.

Before asking the instructor for help, try:
- A quick web search 🔍
- Asking an LLM 🤖
- Discussing with your partner 💬

Remember: debugging is part of the learning process, so don't stress if things don't work immediately!

## Session setup ⚙️

Clone the repository and navigate to the `hands-on/` folder:

```bash
git clone https://github.com/PicoCentauri/md-handson.git
cd md-handson
```

Start an interactive Slurm session

```bash
srun --time=02:00:00 --nodes=1 --ntasks=1 --mem-per-gpu=90G --gres=gpu:1 --partition=l40s --pty bash -c "set +e; exec bash"
```

**What's happening?** This starts a 2-hour interactive session with one node, one task, one GPU, and 90 GB GPU memory on the `l40` partition, and opens a bash shell on the allocated node. The `set +e` disables exit-on-error, allowing the session to persist after command failures. Time to get your hands dirty! 🚀

Load modules including Python and OpenMPI with CUDA support:

```
module purge
module load gcc
module load python
module load openmpi/5.0.3-cuda
```

Create a virtual environment and install tools:

```bash
python -m venv .venv
source .venv/bin/activate
pip install metatrain ipi "torch<2.8"
```

Fetch the PET-MAD ML potential once in the repo root:

```bash
mtt export https://huggingface.co/lab-cosmo/upet/resolve/main/models/pet-mad-s-v1.0.2.ckpt -o model.pt
```

**What's this?** We're downloading a pre-trained PET-MAD potential from HuggingFace. You'll symlink or copy `model.pt` into each engine folder as needed. One model, to rule them all! 🎯

Reference solutions are available in the `solutions/` folder (but try solving it yourself first! 😉).

## Simulation conditions 🌡️

The PET-MAD potential is trained with PBE-sol reference data, so we're running liquid water simulations at 450 K in this hands-on. Just remember: instantaneous temperature and pressure jump around like crazy in MD – only time-averaged values should match the target conditions!

## What is a topology? 🔗

In MD, a topology describes how atoms are connected and which interaction parameters apply. Think of it as the "rulebook" for your system. It typically includes bonded terms (bonds, angles, dihedrals) and nonbonded parameters (charges, atom types). The structure file gives you the coordinates (where things are), while the topology provides the force field definition (how they interact).

## Why not use ASE for MD here? 🤔

ASE is excellent for prototyping and single-point calculations, but it's not optimized for long, high-performance MD runs. Think of it like using a bicycle vs. a race car – both work, but one is way faster for the track! MD engines provide faster kernels, more flexible integration schemes, and better-tested thermostat and barostat implementations. For this session, we're focusing on engine-level workflows and performance rather than high-level wrappers.

## Engine overview 🎮

| Engine | Focus | Why it matters |
| --- | --- | --- |
| LAMMPS 💪 | Materials workhorse, GPU performance | Flexible input scripts and scalable performance |
| i-PI 🐍 | Advanced sampling, PIMD | Decouples force engines and enables path integrals |
| GROMACS 🧬 | Biomolecular MD, ML/MM | Mature bio workflows with hybrid ML/MM support |

## Usual MD workflow 🛠️

TODO: Explain that MD is like setting up an experiment: you prepare your system, choose your conditions, and then run the simulation to collect data. The typical stages are:
