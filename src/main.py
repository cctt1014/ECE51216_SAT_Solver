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
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    sat = SATSolver(args.files[0]) # "/path/to/input_file.cnf"
