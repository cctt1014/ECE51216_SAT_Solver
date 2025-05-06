import os
import logging
import argparse
from dpll_solver import solve_sat_dpll
from cdcl_solver import solve_sat_cdcl
from dpll_watched_1 import solve_sat_wl

def solve_sat(filename, option=0):
    if option == 0:
        logging.info("Using DPLL solver.")
        return solve_sat_dpll(filename)
    elif option == 1:
        logging.info("Using CDCL solver.")
        return solve_sat_cdcl(filename)
    elif option == 2:
        logging.info("Using DPLL with watched literals solver.")
        sat = solve_sat_wl(filename)
        return sat
    else:
        logging.error("Invalid solver option. Use 0 for DPLL or 1 for CDCL.")
        return -1
    

def solve_sat_dataset(foldername, option=0):
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
            if solve_sat(filepath, option) == -1:
                all_pass = False
                logging.error(f"Failed to solve {filepath}")
            elif solve_sat(filepath, option) != 0 and filename.beginswith("uuf"):
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
    parser.add_argument('-solver_option', type=int, default=0,
                    help='0 for DPLL, 1 for CDCL, 2 for DPLL with watched literals')
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
        solve_sat_dataset(args.files[0], args.solver_option)
    else:
        sat = solve_sat(args.files[0], args.solver_option) # "/path/to/input_file.cnf"
