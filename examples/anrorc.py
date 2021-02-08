from cat import GeneratorSet, ProjectedCayleyGraph
from cat.transformation import Transformation
from data.anrorc import dg, initmol


# The generator set obtained from the chemical network.
# The transformations were computed using an
# (unpublished version of) MØD but  can also be given directly.
# Each transformation have the form (id, left_map, right_map),
# mapping each atom id in left_map to the corresponding atom id,
# in right_map.
transformations = [
    Transformation(0, [1, 2, 3], [4, 5, 6]),
    Transformation(1, [4, 5, 6], [7, 8, 9]),
    Transformation(1, [7, 8, 9], [10, 11, 12]),
    Transformation(2, [10, 11, 12], [13, 14, 15]),
    Transformation(3, [2, 3, 16], [14, 13, 15])
]


# Construct ids for each nitrogen atom in the chemical network dg and
# store the given generator set.
gens = GeneratorSet(dg, transformations=transformations,
        fun_ignore=lambda v: v.stringLabel not in ("N", "N-"))

# Specify the atoms that should be tracked.
trace_atoms = [v for v in initmol.vertices if v.stringLabel == "N"]

# Construct and print the Projected Cayley Graph.
pcay = ProjectedCayleyGraph(trace_atoms, gens)
pcay.calc()
pcay.print()

# Find the paths in pcay that maps the nitrogens in initmol
# to the nitrogens in the product molecule.
paths = [pcay.find_path((2, 3), (14, 13)), pcay.find_path((2, 3), (14, 15))]

# Print the chemical network with global ids
# (pruning molecules with less than 3 atoms)
# and overlay the network with the found paths.
vis = lambda v: v.graph.numVertices >= 3
gens.print_dg(path_list=paths, vertex_visible=vis)



