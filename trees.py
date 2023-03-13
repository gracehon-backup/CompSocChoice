from os import path, sep, listdir
import re
import itertools
import time as t 
import enum

cwd = path.dirname(path.abspath(__file__))

DEBUGGING = False
class Constraint:
    def __init__(self, add, subtract, difference) -> None:
        self.add = add
        self.subtract = subtract
        self.difference = difference
    
    def check_constraint(self):
        return sum(self.add) - sum(self.subtract) + self.difference <= 0

    
    def string(self) -> str:
        add = [chr(ord('a') + a) for a in self.add]
        subtract = [chr(ord('a') + a) for a in self.subtract]
        return f"{add} - {subtract} <= {-self.difference}"


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

def vote_count(data, names, eliminations):
    """
    Count the plurality score of each candidate
    input:
        data: list of lists of ints (voters' votes)
        names: dict of ints to strings (candidate names)
        eliminations: list of ints (candidates that have been eliminated)
    output:
        nr_votes: list of ints (number of votes for each candidate)
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

    return nr_votes

def plurality_loser(nr_votes, eliminations):
    sorted_votes, sorted_candidates = zip(*sorted(zip(nr_votes, names.keys()), reverse=False))
    low_vote = sorted_votes[-1]
    losers = []
    for vote, candidate in zip(sorted_votes, sorted_candidates):
        if candidate in eliminations:
            continue
        if vote < low_vote:
            losers = [candidate]
            low_vote = vote
        elif vote == low_vote:
            losers.append(candidate)
    
    return losers

def STV(data, names, eliminations=[]):
    """
    Single Transferable Vote
    input:
        data: list of lists of ints (voters' votes)
        names: dict of ints to strings (candidate names)
        eliminations: list of ints (candidates to be eliminated)
    """
    nr_votes = vote_count(data, names, eliminations)
    losers = plurality_loser(nr_votes, eliminations)

    if len(losers) + len(eliminations) == len(names): 
        return [c for c in range(len(names)) if c not in eliminations] # No more candidates to eliminate, final round
    eliminations += losers                                      # Add the eliminated candidates to the list of eliminations
    return STV(data, names, eliminations)                       # Run STV again without the eliminated candidates


SCENARIOS = 0

def STV_tree(data, names, eliminations=[], ballot=[], old_constraints=[], old_winners=[]):
    print(f"Eliminations: {eliminations}, New ballot: {ballot}")
    nr_votes = vote_count(data, names, eliminations)
    losers = plurality_loser(nr_votes, eliminations)
    global SCENARIOS

    if len(losers) + len(eliminations) == len(names):
        SCENARIOS += 1
        return ([c for c in range(len(names)) if c not in eliminations][0], old_constraints, eliminations, ballot) # No more candidates to eliminate, final round

    possible_alternatives = names.keys()
    for candidate in ballot:
        if candidate not in eliminations:
            possible_alternatives = [candidate]

    results = []
    for new_alternative in possible_alternatives:
        contradiction = False
        new_ballot = ballot.copy()
        if len(possible_alternatives) > 1:
            new_ballot += [new_alternative]
        if new_alternative in old_winners or new_alternative in eliminations:
            continue

        for elim in names.keys():
            if elim in eliminations:
                continue
            constraints = []
            for other_candidate in names.keys():
                if other_candidate in eliminations or other_candidate in old_winners:
                    continue

                difference = nr_votes[elim] - nr_votes[other_candidate]
                add = [other_candidate]
                subtract = [elim]
                if elim in old_winners:
                    subtract = []
                if new_alternative == elim:
                    subtract = []
                    add += [i for i in names.keys() if i not in old_winners and i not in eliminations and i != new_alternative]
                    if difference <= 0:
                        contradiction = True
                        break
                if new_alternative == other_candidate:
                    add = []
                    subtract += [i for i in names.keys() if i not in old_winners and i != new_alternative and i != elim]
                    if difference >= 0:
                        continue
                
                if add == subtract:
                    if difference > 0:
                        contradiction = True
                        break
                    continue

                constraints.append(Constraint(add, subtract, difference))
            
            if contradiction:
                continue

            new_eliminations = eliminations + [elim]
            result = STV_tree(data, names, new_eliminations, new_ballot, old_constraints + constraints, old_winners)
            results.append(result)
    
    return results


def eliminate(data, eliminations):
    """
    Eliminate candidates from the data
    input:
        data: list of lists of ints (voters' votes)
        eliminations: list of ints (candidates to be eliminated)
    output:
        new_data: list of lists of ints (voters' votes)
    """
    new_data = []
    for ballot in data:
        new_ballot = []
        for candidate in ballot:
            if type(candidate) == list:
                new = [c for c in candidate if c not in eliminations]
                if len (new) == 0:
                    continue
                new_ballot.append(new if len(new) > 1 else new[0])
            elif candidate not in eliminations:
                new_ballot.append(candidate)

        new_data.append(new_ballot)
    return new_data


def print_constraints(results, exclude=None):
    for result in results:
        if type(result) == list:
            print_constraints(result)
        elif result[0] != 3:
            continue
        else:
            print(result[0])
            for constraint in result[1]:
                print(constraint.string())
            print(f"Elimination order: {[chr(x + ord('a')) for x in result[2]]}")
            print(f"Ballot: {[chr(x + ord('a')) for x in result[3]]}")
            print()

if __name__ == "__main__":
    start = t.time()
    org_data, names = load_data("manipulatable.toi")
    alternatives = [i for i in range(len(names))]
    original_winner = STV(org_data, names)
    print(f"Original winner: {original_winner}")

    results = STV_tree(org_data, names, eliminations=[], ballot=[], old_winners=original_winner)
    print_constraints(results, exclude=original_winner)
    print(SCENARIOS)
