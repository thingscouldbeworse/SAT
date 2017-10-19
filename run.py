import walksat
import util
import hillclimbing

import sys
import copy

formula, var_dict = util.read_dimacs(sys.argv[1])
print(walksat.walk_sat(formula, var_dict, sys.argv[2],10000 ))
