import random

random.seed(1)

# Class representing a neighborhood
class Neighborhood:
    def __init__(self, nr_inhabitants, preferences, cohesion) -> None:
        self.preferences = preferences
        self.cohesion = cohesion
        self.inhabitants = [Person(self) for i in range(nr_inhabitants)]
        self.nr_inhabitants = nr_inhabitants


# Class representing a person with a political preference based on 4 attributes
class Person:
    def __init__(self, neighborhood) -> None:
        self.neighborhood = neighborhood
        self.attributes = {i: random.gauss(neighborhood.preferences[i], neighborhood.cohesion) for i in range(4)}
        self.required_approval = random.uniform(0, 0.5)
        self.project_approvals = {}
        self.rankings = []

    def project_approval(self, projects):
        for project in projects:
            approval = sum([self.attributes[i] * project.attributes[i] for i in range(4)])
            if self.neighborhood in project.neighborhoods:
                approval *= 0.5
            
            if approval > self.required_approval:
                project.add_supporter(self)
            
            self.project_approvals[project] = approval
        if len(self.project_approvals) == 0:
            self.required_approval -= 0.1

        # Sort the projects by approval
        self.rankings = sorted(self.project_approvals.items(), key=lambda x: x[1], reverse=True)
        self.rankings = [x.instance for x, _ in self.rankings]
        print(self.rankings)
    
    def get_ballot


# Class representing a project
class Project:
    NR_INSTANCES = 0
    def __init__(self, attributes, neighborhoods, cost) -> None:
        Project.NR_INSTANCES += 1
        self.instance = Project.NR_INSTANCES
        self.attributes = attributes
        self.neighborhoods = neighborhoods
        self.cost = cost
        self.supporters = []

    def add_supporter(self, person):
        self.supporters.append(person)

    def __str__(self) -> str:
        return self.instance

def main():
    # Create 5 neighborhoods
    neighborhoods = []
    neighborhoods.append(Neighborhood(200, [0.4, 0.2, -0.1, -0.1], 0.3))
    neighborhoods.append(Neighborhood(600, [0.2, -0.3, -0.2, 0.2], 0.6))
    neighborhoods.append(Neighborhood(300, [0.6, -0.4, -0.3, 0.4], 0.2))
    neighborhoods.append(Neighborhood(300, [-0.2, 0.4, 0.2, -0.3], 0.3))
    neighborhoods.append(Neighborhood(500, [-0.1, 0.2, 0.3, -0.2], 0.4))
    nr_neighborhoods = len(neighborhoods)
    print("Neighborhoods created")

    # Create projects
    nr_projects = 10
    projects = []
    size_probabilities = [0.3, 0.2, 0.1, 0.1, 0.3]
    possible_costs = [50, 100, 200, 500, 1000, 2000, 5000, 10000]
    for i in range(nr_projects):
        # Pick a random number of neighborhoods to support the project
        project_size = random.random()
        print(project_size)
        for n, j in enumerate(size_probabilities):
            project_size -= j
            if project_size < 0:
                project_size = n+1
                break
        print(f"Project {i} has {project_size} neighborhoods")
        in_neighborhoods = []
        for _ in range(project_size):
            # Pick a random neighborhood to support the project
            neighborhood = random.choice(neighborhoods)
            if neighborhood not in in_neighborhoods:
                in_neighborhoods.append(neighborhood)

        # Create the project
        project = Project([random.uniform(-1, 1) for _ in range(4)], neighborhoods, random.choice(possible_costs))
        projects.append(project)
    print("Projects created")

    # Have each person project their approval for each project
    for neighborhood in neighborhoods:
        for person in neighborhood.inhabitants:
            person.project_approval(projects)
    
    for project in projects:
        print(f"Cost: {project.cost}, supporters: {len(project.supporters)}")


if __name__=="__main__":
    main()