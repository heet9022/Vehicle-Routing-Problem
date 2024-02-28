import sys
import util

class Solution:

    def __init__(self):
        self.assigned = {}
        self.drivers = []
        self.loadByID ={}
        self.depot = util.Point(0,0)
        self.max_distance = 12*60

    def load(self, file_path):
        loads = util.loadProblemFromFile(file_path)
        for load in loads:
            self.loadByID[int(load.id)] = load

    def solve(self):
        
        # calculate savings for each link
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
        
        for link, saving in savings:

            load1 = self.loadByID[link[0]]
            load2 = self.loadByID[link[1]]

            # condition a. Either, neither i nor j have already been assigned to a route, 
            # ...in which case a new route is initiated including both i and j.
            if (link[0] not in self.assigned) and (link[1] not in self.assigned):

                # calculate distance
                cost = self.computeDistance([load1, load2], True, True)
                if cost <= self.max_distance:
                    d = util.Driver()
                    d.route = [load1, load2]
                    self.drivers.append(d)
                    self.assigned[link[0]] = d
                    self.assigned[link[1]] = d

            # condition b. Or, exactly one of the two nodes (i or j) has already been included 
            # ...in an existing route and that point is not interior to that route 
            # ...(a point is interior to a route if it is not adjacent to the depot D in the order of traversal of nodes), 
            # ...in which case the link (i, j) is added to that same route.    
            elif (link[0] in self.assigned) and (link[1] not in self.assigned):

                d = self.assigned[link[0]]
                i = d.route.index(load1)
                # if node is the last node of route
                if i == len(d.route) - 1:
                    cost = self.computeDistance(d.route + [load2], True, True)
                    if cost <= self.max_distance:
                        d.route.append(load2)
                        self.assigned[link[1]] = d

            elif (link[0] not in self.assigned) and (link[1] in self.assigned):

                d = self.assigned[link[1]]
                i = d.route.index(load2)
                # if node is the first node of route
                if i == 0:
                    cost = self.computeDistance([load1] + d.route, True, True)
                    if cost <= self.max_distance:
                        d.route = [load1] + d.route
                        self.assigned[link[0]] = d

            # condition c. Or, both i and j have already been included in two different existing routes 
            # ...and neither point is interior to its route, in which case the two routes are merged.        
            else:

                d1 = self.assigned[link[0]]
                i1 = d1.route.index(load1)

                d2 = self.assigned[link[1]]
                i2 = d2.route.index(load2)

                # if node1 is the last node of its route and node 2 is the first node of its route and the routes are different
                if (i1 == len(d.route) - 1) and (i2 == 0) and (d1 != d2):
                    cost = self.computeDistance(d1.route + d2.route, True, True)
                    if cost <= self.max_distance:
                        d1.route = d1.route + d2.route
                        for load in d2.route:
                            self.assigned[int(load.id)] = d1
                        
                        self.drivers.remove(d2)

        # Assign all unassigned drivers to individual routes      
        for i in range(1, len(self.loadByID) + 1):
            if i not in self.assigned:
                d = util.Driver(0, [])
                d.route.append(self.loadByID[i])
                self.drivers.append(d)
                self.assigned[i] = d

    def computeDistance(self, nodes, from_depot, to_depot):

        distance = 0.0
        for i in range(len(nodes)):
            distance += nodes[i].delivery_distance
            if i != (len(nodes) - 1):
                distance += util.distanceBetweenPoints(nodes[i].dropoff, nodes[i+1].pickup)

        if nodes:
            if from_depot:
                distance += util.distanceBetweenPoints(self.depot, nodes[0].pickup)
            if to_depot:
                distance += util.distanceBetweenPoints(nodes[-1].dropoff, self.depot)
        
        return distance

    def print_solution(self):

        for d in self.drivers:
            lids =[]
            for load in d.route:
                lids.append(int(load.id))
            print(lids)

                


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution_naive.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    # file_path = ".\Training Problems\problem13.txt"
    s = Solution()
    s.load(file_path)
    s.solve()
    s.print_solution()
