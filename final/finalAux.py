from final_project import Project

def filter(data):
    return [[vote[0] for vote in ballot if vote[1] > 0 ] for ballot in order(data)]

def order(data):
    ordereddata = data.copy()
    for i in range(len(ordereddata)):
        ordereddata[i].sort(reverse = True, key = lambda x: x[1])
    return ordereddata

def tied_vote(vote, eliminations):
    """
    Resolve a tied vote
    input:
        vote: list of ints (candidates)
        eliminations: list of ints (candidates that have been eliminated)
    output:
        vote: list of ints (candidates)"""

    # print(vote)
    if len(vote) == 1:
        return None if vote[0] in eliminations else [vote[0]]
    if vote[0] in eliminations and vote[1] in eliminations:
        return None
    if vote[0] in eliminations:
        return [vote[1]]
    if vote[1] in eliminations:
        return [vote[0]]
    return vote

def checkrank(ballot, a, b):
    if a in ballot and b in ballot:
        return 1 if ballot.index(a) < ballot.index(b) else 0
    elif a in ballot:
        return 1
    elif b in ballot:
        return -1
    else:
        return 0
    
def applyBudget(outputSCF,budget):
    affordable_projects = []
    for project in outputSCF:
        budget -= Project.INSTANCES[project].cost
        if budget < 0:
            return affordable_projects
        affordable_projects.append(project)
    return affordable_projects

def applyBudgetMaximally(outputSCF,budget):
    affordable_projects = []
    for project in outputSCF:
        if ((budget - Project.INSTANCES[project].cost) < 0):
            continue
        budget -= Project.INSTANCES[project].cost
        affordable_projects.append(project)
    return affordable_projects