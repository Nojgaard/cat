# cat
CAT (Cayley Atom Tracker). A python package for
tracking atoms through chemical networks using projected Cayley graphs.

The code is published as part of the supplementary material to
the paper "Cayley Graphs of Semigroups Applied to
Atom Tracking in Chemistry", submitted to the Journal of Computational Biology.

In the current version, the atom maps of each reaction are hard-coded, but
the the automated generation of these atom maps will be part of
future release of a [MØD](https://cheminf.imada.sdu.dk/mod/).

## Requirements
The package depends on the sofware packages [MØD](https://cheminf.imada.sdu.dk/mod/)
and [networkx](https://networkx.org/).

## Usage
For details on how to use the package, see the example files found in this
repository. To run any of the files simply run: 
```
mod -f examples/anrorc.py
```
from the root folder.


