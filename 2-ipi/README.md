# I-PI engine

## About i-PI

i-PI is a Python-based driver for advanced MD techniques. The name reflects its focus on path integrals (PIMD) and its lightweight, hackable architecture. It separates the integrator from the force engine, which makes it easy to connect to many force providers and to experiment with advanced sampling methods.

## Goals

- Learn the i-PI workflow with an external force engine
- Compare classical MD vs PIMD
- Analyze RDFs with MDAnalysis

## System

We use a small liquid water box with 32 molecules in periodic boundary conditions. The system is intentionally tiny to make classical MD and PIMD runs fast during the session. The PET-MAD potential is trained with PBE-sol reference data, so runs target 450 K.

## Files

- `water.xyz`: pre-built liquid water system
- Input XML files: TODO (to be provided by the instructor)

## Exercise outline

This section will be completed with the input XML files and exact commands. The key idea is to compare a classical MD run to a PIMD run on the same water system and then analyze how the RDF changes.

1. Classical MD run (TODO: input and commands)
2. PIMD run (TODO: input and commands)
3. RDF comparison with MDAnalysis (TODO: scripts and expected trends)

## Notes

- If you already know i-PI, focus on the force engine connection and the RDF comparison.
- If you are new, focus on the structure of the XML input and the role of the driver.
