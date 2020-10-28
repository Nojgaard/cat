# cat
CAT (Cayley Atom Tracker). A python package for
tracking atoms through chemical networks using projected Cayley graphs.

The code is published as part of the supplementary material to
the submitted paper "Cayley Graphs of Semigroups Applied to
Atom Tracking in Chemistry".

The presented version has atom maps of each reaction hardcoded.
These, have have been automatically 
computed with a version of [MØD](https://cheminf.imada.sdu.dk/mod/) to be release in future

## Requirements
The package depends on the sofware packages [MØD](https://cheminf.imada.sdu.dk/mod/)
and [NetworkX](https://networkx.org/).

## Usage
For details on how to use the package, see the example files found in this
repository. To run any of the files simply run: 
```
mod -f examples/anrorc.py
```
from the root folder.

<p align="center">
  <img src="https://github.com/Nojgaard/cat/blob/main/figs/anrorc_network.png" alt=""/>
</p>

