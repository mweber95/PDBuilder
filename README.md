# PDBuilder

This tool provides an easy-to-use and efficient way to delete unnecessary TERs, adding chain identifiers, removing
RNA/DNA notation in front of the bases and/or adding them.

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

3.) This tool includes **five** main functionalities:
* a) removing unnecessary TERs in the PDB file
  * done with flag -t
* b) adding a chain identifier if none is given
  * done with flag -c
* c) removing R/D in front of bases
  * done with flag -rrd
* d) add D in front of bases
  * done with flag -ad
* e) add R in front of bases
  * done with flag -ar

Example of doing three things at once:

```shell
python3 main.py -t -c -rd -i example_input.pdb -o example_output.pdb
```

**Note:** c) d) and e) are mutually exclusive arguments ... this means you can only use one argument at a time
(which is the only meaningful use of this anyway)