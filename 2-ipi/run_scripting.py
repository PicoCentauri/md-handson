#!/usr/bin/python
from ipi.utils.scripting import InteractiveSimulation
from ipi.utils.depend import dstrip
import numpy as np
import ase, ase.io
import random

# Scripting simulations can also be initialized from an external XML template
with open("input-remd_direct.xml", "r", encoding="utf-8") as file:
    input_xml = file.read()

print("Running with XML input:\n\n", input_xml)

sim = InteractiveSimulation(input_xml)

sim.run(10)

print(f'potential now {sim.properties("potential")}')

# f**k up the ordering of the structures, just because
structures = sim.get_structures()
random.shuffle(structures)
sim.set_structures(structures)

sim.run(10)

print(f'potential now {sim.properties("potential")}')


