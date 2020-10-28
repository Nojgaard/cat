from cat import GeneratorSet, ProjectedCayleyGraph, SimplifiedCayleyGraph
from cat.transformation import Transformation
from data.simple_formose import dg, glycolaldehyde
import mod


# The generator set obtained from the chemical network.
# The transformations were computed using an
# (unpublished version of) MØD but  can also be given directly.
# Each transformation have the form (id, left_map, right_map),
# mapping each atom id in left_map to the corresponding atom id,
# in right_map.
transformations = [
    Transformation(0, [1, 2], [3, 4]),
    Transformation(1, [1, 2], [4, 3]),
    Transformation(2, [3, 4], [1, 2]),
    Transformation(3, [3, 4], [2, 1]),
    Transformation(4, [1, 2, 3, 4], [8, 7, 6, 5]),
    Transformation(5, [1, 2, 3, 4], [8, 7, 5, 6])
]

# Construct ids for each carbon atom in the chemical network dg and
# store the given generator set.
gens = GeneratorSet(dg, transformations=transformations,
                    fun_ignore=lambda v: v.stringLabel != "C")

# Print the chemical network with global ids assigned to each
# carbon atom, and overlay it with the given transformations.
print("Found transformations:", len(gens))
gens.print_dg(draw_trace=True)

# Specify the atoms that should be tracked.
trace_atoms = [v for v in glycolaldehyde.vertices if v.stringLabel == "C"]

# Construct and print the Projected Cayley Graph.
pcay = ProjectedCayleyGraph(trace_atoms, gens)
pcay.calc()

mod.postSection("Projected Cayley Graph")
pcay.print()

# Construct and print the Simplified Projected Cayley Graph.
scay = SimplifiedCayleyGraph(pcay)

mod.postSection("Simplified Cayley Graph")
scay.print()

