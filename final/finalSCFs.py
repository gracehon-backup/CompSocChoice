from collections import Counter

def plurality(data, names, eliminations=[], standalone = False):
    """
    Plurality voting
    input:
        data: list of lists of ints (voters' votes)
        names: dict of ints to strings (candidate names)
        eliminations: list of ints (candidates that have been eliminated)
    output:
        winners: list of ints (candidate(s) with most votes)
        losers: list of ints (candidate(s) with least votes)
    """
    nr_votes = [0] * len(names)

    for ballot in data:                                         # For each ballot
        for candidate in ballot:                                # For first eligible candidate in the vote
            if type(candidate) == list:                         # In case of Split vote
                result = tied_vote(candidate, eliminations)
                if result is None:                              # Both candidates were eliminated,
                    continue                                    # continue to next candidate in ballot
                for c in result:
                    nr_votes[c] += 1/len(result)                # Add weighted vote to one or both candidates
                    break
                continue                                        # Both candidates were eliminated, continue to next candidate
            if candidate not in eliminations:
                nr_votes[candidate] += 1                        # Add vote to single candidate
                break

    # Find the winners and losers
    max_votes = max([i for i in nr_votes if nr_votes.index(i) not in eliminations])               # max(nr_votes) belongs to winner
    winners = [i for i in range(len(nr_votes)) if nr_votes[i] == max_votes]       # Find index of winners
    
    # Find the losers
    min_votes = float("inf")                                                      # Set min to infinity
    for idx, ballot in enumerate(nr_votes):
        if ballot < min_votes and idx not in eliminations and idx not in winners: # Lower than min, not eliminated and not a winner
            min_votes = ballot                                                    # Set new min

    # Eliminated if received min votes and not a winner
    losers = [i for i in range(len(nr_votes)) if  nr_votes[i] == min_votes 
                                              and i not in winners]

    if standalone:
        losers.extend(winners)
        return losers[::-1]
    
    return winners, losers

def STV(data, names, eliminations=[]):

    """
    Single Transferable Vote
    input:
        data: list of lists of ints (voters' votes)
        names: dict of ints to strings (candidate names)
        eliminations: list of ints (candidates to be eliminated)
    """
    winners, losers = plurality(data, names, eliminations)
    eliminations += losers                                     # Add the eliminated candidates to the list of eliminations
    if len(losers) == 0: 
        eliminations.extend(winners)
        return eliminations[::-1]                                          # No more candidates to eliminate, final round
    return STV(data, names, eliminations) 

def approval(data,names):
    
    nr_votes = [0] * len(names)                                 # everyone starts with zero votes

    for ballot in data:
        for vote in ballot:
            nr_votes[vote] += 1                                 # everytime someone approved, they gain a vote

    return([x[1] for x in sorted(((value, index) for index, value in enumerate(nr_votes)), reverse=True)]) # return winner

def condorcet(data,names):

    candidate_wins = [[0 for i in range(len(names))] for j in range(len(names))] # start with empty matrix

    for i in names:
        for j in names[names.index(i)+1:]: # pairwise comparison of candidates
            if j == i:
                continue
            wins_i = 0
            wins_j = 0
            for ballot in data:            # count wins against each other
                if i in ballot and j in ballot:
                    if ballot.index(i) < ballot.index(j):
                        wins_i += 1
                    else:
                        wins_j += 1
                elif i in ballot:
                    wins_i += 1
                elif j in ballot:
                    wins_j += 1                      
            if wins_i > wins_j:          # mark winner in matrix
                candidate_wins[i][j] = 1
            elif wins_i < wins_j:
                candidate_wins[j][i] = 1
    
    results = []
    i = 1
    while len(results) == 0 and i <= len(names)/2:    
        for row in candidate_wins:
            if sum(row) == len(names) - i:
                results.append(candidate_wins.index(row)) 
        i += 1

    return results 

def borda(data, names):

    points = [0] * len(names) # empty list of points

    for ballot in data:
        for idx, vote in enumerate(ballot):
            points[vote] += len(names) - 1 - idx # give options n-1,n-2... points based on ranking

    return([x[1] for x in sorted(((value, index) for index, value in enumerate(points)), reverse=True)])

def copeland(data,names):

    score = [0] * len(names) # start with empty list

    for ballot in data: 
        for idx, vote in enumerate(ballot): 
            score[vote] += len(names) - 1 - 2*idx  # increase score by how many they're above vs how many are ranked higher
        for i in names:
            if i not in ballot:
                score[i] -= len(ballot)       # un voted for is tied bottom, subtract number above from score

    return([x[1] for x in sorted(((value, index) for index, value in enumerate(score)), reverse=True)])

def equalshares(projects):

    scores = []
    winners = []
    for idx in range(len(projects)):
        scores.append(projects[idx].cost/len(projects[idx].supporters))
    choice = scores.index(min(scores))
    while scores[choice] < 100000:
        if projects[choice].is_affordable():
            projects[choice].pick_in_equal_shares()
            winners.append(choice)
        scores[choice] = 100000
        choice = scores.index(min(scores))
    
    return winners