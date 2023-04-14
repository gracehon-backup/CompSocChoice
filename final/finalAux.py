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
    
