# WalkSAT implementation
import sys
import random
import util
import copy

def walk_sat(formula, var_dict, seed, max_flips=10000):
    # randomly assign values
    random.seed(seed)
    for var in var_dict:
        var_dict[var] = bool(random.randint(0,1))
    
    # get initial score with random values
    formula, result, score = util.check_formula(formula, var_dict)
    if result:
        return formula, result, score
    target_score = len(formula)
    
    # loop until solved or max_flips
    for i in range(0, max_flips):
        # get all unsatisfied clauses
        unsat = []
        for line in formula:
            if not line[1]:
                unsat.append(line)

        # choose a random unsolved clause
        target_pick = random.randint(0,len(unsat)-1)
        best_score = 0
        best_var_dict = []
        for literal in unsat[target_pick][0]:
            # choose literal within clause with highest score
            var_dict_copy = copy.copy(var_dict)
            var_dict_copy[abs(literal)] = not var_dict_copy[abs(literal)]
            new_formula, new_result, new_score = util.check_formula(formula, var_dict_copy)
            if new_score > best_score:
                best_score = new_score
                best_var_dict = var_dict_copy
        var_dict = best_var_dict
        formula, result, score = util.check_formula(formula, var_dict)
        if result:
            return formula, result, score, i

    formula, result, score = util.check_formula(formula, var_dict)
    return formula, result, score, i

