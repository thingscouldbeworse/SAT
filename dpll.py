import util
import copy

def propogate(formula, var_dict):
    
    for line in formula:
        clause = line[0]
        num_unassigned = 0
        unassigned = 0
        for literal in clause:
            if var_dict[abs(literal)] == None:
                num_unassigned = num_unassigned + 1
                unassigned = literal
            if num_unassigned > 1:
                break
        var_dict_copy = copy.copy(var_dict)
        if num_unassigned == 1: 
            # try true
            var_dict_copy[abs(unassigned)] = True
            result = util.check_clause(clause, var_dict_copy)
            if result:   
                # look for contradiction
                if contradiction(formula, var_dict_copy, unassigned):
                    var_dict_copy[abs(unassigned)] = None             
            else:
                # try false
                var_dict_copy[abs(unassigned)] = False
                result = util.check_clause(clause, var_dict_copy)
                if result:
                    if contradiction(formula, var_dict_copy, unassigned):
                        var_dict_copy[abs(unassigned)] = None
                else:
                    print("something went wrong")
                    return 0
            var_dict = var_dict_copy
    return var_dict

def contradiction(formula, var_dict, literal_to_flip):
    for line in formula:
        clause_result = False
        our_literal = False
        clause = line[0]
        for literal in clause:
            if literal == literal_to_flip:
                our_literal = True
            if literal < 0:
                clause_result = clause_result or not var_dict[abs(literal)]
            else:
                clause_results = clause_result or var_dict[abs(literal)]
        if our_literal:
            if clause_result == False:
                return True

