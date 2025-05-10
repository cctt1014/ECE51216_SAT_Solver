# ECE51216_SAT_Solver
## Overview
This repository contains a SAT solver implemented in Python, designed to solve the SAT problem using the DPLL algorithm. The solver can handle CNF (Conjunctive Normal Form) formulas in DIMACS format and includes heuristics such as two watched literals and clause learning. 

## File structure
1. `src/`: Contains the source code for the SAT solver.
   - `dpll_solver.py`: Implementation of the DPLL SAT solver.
   - `dpll_watched.py`: Implementation of the DPLL solver with watched literals.
   - `main.py`: Main entry point for the program.
   - `utils.py`: Utility functions for parsing CNF files and other helper functions.
   - `input_parser.py`: Parses the input CNF files and converts them into a suitable format for the solver.
2. `data/`: Contains datasets for testing the SAT solver.
3. `logs/`: Contains log files generated during SAT solver runs in our tests for result analysis.

## Quick Start
### Run our best SAT solver with the following command format:
```shell
python3 src/main.py <path_to_your_cnf_file>
```
### To run the best solver with a specific dataset in this code repository, use the following command:
```shell
python3 src/main.py <data/dataset_folder/instance_file.cnf>
```
### Example command to run with a CNF file:
```shell
python3 src/main.py "data/UF50.218.1000/uf50-01.cnf"
```

## Input Options
The SAT solver accepts the following command-line arguments if you need to customize the run:
   - `-v` or `--verbosity`: Increase output verbosity.
   - `-solver_option`: Choose between the DPLL solver (0) or the enhanced solver with watched literals and VSIDS (1).
   - `-max_files`: Specify the maximum number of files to process in a dataset. The default is None, which means all files will be processed. Only applicable when the input is a folder.

### Example command to run with options:
This command runs the best SAT solver on the instance `uf50-01.cnf` in the dataset `UF50.218.1000`:
```shell
python3 src/main.py "data/UF50.218.1000/uf50-01.cnf" -solver_option 1
```

Moreover, our SAT solver can take in an entire folder. This command runs the basic DPLL solver on the dataset `UF50.218.1000` with only 10 instances in the `UF50.218.1000` folder:
```shell
python3 src/main.py "data/UF50.218.1000" -solver_option 0 -max_files 10
```



## Datasets
1. Uniform Random-3-SAT
   1. UF50.218.1000: 50 variables, 218 clauses - 1000 instances, all sat
   2. UUF50.218.1000: 50 variables, 218 clauses - 1000 instances, all unsat
   3. UF75.325.100: 75 variables, 325 clauses - 100 instances, all sat
   4. UUF75.325.100: 75 variables, 325 clauses - 100 instances, all unsat
   5. UF100.430.100: 100 variables, 430 clauses - 100 instances, all sat
   6. UUF100.430.100: 100 variables, 430 clauses - 100 instances, all unsat

2. SAT-encoded "Morphed" Graph Colouring Problems
   1. sw100-8-2: 100 vertices, 400 edges, p=2^-2 - 100 instances, all satisfiable
   2. sw100-8-4: 100 vertices, 400 edges, p=2^-4 - 100 instances, all satisfiable
   3. sw100-8-8: 100 vertices, 400 edges, p=2^-6 - 100 instances, all satisfiable

3. Planning
   1. theblocksworld: 7 instances, all satisfiable
   2. logistics: 3 instances, all satisfiable