import walksat
import util
import hillclimbing

import sys
import copy
import os
import time

def satisfy_dir(directory):
    all_results = []
    for file in os.listdir(directory):
        if file.endswith(".cnf"):
            formula, var_dict = util.read_dimacs(directory +"/"+ file)
           
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
           
            current = time.time()

            hill_formula, hill_result, hill_score, hill_flips = hillclimbing.hill_climb(formula, var_dict) 
            result = [directory+"/"+file,"HillClimb", hill_result, str(hill_score)+"/"+str(len(formula)), hill_flips, time.time() - current]
            print(result)
            all_results.append(result)

    return all_results

#formula, var_dict = util.read_dimacs(sys.argv[1])
#print(walksat.walk_sat(formula, var_dict, sys.argv[2],10000 ))
#print(hillclimbing.hill_climb(formula, var_dict))
satisfy_dir(sys.argv[1])
