fifteen
=================

[![shields.io](https://img.shields.io/badge/pypi-0.0.2-violet?style=for-the-badge&logo=pypi)](https://pypi.org/project/table-five/) [![shields.io](https://img.shields.io/badge/made_with-rust-violet?style=for-the-badge&logo=rust)](https://pyo3.rs/v0.16.4/)

(DBA `table_fifth`)

> This is a research fork of the original library

Experimental library for quick quintet tallying, useful when you have a lot of quintets that somehow you don't want to count yourself.

## Usage

Binary wheels are provided on PyPI for Python starting from 3.7, but note that PyPy is not supported (yet).

```
python3 -m pip install table-five
```

## API

### `TreeSet`

A treeset is an efficient (i.e., fast parsing) list of tree topologies. The construction is $O(k n \lg n)$ where $k$ is the number of trees and $n$ the number of taxa. The log factor is due to the LCA data structure initialization.

```python
from table_five import TreeSet
trees = TreeSet("path_to_newline_delimited_newicks.tre")
```

#### Quintet Counting

The major API is `tally_single_quintet` returning a list of length 15 containing the empirical
counts of the 15 ADR unrooted quintet topology among the tree-set in $O(k)$ time:

```python
# get counts of the ADR unrooted quintet topologies on taxa '1','2','3','4','5'. Taxa order matters.
treeset.tally_single_quintet(('1','2','3','4','5'))
# obviously you might want to convert it to numpy arrays

# normalize by the number of genes in the tree-set
new_tree_dist = np.asarray(treeset.tally_single_quintet(q_taxa)) / len(treeset)
```

## Development and Building

After installing the Rust toolchain and [Maturin](https://www.maturin.rs/), see the following commands:

```bash
# build the library
maturin build
# installing it locally
maturin develop
```

See the Maturin documentation for more details.