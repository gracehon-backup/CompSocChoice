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