# SignNet_Programming_Python
This repository contains the implementation of the SignNet research conducted by the Chair of Microeconomics at the University of Fribourg.


## Supported Input Formats

### Adjacency Matrix (CSV)

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