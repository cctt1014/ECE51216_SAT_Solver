import os
import logging
import argparse
from dpll_solver import solve_sat

def solve_sat_dataset(foldername):
    """
    Solves all SAT problems in a given folder.
    
    Args:
        foldername (str): Path to the folder containing CNF files.
        
    Returns:
        None
    """
    # Check if the folder exists
    if not os.path.isdir(foldername):
        logging.error(f"Folder \"{foldername}\" does not exist.")
        return
    
    # Check if the folder is empty
    if not os.listdir(foldername):
        logging.error(f"Folder \"{foldername}\" is empty.")
        return
    
    # Iterate through all files in the folder
    all_pass = True
    for filename in os.listdir(foldername):
        if filename.endswith(".cnf"):
            filepath = os.path.join(foldername, filename)
            logging.info(f"Solving {filepath}")
            if solve_sat(filepath) == -1:
                all_pass = False
                logging.error(f"Failed to solve {filepath}")
            elif solve_sat(filepath) != 0 and filename.beginswith("uuf"):
                all_pass = False
                logging.error(f"Failed to solve UNSAT problem {filepath}")
    
    if all_pass:
        logging.info("All SAT problems in the folder were solved successfully.")
    else:
        logging.error("Some SAT problems in the folder could not be solved.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="count")
    parser.add_argument('files', metavar='f', type=str, nargs=1,
                    help='CNF file to test for satisfiability')
    args = parser.parse_args()
    if args.verbosity == 2:
        logging.basicConfig(filename=f'logs/{os.path.basename(args.files[0])}.log', filemode="w", level=logging.DEBUG)
    elif args.verbosity == 1:
        logging.basicConfig(filename=f'logs/{os.path.basename(args.files[0])}.log', filemode="w", level=logging.INFO)
    else:
        logging.basicConfig(filename=f'logs/{os.path.basename(args.files[0])}.log', filemode="w", level=logging.WARN)

    if not (os.path.isfile(args.files[0]) or os.path.isdir(args.files[0])):
        logging.error("Input file/folder name \"{}\" does not exists.".format(args.files[0]))
        exit(1)
    
    if os.path.isdir(args.files[0]):
        solve_sat_dataset(args.files[0])
    else:
        sat = solve_sat(args.files[0]) # "/path/to/input_file.cnf"
