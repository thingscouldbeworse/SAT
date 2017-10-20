import walksat
import util
import hillclimbing
import dpll
import dpll2

import sys
import copy
import os
import time

def satisfy_dir(directory, walk=True, hill=True, deepee=True):
    all_results = []
    for file in os.listdir(directory):
        if file.endswith(".cnf"):
            formula, var_dict = util.read_dimacs(directory +"/"+ file)

            if walk:           
                for i in range(1, 11):
                    formula_walk = copy.copy(formula)
                    var_dict_walk = copy.copy(var_dict)
                    current = time.time()
                    try:
                        walk_formula, walk_result, walk_score, walk_flips = walksat.walk_sat(formula_walk, var_dict_walk, i, 5000)
                        result = [directory+"/"+file, "WalkSAT", walk_result, str(walk_score)+"/"+str(len(formula)), walk_flips, time.time() - current]
                    except:
                        result = [directory+"/"+file, "WalkSAT", "ERROR"]
                    print(result)
                    all_results.append(result)
            if hill: 
                current = time.time()

                hill_formula, hill_result, hill_score, hill_flips = hillclimbing.hill_climb(formula, var_dict) 
                result = [directory+"/"+file, "HillClimb", hill_result, str(hill_score)+"/"+str(len(formula)), hill_flips, time.time() - current]
                print(result)
                all_results.append(result)

            if deepee:
                current = time.time()
                for var in var_dict:
                    var_dict[var] = None
                for line in formula:
                    line[1] = None
                result, new_var_dict = dpll.dpll(formula, var_dict)
                new_formula, result, score = util.check_formula(formula, new_var_dict)
                if result == False:
                    result = "Unsatisfied"
                else:
                    result = "Satisfied"
                result = [directory+"/"+file, "DPLL", result, 'NA', 'NA', time.time() - current]
                print(result)
                all_results.append(result)
                
            
    return all_results

satisfy_dir(sys.argv[1], True, True, True)
