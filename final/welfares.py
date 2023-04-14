
"""
This module contains the functions for calculating the different welfare functions.
"""

def utalitarian_welfare(persons, projects):
    """Return the utilitarian welfare of a list of satisfactions."""
    if len(projects) == 0:
        return 0
    total = 0
    for person in persons:
        total += sum([a for project, a in person.project_approvals.items() if project.instance in projects])
    
    return total / (len(persons) * len(projects))

def chamberlin_courant_welfare(persons, projects):
    """Return the Chamberlin-Courant welfare of a list of satisfactions."""
    if len(projects) == 0:
        return 0
    total = 0
    for person in persons:
        total += max([a for project, a in person.project_approvals.items() if project.instance in projects])
    return total / len(persons)

def egalitarian_social_welfare(persons, projects):
    """Return the egalitarian social welfare of a list of satisfactions."""
    if len(projects) == 0:
        return 0
    approvals = []
    for person in persons:
        approvals.append(sum([a for project, a in person.project_approvals.items() if project.instance in projects]))
    return min(approvals)

def nash_welfare(persons, projects):
    """Return the Nash welfare of a list of satisfactions."""
    if len(projects) == 0:
        return 0
    total = 1
    for person in persons:
        approval = sum([a for project, a in person.project_approvals.items() if project.instance in projects])  
        total *= min(1, approval)
    return total
