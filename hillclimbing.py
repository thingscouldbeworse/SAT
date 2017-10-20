import util

import copy

# returns the literal which produces the highest score when flipped
def get_best_flip(formula, var_dict, old_score = 0):

    best_score = old_score
    best_literal = 0
    for line in formula:
        clause = line[0]
        for literal in clause:
            var_dict_copy = copy.copy(var_dict)
            var_dict_copy[abs(literal)] = not var_dict_copy[abs(literal)] 
            new_formula, new_result, new_score = util.check_formula(formula, var_dict_copy)
            if new_score > best_score:
                best_score = new_score
                best_literal = literal
   
    return best_literal, best_score

# run the hill climbing algorith
# given a formula, run through picking the literal to flip that will most improve the score,
# stopping when the formula is solved or we hit a local maxima
def hill_climb(formula, var_dict, max_flips = 10000, pp=False):

    formula, result, old_score = util.check_formula(formula, var_dict)
    maxima = 0
    for i in range(0, max_flips):
        new_literal, new_score = get_best_flip(formula, var_dict)
        var_dict[abs(new_literal)] = not var_dict[abs(new_literal)]
        formula, result, score = util.check_formula(formula, var_dict)
        if score > old_score:
            if pp: 
                print("Improvement made, %s" % score)
        else:
            if pp:
                print("Local Maxima")
            maxima = maxima + 1
        if result:
            return formula, result, score, i
        elif maxima > 2:
            print("Local maxima found at score %s" % score)
            return formula, result, score, i              
        old_score = score
    # no improvement made, local maxima
    if pp:
        print("Local maxima found at score %s" % score)
    return formula, result, score, i       
