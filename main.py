from os import path, sep, listdir
import re
import itertools
import time as t 
import csv

cwd = path.dirname(path.abspath(__file__))

DEBUGGING = False

def load_data(filename="00016-00000001.toi"):
    """
    Load data from file
    """
    data = []
    names = {}
    with open(cwd + sep + filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("# ALTERNATIVE"):
                s = line.split(":")
                number = int(s[0].split(" ")[-1]) - 1
                name = s[1].strip()
                names[number] = name
            
            if line.startswith("#"):
                continue
            s = line.split(":")
            nr_voters = int(s[0])
            votes = []
            if "{" in s[1]:
                # Split {...} from the rest
                new = re.split(r"(\{.*?\})", s[1].strip())
                new[1] = new[1][1:-1]
                votes = [int(v) - 1 for v in new[0].split(",") if v != ""]
                votes += [[int(v) - 1 for v in new[1].split(",") if v != "" if v != "{" if v != "}"]]
                votes += [int(v) - 1 for v in new[2].split(",") if v != ""]

            else:
                votes = [int(v) - 1 for v in s[1].strip().split(",")]    

            for _ in range(nr_voters):
                data.append(votes)
    
    return data, names


def tied_vote(vote, eliminations):
    """
    Resolve a tied vote
    input:
        vote: list of ints (candidates)
        eliminations: list of ints (candidates that have been eliminated)
    output:
        vote: list of ints (candidates)"""

    if vote[0] in eliminations and vote[1] in eliminations:
        return None
    if vote[0] in eliminations:
        return [vote[1]]
    if vote[1] in eliminations:
        return [vote[0]]
    return vote

def plurality(data, names, eliminations):
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
    
    # When debugging, print the number of votes for each candidate
    if DEBUGGING:
        print("\n\nNew Round:")
        for i in range(len(nr_votes)):
            if i not in eliminations:
                print(f"{names[i]}: ", end="")
                for _ in range((21 - len(names[i])) // 8 + 1):
                    print("\t", end="")
                print(f"{nr_votes[i]} votes")

    # Find the winners and losers
    max_votes = max([i for i in nr_votes if i not in eliminations])               # max(nr_votes) belongs to winner
    winners = [i for i in range(len(nr_votes)) if nr_votes[i] == max_votes]       # Find index of winners
    
    # Find the losers
    min_votes = float("inf")                                                      # Set min to infinity
    for idx, ballot in enumerate(nr_votes):
        if ballot < min_votes and idx not in eliminations and idx not in winners: # Lower than min, not eliminated and not a winner
            min_votes = ballot                                                    # Set new min

    # Eliminated if received min votes and not a winner
    losers = [i for i in range(len(nr_votes)) if  nr_votes[i] == min_votes 
                                              and i not in winners]

    return winners, losers

def nummanipulators(data):                                                  # count everyone Derek is least prefered or not not wanted at all
    manipulators = 0
    for ballot in data:
        if (ballot[::-1][0] == 7 and len(ballot) > 1) or (7 not in ballot):
            manipulators += 1
    return manipulators

def bruteforce(data,vote,manipulators):                                     # edit the data by changing the vote of a specified number of voters
    for ballot in data:
        if (ballot[::-1][0] == 7 and len(ballot) > 1) or (7 not in ballot): # just the Derek dislikers
            data[data.index(ballot)] = vote
            manipulators -= 1
        if manipulators == 0:
            break
    return data

def STV(data, names, eliminations):
    """
    Single Transferable Vote
    input:
        data: list of lists of ints (voters' votes)
        names: dict of ints to strings (candidate names)
        eliminations: list of ints (candidates to be eliminated)
    """
    winners, losers = plurality(data, names, eliminations)
    #print(f"Eliminated before: {eliminations}, eliminated now: {losers}")
    eliminations += losers                                      # Add the eliminated candidates to the list of eliminations
    if len(losers) == 0: 
        return winners                                          # No more candidates to eliminate, final round
    return STV(data, names, eliminations)                       # Run STV again without the eliminated candidates


if __name__ == "__main__":
    start = t.time()
    alternatives = [0,1,2,3,4,5,6,8]
    data, names = load_data()
    fields = ['Winner', 'NumManipulators', 'Ballot']
    output = []
    minmanipulators = nummanipulators(data)
    combinations = list(itertools.permutations(alternatives))       # all possible ballots without Derek
    for combination in combinations:                                # loop through possible insincere ballots
        for manipulator in range(minmanipulators,0,-1):             # loop through number of manipulators
            data = bruteforce(data,list(combination),manipulator)
            result = STV(data, names, [9,10])
            if 7 not in result:                                     # Derek deposed
                minmanipulators = manipulator                       # set new best minimum
                data, names = load_data()
                output.append([result[0], minmanipulators, list(combination)])
                continue 
            data, names = load_data()
            break                                                   # for lowest minimum number manipulators, Derek still wins, try next combo
    with open('manipulation.csv', 'w') as f:                        # save results to csv 
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(output)                                                       
    end = t.time()
    print(f"Time taken: {(end-start)}s")        
