import random
import glob
import os

# parse a dimacs file into a formula
def read_dimacs(filename):
    
    formula = []
    f = open(filename, 'r')
    nbvar, nbclauses = 0, 0
    var_dict = {}
    for line in f:
        if line[0] == 'c': # comment
            continue
        elif line[0] == 'p': 
            splitted = line.split(" ")
            nbvar, nbclauses = int(splitted[2]), int(splitted[3])
        else:
            clause = [ int(x) for x in line.split(" ")[1:] ]
            formula.append([clause[:-1],False])
            for var in clause[:-1]:
                var_dict[abs(var)] = False
    return formula, var_dict

def check_clause(clause, var_dict):
    values = []
    result = False
    for value in clause:
        if value > 0:
            values.append(var_dict[abs(value)])
        else:
            values.append(not var_dict[abs(value)])
    for value in values:
        result = result or value
    return result

def check_formula(formula, var_dict):
    result = True
    clauses_sat = 0
    for line in formula:
        clause = line[0]
        check_result = check_clause(clause, var_dict)
        result = result and check_result
        if check_result:
            clauses_sat = clauses_sat + 1
            line[1] = True
        else:
            line[1] = False

    return formula, result, clauses_sat

# open a directory of CNF files
def open_dir(directory):
    dimaces_list = []
    for file in os.listdir(directory):
       dimacs_list.append([read_dimacs(file)])

    return dimacs_list

