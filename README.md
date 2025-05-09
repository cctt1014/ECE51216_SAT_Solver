# ECE51216_SAT_Solver
Due May 9


## File structure
1. `main.py`: Main entry point for the program.
2. `src/`: Contains the source code for the SAT solver.
   - `dpll_solver.py`: Implementation of the DPLL SAT solver.
   - `dpll_watched.py`: Implementation of the DPLL solver with watched literals.
3. `data/`: Contains datasets for testing the SAT solver.
4. `logs/`: Contains log files generated during SAT solver runs.

## Datasets
1. uf20-91: Uniform Random-3-SAT, 20 variables, 91 clauses - 1000 instances, all satisfiable [PASS]
2. RTI_k3_n100_m429: Random-3-SAT Instances and Backbone-minimal Sub-instances, 100 variables, 429 clauses - 500 instances, all satisfiable 
3. sw100-8-lp0-c5: "Morphed" Graph Colouring, 5 colourable, 100 vertices, 400 edges, p=1 - 100 instances, all satisfiable
4. uuf50-218: 50 variables, 218 clauses - 1000 instances, all unsat [PASS]
5. uf250-1065: 250 variables, 1065 clauses - 100 instances, all sat

## Test run command
```shell
python3 src/main.py "data/uf20-91/uf20-01.cnf"
python3 src/main.py "data/RTI_k3_n100_m429/RTI_k3_n100_m429_0.cnf"
python3 src/main.py "data/sw100-8-lp0-c5/SW100-8-0/sw100-1.cnf"
python3 src/main.py "data/toy.cnf"
```

```shell
-solver_option=1
```

```shell
python3 src/main.py "data/uf20-91/uf20-01.cnf" -solver_option=2 -vv
python3 src/main.py "data/RTI_k3_n100_m429/RTI_k3_n100_m429_0.cnf" -solver_option=1 -vv
python3 src/main.py "data/sw100-8-lp0-c5/SW100-8-0/sw100-1.cnf" -solver_option=1 -vv
python3 src/main.py "data/toy.cnf" -solver_option=1 -vv
```

```shell
python3 src/main.py "data/uf20-91" -solver_option=2 -vv
```