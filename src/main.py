import logging
import argparse
from sat_solver import SATSolver


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="count")
    parser.add_argument('files', metavar='f', type=str, nargs=1,
                    help='CNF file to test for satisfiability')
    args = parser.parse_args()
    if args.verbosity == 2:
        logging.basicConfig(filename='logs/SATSolver.log', filemode="w", level=logging.DEBUG)
    elif args.verbosity == 1:
        logging.basicConfig(filename='logs/SATSolver.log', filemode="w", level=logging.INFO)
    else:
        logging.basicConfig(filename='logs/SATSolver.log', filemode="w", level=logging.WARN)

    sat = SATSolver()
    sat.setup_solver(args.files[0])
    sat.dpll()

