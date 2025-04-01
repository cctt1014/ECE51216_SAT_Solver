import logging
import os
    

class SATSolver():
    """
        SATSolver class stores SAT solver configurations, 
        input data and searching algorithms.
    """
    def __init__(self, cnf_fpath):
        self.config = {} # A dictionary of SAT solver configurations
        self.cnf = [] # A list of arrays representing input CNF data
        self.config, self.cnf = self.setup_solver(cnf_fpath)
        self.result = self.dpll()
    
    def setup_solver(self, fpath):
        """
            Setup SAT solver with input CNF file
        """
        if not (os.path.isfile(fpath)):
            logging.error("[ERROR] Input CNF file \"{}\" does not exists or it is a folder.".format(fpath))
            pass

        
        return {}, []

    def dpll(self):
        """
            Run DPLL algorithm for given CNF to find the assignment
        """
        pass

