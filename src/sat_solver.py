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
        self.decision_stack = [] # A stack keeping var assignments
        self.implications = [] # A list records all forced decisions at one node
        self.was_backtracked = []

    
    def setup_solver(self, fpath):
        """
            Setup SAT solver with input CNF file
        """
        if not (os.path.isfile(fpath)):
            logging.error("Input CNF file \"{}\" does not exists or it is a folder.".format(fpath))
            return -1

        # Read CNF file and parse it
        self.cnf, self.n_vars, self.n_clauses = input_parser(fpath)

        logging.info("Number of variables: {}, Number of clauses: {}".format(self.n_vars, self.n_clauses))
        
        # Init curr sat status for each clause
        self.clause_status = [Status.UNRESOLVED] * self.n_clauses

        # Init unassigned variable list
        for i in range(1, self.n_vars+1):
            self.unassigned_var_list.append(i)

        # Init backtrack record for each variable
        self.was_backtracked = [False] * self.n_vars

    def dpll(self):
        """
            Run DPLL algorithm for given CNF to find the assignment
        """
        while (len(self.unassigned_var_list) != 0 or len(self.implications) != 0):
            # Pick a variable assignment via implications or unassigned var list
            if (len(self.implications) != 0):
                imply_conflict = False
                for a in self.implications:
                    if ((-1*a) in self.implications):
                        logging.info("Implication leads to conflict for variable {}, backtracking...".format(abs(a)))
                        imply_conflict = True
                        break
                        
                if (not imply_conflict):
                    self.decision_stack.append(self.implications.pop())
                else:
                    for lit in self.implications:
                        if abs(lit) not in self.unassigned_var_list:
                            self.unassigned_var_list.append(abs(lit))
                    self.implications = [] # TODO It hurts efficiency, further enhancement expected
                    self.backtrack()
                    continue
            else:
                # Traverse negative assignment first by default, push negative assignment to the stack
                self.decision_stack.append((self.pick_a_var_randomly())*(-1))

            logging.info("Current decision list: {}".format(self.decision_stack))

            # Update sat status after new assignment
            for i, status in enumerate(self.clause_status):
                match status:
                    case Status.UNRESOLVED:
                        unsat_lit_cnt = 0
                        unres_lit = 0 # record one single unresolved literal, works when implication triggered

                        for literal in self.cnf[i]:
                            if (literal in self.decision_stack):
                                self.clause_status[i] = Status.SATISFIED
                                break
                            elif ((-1*literal) in self.decision_stack):
                                unsat_lit_cnt += 1
                            else:
                                unres_lit = literal

                        if (self.clause_status[i] != Status.SATISFIED and unsat_lit_cnt == len(self.cnf[i])-1): # condition to trigger forced implication
                            logging.info("current assignment {} + clause {} -> implication {}".format(self.decision_stack[-1], self.cnf[i], unres_lit))
                            self.implications.append(unres_lit)
                            if abs(unres_lit) in self.unassigned_var_list:
                                self.unassigned_var_list.remove(abs(unres_lit))
                    case Status.SATISFIED:
                        continue
                    case _:
                        logging.error("Invalid clause status found at index[{}]: {}".format(i, status))
                        
        logging.info("RESULT:SAT")
        print("RESULT: SAT")
        
        output_str = "ASSIGNMENT:"
        for var in range(1, self.n_vars+1):
            var_str = "{}=".format(var)
            if (var in self.decision_stack):
                var_str += "1 "
            elif ((-1*var) in self.decision_stack):
                var_str += "0 "
            else:
                var_str += "1 "
            output_str += var_str
            
        logging.info(output_str)
        print(output_str)

        self.is_result_correct() # Verify SAT result

    def pick_a_var_randomly(self):
        """
            Dummy picking stratgy, will be replaced by some heuristics
        """
        if (len(self.unassigned_var_list) == 0):
            logging.error("Run out of variables for assignment!")

        var = random.choice(self.unassigned_var_list)
        
        self.unassigned_var_list.remove(var)

        return var
    
    def backtrack(self):
        """
            Backtracking current assignment stack to recover a parent node
        """
        # Backtrack base case
        if (len(self.decision_stack) == 0):
            logging.info("Backtrack reaches root, given CNF is UNSAT.")
            logging.info("RESULT:UNSAT")
            print("RESULT:UNSAT")
            exit()

        # Pop out current literal
        curr_lit = self.decision_stack.pop()
        logging.info("Backtracking pops out literal {}".format(curr_lit))

        return_val = 0
        if (not self.was_backtracked[abs(curr_lit)-1]): 
            # try another value for the same var
            self.was_backtracked[abs(curr_lit)-1] = True
            self.implications.append(curr_lit*-1)
        else:
            # push var back to unassigned list, further backtrack another literal
            self.was_backtracked[abs(curr_lit)-1] = False
            self.unassigned_var_list.append(abs(curr_lit))
            return_val = self.backtrack()

        # Recover clause status back to the stage before current literal decision
        for i, status in enumerate(self.clause_status):
            if ((status == Status.SATISFIED) and (curr_lit in self.cnf[i])):
                sat_lit_cnt = 0
                for literal in self.cnf[i]:
                    if (literal in self.decision_stack):
                        sat_lit_cnt += 1
                if (sat_lit_cnt == 0):
                    self.clause_status[i] = Status.UNRESOLVED

        return return_val

    def is_result_correct(self):
        self.clause_status = [Status.UNRESOLVED] * self.n_clauses
        
        logging.info("Final decision stack: {}".format(self.decision_stack))
        
        for i, clause in enumerate(self.cnf):
            for lit in clause:
                if (lit in self.decision_stack):
                    self.clause_status[i] = Status.SATISFIED
                    break
        
        all_good = True
        for i, status in enumerate(self.clause_status):
            if (status != Status.SATISFIED):
                all_good = False
                logging.info("Clause {} is not SAT".format(self.cnf[i]))
        
        if (all_good):
            logging.info("Decisions have been verified to satisfy all clauses!")
        else:
            logging.info("Some clauses are found to be UNSAT under given decisions...")
                
            