# PDBuilder

This tool provides an easy-to-use and efficient way to delete unnecessary TERs, adding chain identifiers and/or removing
RNA/DNA notation in front of the bases.

## How to use
1.) Clone the repository

2.) The execution of main.py requires two flags:  
* **a)** input_file with flag -i
* **b)** output_file with flag -o

Example:

```shell
python3 main.py -i example_input.pdb -o example_output.pdb
```

**Note:** This would do absolutely nothing because there are no operations for rebuilding specified :)

3.) This tool includes **three** main functionalities:
* a) removing unnecessary TERs in the PDB file
  * done with flag -t
* b) adding a chain identifier if none is given
  * done with flag -c
* c) removing R/D in front of bases
  * done with flag -rd

Example of doing all three things at once:

```shell
python3 main.py -t -c -rd -i example_input.pdb -o example_output.pdb
```
