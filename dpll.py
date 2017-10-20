import util
import copy

# unit clauses (only one literal unassigned we know that literal's value
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

# a literal cannot be set if doing so would invalidate another clause
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

# if a literal appears with only one polarity, it must have that value
def pure_literal_elim(formula):
    literals = {}
    for line in formula:
        clause = line[0]
        for literal in clause:
            if abs(literal) not in literals:
                literals[abs(literal)] = literal / abs(literal)
            else:
                if literals[abs(literal)] == 'impure' or literal / abs(literal) != literals[abs(literal)]:
                    literals[abs(literal)] = 'impure'
    return literals

# empty clauses are clauses with all variables set, but still False
def empty(formula, var_dict):
    for line in formula:
        clause = line[0]
        result = False
        complete = True
        for literal in clause:
            if var_dict[abs(literal)] != None:
                if literal < 0:
                    result = result or not var_dict[abs(literal)]
                else:
                    result = result or var_dict[abs(literal)]
            else:
                complete = False
        if complete and not result:
            return True
    return False
        

# recursively apply DPLL
def dpll(formula, var_dict):
    new_formula, result, new_score = util.check_formula(formula, var_dict)
    if result:
        return result, var_dict
    if empty(formula, var_dict):
        return False, var_dict
    var_dict = propogate(formula, var_dict)
    unassigned = False
    for var in var_dict:
        if var_dict[var] == None:
            literal = var
            #print("Chose %s" % var)
            unassigned = True
            break
    #print(var_dict)
    if not unassigned:
        temp_formula, temp_result, temp_score = util.check_formula(formula, var_dict)
        if temp_result:
            return True, var_dict
        else:
            return False, var_dict
    var_dict_true = copy.copy(var_dict)
    var_dict_true[literal] = True
    var_dict[var] = False
    return dpll(formula, var_dict_true) or dpll(formula, var_dict)
