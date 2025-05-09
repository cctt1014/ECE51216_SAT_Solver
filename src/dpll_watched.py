import sys
import logging
from collections import deque, defaultdict
from utils import validate_sat_solution
from input_parser import input_parser

class Clause:
    def __init__(self, lits):
        self.lits = lits
        # watch two positions (or same one twice if unit)
        self.w1 = 0
        self.w2 = 1 if len(lits) > 1 else 0

class SATSolver:
    def __init__(self, clauses, num_vars):
        self.num_vars = num_vars
        self.clauses = [Clause(c) for c in clauses]
        # build watchlist: literal -> list of Clause
        self.watchlist = {lit: [] for lit in range(-num_vars, num_vars+1) if lit != 0}
        for cl in self.clauses:
            l1, l2 = cl.lits[cl.w1], cl.lits[cl.w2]
            self.watchlist[l1].append(cl)
            if cl.w2 != cl.w1:
                self.watchlist[l2].append(cl)
        # assignment map: var -> bool
        self.assignment = {}
        # propagation queue of literals
        self.queue = deque()
        # trail of assigned literals for backtracking (stores lit)
        self.trail = []
        # decision level markers: positions in trail
        self.decision_levels = []
        # VSIDS activity: var -> float
        self.activity = defaultdict(float)
        # initialize activity by counting occurrences
        for cl in self.clauses:
            for lit in cl.lits:
                self.activity[abs(lit)] += 1.0
        # conflict tracking
        self.conflict_clause = None
        self.conflict_count = 0
        self.decay_period = 100    # decay every 100 conflicts
        self.decay_factor = 0.95   # multiply activities by this

    def assign(self, lit):
        """Assign lit=True, enqueue it, or detect immediate conflict."""
        v, val = abs(lit), (lit > 0)
        if v in self.assignment:
            return self.assignment[v] == val
        self.assignment[v] = val
        self.trail.append(lit)
        self.queue.append(lit)
        return True

    def propagate(self):
        """
        Two-watched-literals unit propagation.
        Returns True if no conflict, False otherwise.
        On conflict, self.conflict_clause is set to the conflicting clause's lits.
        """
        while self.queue:
            lit = self.queue.popleft()
            opp = -lit
            # copy list because we may modify watchlist
            for cl in list(self.watchlist[opp]):
                # determine which watch is opp
                if cl.lits[cl.w1] == opp:
                    i_opp, i_other = cl.w1, cl.w2
                else:
                    i_opp, i_other = cl.w2, cl.w1
                other_lit = cl.lits[i_other]
                moved = False
                # try to find a new literal to watch
                for i, l in enumerate(cl.lits):
                    if i == cl.w1 or i == cl.w2:
                        continue
                    val = self.assignment.get(abs(l))
                    if val is None or val == (l > 0):
                        # move watch
                        self.watchlist[opp].remove(cl)
                        if i_opp == cl.w1:
                            cl.w1 = i
                        else:
                            cl.w2 = i
                        self.watchlist[l].append(cl)
                        moved = True
                        break
                if moved:
                    continue
                # no watch move -> clause is unit or conflict
                val_other = self.assignment.get(abs(other_lit))
                if val_other is not None and val_other != (other_lit > 0):
                    # conflict
                    self.conflict_clause = cl.lits
                    return False
                # unit-propagate other_lit
                if val_other is None:
                    if not self.assign(other_lit):
                        self.conflict_clause = cl.lits
                        return False
        return True

    def backtrack(self):
        """Undo assignments down to the last decision level."""
        if not self.decision_levels:
            return
        lvl = self.decision_levels.pop()
        while len(self.trail) > lvl:
            lit = self.trail.pop()
            v = abs(lit)
            del self.assignment[v]
        # clear any outstanding queue
        self.queue.clear()

    def pick_branch_var(self):
        """Return the unassigned var with highest VSIDS activity, or None."""
        best = None
        best_score = -1.0
        for v, score in self.activity.items():
            if v not in self.assignment and score > best_score:
                best, best_score = v, score
        return best

    def all_clauses_satisfied(self):
        """Check if every clause has a true literal under current assignment."""
        for cl in self.clauses:
            sat = False
            for l in cl.lits:
                val = self.assignment.get(abs(l))
                if val is not None and val == (l > 0):
                    sat = True
                    break
            if not sat:
                return False
        return True

    def dpll(self):
        """Main recursive DPLL with trail-based backtracking and VSIDS branching."""
        if not self.propagate():
            # bump activity for vars in conflict clause
            self.conflict_count += 1
            for lit in self.conflict_clause:
                self.activity[abs(lit)] += 1.0
            # decay periodically
            if self.conflict_count % self.decay_period == 0:
                for v in self.activity:
                    self.activity[v] *= self.decay_factor
            return False

        if self.all_clauses_satisfied():
            return True

        var = self.pick_branch_var()
        if var is None:
            return True

        for lit in (var, -var):
            # mark decision level
            self.decision_levels.append(len(self.trail))
            if self.assign(lit) and self.dpll():
                return True
            # undo this branch
            self.backtrack()

        return False

def solve_sat_wl(filename):
    clauses, nv, nc = input_parser(filename)
    logging.info(f"Number of Variables: {nv}")
    logging.info(f"Number of Clauses: {nc}")

    solver = SATSolver(clauses, nv)
    is_sat = solver.dpll()
    print("RESULT:", end="")
    print("SAT" if is_sat else "UNSAT")
    if not is_sat:
        return 0
    else:
        assignment_list = []
        print("ASSIGNMENT: ", end="")
        for v in range(1, nv+1):
            val = 1 if solver.assignment.get(v, False) else 0
            print(f"{v}={val}", end=" ")
            assignment_list.append(v if val else -v)
        print("")
        
        if validate_sat_solution(clauses, assignment_list):
            logging.info("The solution is valid.")
            return 1
        else:
            logging.error("The solution is invalid.")
            return -1

# Example usage:
if __name__ == "__main__":
    # Replace the path below with the actual location of your .cnf file.
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\uf50-218\\uf50-05.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF50.218.1000\\uuf50-05.cnf"
    #filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UF250.1065.100\\uf250-01.cnf"
    filename = "C:\\Users\\hokie\\OneDrive - purdue.edu\\2025 Spring\\ECE 51216\\Project\\UUF250.1065.100\\uuf250-03.cnf"
    solve_sat_wl(filename)
