import sys
import util

class Solution:

    def __init__(self):
        self.drivers = []
        self.loadByID ={}
        self.depot = util.Point(0,0)
        self.max_distance = 12*60

    def loadProblem(self, file_path):
        loads = util.loadProblemFromFile(file_path)
        for load in loads:
            self.loadByID[int(load.id)] = load

    def computeSavings(self):
        savings = []
        for i in self.loadByID:
            for j in self.loadByID:
                if i != j:            
                    key = (i, j)
                    saving = (key, util.distanceBetweenPoints(self.loadByID[i].dropoff, self.depot) \
                                    + util.distanceBetweenPoints(self.depot, self.loadByID[j].pickup) \
                                    - util.distanceBetweenPoints(self.loadByID[i].dropoff, self.loadByID[j].pickup))
                    savings.append(saving)

        savings = sorted(savings, key = lambda x: x[1], reverse=True)

        return savings
    
    def computeDistance(self, nodes):

        if not nodes:
            return 0.0
        
        distance = 0.0
        for i in range(len(nodes)):
            distance += nodes[i].delivery_distance
            if i != (len(nodes) - 1):
                distance += util.distanceBetweenPoints(nodes[i].dropoff, nodes[i+1].pickup)

        distance += util.distanceBetweenPoints(self.depot, nodes[0].pickup)
        distance += util.distanceBetweenPoints(nodes[-1].dropoff, self.depot)
        
        return distance

    def print_solution(self):

        for driver in self.drivers:
            print([int(load.id) for load in driver.route])

    def solve(self):
        
        # calculate savings for each link
        savings = self.computeSavings()

        for link, _ in savings:

            load1 = self.loadByID[link[0]]
            load2 = self.loadByID[link[1]]

            # condition a. Either, neither i nor j have already been assigned to a route, 
            # ...in which case a new route is initiated including both i and j.
            if not load1.assigned and not load2.assigned:

                # check constraints
                cost = self.computeDistance([load1, load2])
                if cost <= self.max_distance:
                    driver = util.Driver()
                    driver.route = [load1, load2]
                    self.drivers.append(driver)
                    load1.assigned = driver
                    load2.assigned = driver

            # condition b. Or, exactly one of the two nodes (i or j) has already been included 
            # ...in an existing route and that point is not interior to that route 
            # ...(a point is interior to a route if it is not adjacent to the depot D in the order of traversal of nodes), 
            # ...in which case the link (i, j) is added to that same route.    
            elif load1.assigned and not load2.assigned:

                driver = load1.assigned
                i = driver.route.index(load1)
                # if node is the last node of route
                if i == len(driver.route) - 1:
                    # check constraints
                    cost = self.computeDistance(driver.route + [load2])
                    if cost <= self.max_distance:
                        driver.route.append(load2)
                        load2.assigned = driver

            elif not load1.assigned and load2.assigned:

                driver = load2.assigned
                i = driver.route.index(load2)
                # if node is the first node of route
                if i == 0:
                    # check constraints
                    cost = self.computeDistance([load1] + driver.route)
                    if cost <= self.max_distance:
                        driver.route = [load1] + driver.route
                        load1.assigned = driver

            # condition c. Or, both i and j have already been included in two different existing routes 
            # ...and neither point is interior to its route, in which case the two routes are merged.        
            else:

                driver1 = load1.assigned
                i1 = driver1.route.index(load1)

                driver2 = load2.assigned
                i2 = driver2.route.index(load2)

                # if node1 is the last node of its route and node 2 is the first node of its route and the routes are different
                if (i1 == len(driver1.route) - 1) and (i2 == 0) and (driver1 != driver2):
                    cost = self.computeDistance(driver1.route + driver2.route)
                    if cost <= self.max_distance:
                        driver1.route = driver1.route + driver2.route
                        for load in driver2.route:
                            load.assigned = driver1
                        
                        self.drivers.remove(driver2)

        # Assign all unassigned drivers to individual routes      
        for load in self.loadByID.values():
            if not load.assigned:
                driver = util.Driver(0, [])
                driver.route.append(load)
                self.drivers.append(driver)
                load.assigned = driver

                
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution_naive.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    solution = Solution()
    solution.loadProblem(file_path)
    solution.solve()
    solution.print_solution()
