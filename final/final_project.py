import random
from enum import Enum
from finalSCFs import *

random.seed(1)

class BallotType(Enum):
    APPROVAL = 1
    FULL_RANKING = 2
    PARTIAL_RANKING = 3

# Class representing a neighborhood
class Neighborhood:
    def __init__(self, nr_inhabitants, preferences, cohesion, budget) -> None:
        self.preferences = preferences
        self.cohesion = cohesion
        self.inhabitants = [Person(self) for i in range(nr_inhabitants)]
        self.nr_inhabitants = nr_inhabitants


# Class representing a person with a political preference based on 4 attributes
class Person:
    INSTANCES = []
    NR_INSTANCES = 0
    def __init__(self, neighborhood, budget) -> None:
        self.neighborhood = neighborhood
        self.attributes = {i: random.gauss(neighborhood.preferences[i], neighborhood.cohesion) for i in range(4)}
        self.required_approval = 0
        self.project_approvals = {}
        self.approves = []
        self.rankings = []
        self.budget = budget
        Person.INSTANCES.append(self)
        Person.NR_INSTANCES += 1

    def project_approval(self, projects):
        for project in projects:
            approval = sum([self.attributes[i] * project.attributes[i] for i in range(4)])
            if self.neighborhood not in project.neighborhoods:
                approval *= 0.5
            
            if approval > self.required_approval:
                project.add_supporter(self)
                self.approves.append(project.instance)
            
            self.project_approvals[project] = approval
        if len(self.project_approvals) == 0:
            self.required_approval -= 0.1
            self.project_approval(projects)
            return

        # Sort the projects by approval
        self.rankings = sorted(self.project_approvals.items(), key=lambda x: x[1], reverse=True)
        self.rankings = [x.instance for x, _ in self.rankings]
    
    def get_ballot(self, ballot_type: BallotType):
        if ballot_type == BallotType.APPROVAL:
            return self.approves
        elif ballot_type == BallotType.FULL_RANKING:
            return self.rankings
        elif ballot_type == BallotType.PARTIAL_RANKING:
            return [x for x in self.rankings if x in self.approves]

 
# Class representing a project
class Project:
    NR_INSTANCES = 0
    def __init__(self, attributes, neighborhoods, cost) -> None:
        self.instance = Project.NR_INSTANCES
        Project.NR_INSTANCES += 1
        self.attributes = attributes
        self.neighborhoods = neighborhoods
        self.cost = cost
        self.supporters = []

    def add_supporter(self, person):
        self.supporters.append(person)

    def __str__(self) -> str:
        return self.instance

def main():
    budget = 25000
    # Create 5 neighborhoods
    neighborhoods = []
    neighborhoods.append(Neighborhood(200, [0.4, 0.2, -0.1, -0.1], 0.3))
    neighborhoods.append(Neighborhood(800, [0.2, -0.3, -0.2, 0.2], 0.5))
    neighborhoods.append(Neighborhood(400, [-0.6, 0.4, 0.3, -0.4], 0.2))
    neighborhoods.append(Neighborhood(400, [-0.2, 0.4, 0.2, -0.3], 0.3))
    neighborhoods.append(Neighborhood(700, [0.1, -0.1, -0.3, 0.2], 0.4))
    nr_neighborhoods = len(neighborhoods)
    for person in Person.INSTANCES:
        person.budget = budget / Person.NR_INSTANCES

    print("Neighborhoods created")

    # Create projects
    nr_projects = 100
    projects = []
    size_probabilities = [0.4, 0.15, 0.05, 0.05, 0.3]
    possible_costs = [200, 500, 1000, 1500, 2000, 5000, 8000, 10000, None]
    for i in range(nr_projects):
        # Pick a random number of neighborhoods to support the project
        project_size = random.random()
        for n, j in enumerate(size_probabilities):
            project_size -= j
            if project_size < 0:
                project_size = n+1
                break
        in_neighborhoods = []
        for _ in range(project_size):
            # Pick a random neighborhood to support the project
            neighborhood = random.choice(neighborhoods)
            if neighborhood not in in_neighborhoods:
                in_neighborhoods.append(neighborhood)

        # Create the project
        current_possible_costs = possible_costs[project_size-1: -6 + project_size]
        project = Project([random.uniform(-1, 1) for _ in range(4)], neighborhoods, random.choice(current_possible_costs))
        print(f"Project {i} of cost {project.cost} is spread over {project_size} neighborhoods")
        projects.append(project)
    print("Projects created")

    # Have each person project their approval for each project
    for person in Person.INSTANCES:
        person.project_approval(projects)

    for project in projects:
        print(f"Project {project.instance} has {len(project.supporters)} supporters")

    partial_approval_profile = [x.get_ballot(BallotType.PARTIAL_RANKING) for x in Person.INSTANCES]
    print(partial_approval_profile[1])
    print(len(partial_approval_profile))
    print(STV(partial_approval_profile,[0,1,2,3,4,5,6,7,8,9]))

    

if __name__=="__main__":
    main()