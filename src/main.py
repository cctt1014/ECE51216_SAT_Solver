import os
import logging
import argparse
import time
import psutil  # Add this import for memory usage tracking
import csv  # Add this import for CSV writing
from dpll_solver import solve_sat_dpll
from dpll_watched import solve_sat_wl


def solve_sat(filename, option=0):
    """
        Solves a SAT problem using the specified solver.
        Args:
            filename (str): Path to the CNF file.
            option (int): Solver option (0 for DPLL, 1 for CDCL).
        Returns:
            int: 0 if UNSAT, 1 if SAT, -1 if an error occurred.
    """
    # Setup timing and memory tracking
    process = psutil.Process(os.getpid())  # Get the current process
    start_time = time.time()  # Start the timer
    start_memory = process.memory_info().rss  # Get initial memory usage

    # Check which solver to use
    if option == 0:
        logging.info("Using DPLL solver.")
        result = solve_sat_dpll(filename)
    elif option == 1:
        logging.info("Using DPLL with watched literals solver.")
        result = solve_sat_wl(filename)
    else:
        logging.error("Invalid solver option. Use 0 for DPLL or 1 for CDCL.")
        return -1

    # Check the result and record it
    end_time = time.time()  # End the timer
    end_memory = process.memory_info().rss  # Get final memory usage

    runtime = end_time - start_time
    memory_used = (end_memory - start_memory) / 1024  # Convert to KB

    logging.info(f"Runtime: {runtime:.4f} seconds")
    logging.info(f"Memory used: {memory_used:.4f} KB")

    return result, runtime, memory_used

def solve_sat_dataset(foldername, option=0, max_files=None):
    """
    Solves all SAT problems in a given folder and saves runtime and memory usage data into a CSV file.
    
    Args:
        foldername (str): Path to the folder containing CNF files.
        option (int): Solver option (0 for DPLL, 1 for CDCL, 2 for DPLL with watched literals).
        max_files (int, optional): Maximum number of files to process. If None, process all files.
        
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
    
    # Prepare CSV file for writing
    csv_filename = os.path.join(foldername, "solver_metrics.csv")
    with open(csv_filename, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header row
        csv_writer.writerow(["Filename", "Result", "Runtime (s)", "Memory Usage (KB)"])
        
        # Initialize metrics
        total_runtime = 0
        total_memory = 0
        peak_runtime = 0
        peak_memory = 0
        file_count = 0
        all_pass = True

        # Iterate through all files in the folder
        for filename in os.listdir(foldername):
            if filename.endswith(".cnf"):
                if max_files is not None and file_count >= max_files:
                    logging.info(f"Reached the maximum number of files to process: {max_files}")
                    break

                filepath = os.path.join(foldername, filename)
                logging.info(f"Solving {filepath}")
                result, runtime, memory = solve_sat(filepath, option)
                
                if result == -1:
                    all_pass = False
                    logging.error(f"Failed to solve {filepath}")
                elif result != 0 and filename.startswith("uuf"):
                    all_pass = False
                    logging.error(f"Failed to solve UNSAT problem {filepath}")
                
                # Write data to CSV
                csv_writer.writerow([filename, result, runtime, memory])
                
                # Update metrics
                total_runtime += runtime
                total_memory += memory
                peak_runtime = max(peak_runtime, runtime)
                peak_memory = max(peak_memory, memory)
                file_count += 1

        # Calculate averages
        if file_count > 0:
            avg_runtime = total_runtime / file_count
            avg_memory = total_memory / file_count
            logging.info(f"Average Runtime: {avg_runtime:.4f} seconds")
            logging.info(f"Average Memory Usage: {avg_memory:.4f} KB")
            logging.info(f"Peak Runtime: {peak_runtime:.4f} seconds")
            logging.info(f"Peak Memory Usage: {peak_memory:.4f} KB")
        else:
            logging.warning("No valid CNF files found in the folder.")

        if all_pass:
            logging.info("All SAT problems in the folder were solved successfully.")
        else:
            logging.error("Some SAT problems in the folder could not be solved.")

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="count")
    parser.add_argument('files', metavar='f', type=str, nargs=1,
                    help='CNF file to test for satisfiability')
    parser.add_argument('-solver_option', type=int, default=1,
                    help='0 for DPLL, 1 for enhanced solver with watched literals and VSIDS')
    parser.add_argument('-max_files', type=int, default=None,
                    help='Maximum number of files to process in a dataset')
    args = parser.parse_args()
    
    # Set up logging
    if args.verbosity == 2:
        logging.basicConfig(filename=f'logs/{os.path.basename(args.files[0])}.log', filemode="w", level=logging.DEBUG)
    elif args.verbosity == 1:
        logging.basicConfig(filename=f'logs/{os.path.basename(args.files[0])}.log', filemode="w", level=logging.INFO)
    else:
        logging.basicConfig(filename=f'logs/{os.path.basename(args.files[0])}.log', filemode="w", level=logging.WARN)

    # Check if the input file/folder exists
    if not (os.path.isfile(args.files[0]) or os.path.isdir(args.files[0])):
        logging.error("Input file/folder name \"{}\" does not exists.".format(args.files[0]))
        exit(1)

    # Check if the input file is a CNF file or a dataset folder
    if os.path.isdir(args.files[0]):
        solve_sat_dataset(args.files[0], args.solver_option, args.max_files)
    else:
        solve_sat(args.files[0], args.solver_option)
