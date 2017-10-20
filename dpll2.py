import util
import copy

# if a clause has a single unassigned value we can assign it now
def propogate(formula):
    for line in formula:
        clause = line[0]
        local_result = False
        unassigned_num = 0
        unassigned = 0
        for i in range(0, len(clause)):
            if str(clause[i]) != 'False' and str(clause[i]) != 'True':
                print(clause[i])
                unassigned_num = unassigned_num + 1
                unassigned = i
            else:
                local_result = local_result or clause[i]
        if unassigned_num == 1:
            clause[unassigned] = True

    return formula

def empty(formula):
    want_dict = {}
    for line in formula:
        clause = line[0]
        unassigned_num = 0
        unassigned = 0
        local_result = False
        for i in range(0, len(clause)):
            if str(clause[i]) != 'False' and str(clause[i]) != 'True':
                unassigned_num = unassigned_num + 1
                unassigned = i
            else:
                local_result = local_result or clause[i]
        if unassigned_num == 1 and not local_result:
            if clause[unassigned] < 0:
                want = False
            else:
                want = True
            if abs(clause[unassigned]) in want_dict:
                if want == want_dict[abs(clause[unassigned])]:
                    continue 
                else:
                    return False
            else:
                want_dict[abs(clause[unassigned])] = want

