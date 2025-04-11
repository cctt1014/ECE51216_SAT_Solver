import logging
import os
import random
from enum import Enum
from input_parser import input_parser


class Status(Enum):
    """
        Status enum contains 3 status of a clause for showing whether it has been satisfied
    """
    UNRESOLVED = 1
    SATISFIED = 2
    UNSATISFIED = 3

class SATSolver():
    """
        SATSolver class stores SAT solver configurations, 
        input data and searching algorithms.
    """
    def __init__(self):
        self.n_vars = 0
        self.n_clauses = 0
        self.cnf = [] # A list of arrays representing input CNF data
        self.clause_status = [] # current clause status
        self.unassigned_var_list = []
        self.assign_stack = [] # A stack keeping var assignments
        self.implications = [] # A list records all forced decisions at one node

    
    def setup_solver(self, fpath):
        """
            Setup SAT solver with input CNF file
        """
        if not (os.path.isfile(fpath)):
            logging.error("Input CNF file \"{}\" does not exists or it is a folder.".format(fpath))
            return -1

        # Read CNF file and parse it
        self.cnf, self.n_vars, self.n_clauses = input_parser(fpath)

        logging.info("Number of variables: {}\n Number of clauses: {}".format(self.n_vars, self.n_clauses))
        
        # Init curr sat status for each clause
        for _ in self.cnf:
            self.clause_status.append(Status.UNRESOLVED)

        # Init unassigned variable list
        for i in range(1, self.n_vars+1):
            self.unassigned_var_list.append(i)

    def dpll(self):
        """
            Run DPLL algorithm for given CNF to find the assignment
        """
        while (len(self.unassigned_var_list) != 0):
            # Pick a variable assignment assignment
            if (len(self.implications) != 0):
                for a in self.implications:
                    if ((-1*a) in self.implications):
                        logging.info("Implication leads to conflict, backtracking...")
                        self.implications = [] # TODO It hurts efficiency, further enhancement expected
                        self.backtrack()
                
                self.assign_stack.append(self.implications.pop())
            else:
                # Traverse negative assignment first by default, push negative assignment to the stack
                self.assign_stack.append((self.pick_a_var_randomly())*(-1))

            # Update sat status after new assignment
            for i, status in enumerate(self.clause_status):
                match status:
                    case Status.UNRESOLVED:
                        unsat_lit_cnt = 0
                        unres_lit = 0 # record one single unresolved literal, works when implication triggered

                        for literal in self.cnf[i]:
                            if (literal in self.assign_stack):
                                self.clause_status[i] = Status.SATISFIED
                                break
                            elif ((-1*literal) in self.assign_stack):
                                unsat_lit_cnt += 1
                            else:
                                unres_lit = literal

                        if (unsat_lit_cnt == len(self.cnf[i])-1): # condition to trigger forced implication
                            logging.info("current assignment {} + clause {} -> implication {}".format(self.assign_stack[-1], self.cnf[i], unres_lit))
                            self.implications.append(unres_lit)
                    case Status.SATISFIED:
                        continue
                    case _:
                        logging.error("Invalid clause status found at index[{}]: {}".format(i, status))
                        


    def pick_a_var_randomly(self):
        """
            Dummy picking stratgy, will be replaced by some heuristics
        """
        if (len(self.unassigned_var_list) == 0):
            logging.error("Run out of variables for assignment!")

        var = random.choice(self.unassigned_var_list)

        return var
    
    def backtrack(self):
        """
            Backtracking current assignment stack to recover a parent node
        """
        # Backtrack base case
        if (len(self.assign_stack) == 0):
            logging.info("Backtrack reaches root, given CNF is UNSAT.")
            return -1

        # Pop out current literal
        curr_lit = self.assign_stack.pop()
        logging.info("Backtracking pops out literal {}".format(curr_lit))

        return_val = 0
        if (curr_lit < 0): # try another value
            self.implications.append(curr_lit*-1)
        else:
            return_val = self.backtrack()

        for i, status in enumerate(self.clause_status):
            if ((status == Status.SATISFIED) and (curr_lit in self.cnf[i])):
                sat_lit_cnt = 0
                for literal in self.cnf[i]:
                    if (literal in self.assign_stack):
                        sat_lit_cnt += 1
                if (sat_lit_cnt == 0):        
                    self.clause_status[i] = Status.UNRESOLVED

        return return_val
