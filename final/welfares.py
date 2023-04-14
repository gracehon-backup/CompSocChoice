

def utalitarian_welfare(persons, projects):
    """Return the utilitarian welfare of a list of satisfactions."""
    total = 0
    for person in persons:
        total += sum([a for project, a in person.project_approvals.items() if project in projects])
    
    return total / (len(persons) * len(projects))

def chamberlin_courant_welfare(persons, projects):
    """Return the Chamberlin-Courant welfare of a list of satisfactions."""
    total = 0
    for person in persons:
        total += max([a for project, a in person.project_approvals.items() if project in projects])
    return total / len(persons)

def egalitarian_social_welfare(persons, projects):
    """Return the egalitarian social welfare of a list of satisfactions."""
    total = 0
    for person in persons:
        total += min([a for project, a in person.project_approvals.items() if project in projects])
    return total / len(persons)

def nash_welfare(persons, projects):
    """Return the Nash welfare of a list of satisfactions."""
    total = 0
    for person in persons:
        approval = sum([a for project, a in person.project_approvals.items() if project in projects])  
        total *= max(0, approval)
    return total / (len(persons) * len(projects))


    