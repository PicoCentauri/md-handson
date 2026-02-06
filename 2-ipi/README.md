# i-PI engine 🐍

## About i-PI

i-PI is a Python-based driver for advanced MD techniques. The name reflects its focus on path integrals (PIMD) and its lightweight, hackable architecture (plus, it's written in Python, hence the snake 🐍). It separates the integrator from the force engine, which makes it super easy to connect to many force providers and to experiment with advanced sampling methods. Think of it as the Swiss Army knife of MD! 🔪

## Goals 🎯

- Learn the i-PI workflow with an external force engine
- Compare classical MD vs PIMD (nuclear quantum effects, anyone? 🧠)
- Analyze RDFs with MDAnalysis

## System 💧

We use a small liquid water box with 32 molecules in periodic boundary conditions. The system is intentionally tiny to make classical MD and PIMD runs fast during the session. The PET-MAD potential is trained with PBE-sol reference data, so runs target 450 K. Nuclear quantum effects in water? Yeah, that's a thing! 🎉

## Files

- `water.xyz`: pre-built liquid water system
- Input XML files: TODO (to be provided by the instructor)

## Exercise outline 🏃

This section will be completed with the input XML files and exact commands. The key idea is to compare a classical MD run to a PIMD run on the same water system and then analyze how the RDF (radial distribution function) changes. Spoiler: quantum effects make water weirder! 😅

1. Classical MD run (TODO: input and commands)
2. PIMD run (TODO: input and commands)
3. RDF comparison with MDAnalysis (TODO: scripts and expected trends)

## Notes 📌

- If you already know i-PI: focus on the force engine connection and the RDF comparison. Can you spot the quantum effects?
- If you're new: focus on the structure of the XML input and the role of the driver. XML might look scary at first, but it's actually pretty logical!
- Remember: i-PI is all about flexibility and advanced methods, so don't be afraid to experiment later! 🚀
