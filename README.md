# SignNet_Programming_Python
This repository contains the implementation of the SignNet research conducted by the Chair of Microeconomics at the University of Fribourg.


## Supported Input Formats

### Adjacency Matrix

The framework expects adjacency matrices in the following format:

|     | A | B | C |
|-----|---|---|---|
| A   | 0 | 1 | -1 |
| B   | 1 | 0 | 1 |
| C   | -1| 1 | 0 |

Requirements:

- The first row contains the node labels.
- The first column contains the node labels.
- Row and column labels must be identical.
- A value of `0` denotes the absence of an edge.
- Positive and negative values represent signed edges.

### Edge List

The framework expects edge lists in the following format:
	source	target	sign
	A	B	1
	B	C	1
	A	C	-1

Requirements:

- The first row contains the column headers (e.g., 'source', 'target', 'sign').
- Each subsequent row represents a distinct signed relationship between two nodes.
- The source and target columns contain the node labels.
- The sign column contains numerical values where positive and negative values represent signed edges.
- Missing combinations or a weight of 0 denote the absence of an edge.
