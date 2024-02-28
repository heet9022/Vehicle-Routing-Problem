import evaluateShared as es
import sys

class Driver:

    def __init__(self, distance=0, route=[]):
        self.distanceTravelled = distance
        self.route = route

class Solution:

    def __init__(self):
        self.assigned = {}
        self.drivers = []
        self.loadByID ={}

    def solve(self, file_path):
        
        savings = []
        home = es.Point(0,0)
        vrp = es.loadProblemFromFile(file_path)
        for load in vrp.loads:
            self.loadByID[int(load.id)] = load
        num_loads = len(vrp.loads)

        # calculate savings for each link

        for i in range(num_loads):
            for j in range(num_loads):
                if i != j:            
                    key = str(i+1) + ',' + str(j+1)
                    saving = (key, es.distanceBetweenPoints(vrp.loads[i].dropoff, home) \
                                    + es.distanceBetweenPoints(home, vrp.loads[j].pickup) \
                                    - es.distanceBetweenPoints(vrp.loads[i].dropoff, vrp.loads[j].pickup))
                    savings.append(saving)

        savings = sorted(savings, key = lambda x: x[1], reverse=True)

        # print(savings)
        # print(self.loadByID)
        for saving in savings:

            link  = saving[0]

            # If not all loads are assigned
            if len(self.assigned) != len(vrp.loads):

                link = self.get_node(link)

                # condition a. Either, neither i nor j have already been assigned to a route, 
                # ...in which case a new route is initiated including both i and j.
                if (link[0] not in self.assigned) and (link[1] not in self.assigned):

                    # calculate distance
                    cost = self.computeDistance([self.loadByID[link[0]], self.loadByID[link[1]]], True, True)
                    if cost <= 12*60:
                        d = Driver()
                        d.route = [self.loadByID[link[0]], self.loadByID[link[1]]]
                        self.drivers.append(d)
                        self.assigned[link[0]] = d
                        self.assigned[link[1]] = d


                # condition b. Or, exactly one of the two nodes (i or j) has already been included 
                # ...in an existing route and that point is not interior to that route 
                # ...(a point is interior to a route if it is not adjacent to the depot D in the order of traversal of nodes), 
                # ...in which case the link (i, j) is added to that same route.    
                elif (link[0] in self.assigned) and (link[1] not in self.assigned):

                    d = self.assigned[link[0]]
                    i = d.route.index(self.loadByID[link[0]])
                    # if node is the last node of route
                    if i == len(d.route) - 1:
                        cost = self.computeDistance(d.route + [self.loadByID[link[1]]], True, True)
                        if cost <= 12*60:
                            d.route.append(self.loadByID[link[1]])
                            self.assigned[link[1]] = d
 
                elif (link[0] not in self.assigned) and (link[1] in self.assigned):

                    d = self.assigned[link[1]]
                    i = d.route.index(self.loadByID[link[1]])
                    # if node is the first node of route
                    if i == 0:
                        cost = self.computeDistance([self.loadByID[link[0]]] + d.route, True, True)
                        if cost <= 12*60:
                            d.route = [self.loadByID[link[0]]] + d.route
                            self.assigned[link[0]] = d

                # condition c. Or, both i and j have already been included in two different existing routes 
                # ...and neither point is interior to its route, in which case the two routes are merged.        
                else:

                    d1 = self.assigned[link[0]]
                    i1 = d1.route.index(self.loadByID[link[0]])

                    d2 = self.assigned[link[1]]
                    i2 = d2.route.index(self.loadByID[link[1]])

                    # if node1 is the last node of its route and node 2 is the first node of its route and the routes are different
                    if (i1 == len(d.route) - 1) and (i2 == 0) and (d1 != d2):
                        cost = self.computeDistance(d1.route + d2.route, True, True)
                        if cost <= 12*60:
                            d1.route = d1.route + d2.route
                            for load in d2.route:
                                self.assigned[int(load.id)] = d1
                            # self.assigned[link[1]] = d1
                            
                            self.drivers.remove(d2)
                        
        for i in range(1, len(vrp.loads) + 1):
            if i not in self.assigned:
                d = Driver(0, [])
                d.route.append(self.loadByID[i])
                self.drivers.append(d)
                self.assigned[i] = d
                

    def computeDistance(self, nodes, from_depot, to_depot):

        distance = 0.0
        for i in range(len(nodes)):
            distance += es.distanceBetweenPoints(nodes[i].pickup, nodes[i].dropoff)
            if i != (len(nodes) - 1):
                distance += es.distanceBetweenPoints(nodes[i].dropoff, nodes[i+1].pickup)

        home = es.Point(0,0)
        if nodes:
            if from_depot:
                distance += es.distanceBetweenPoints(home, nodes[0].pickup)
            if to_depot:
                distance += es.distanceBetweenPoints(nodes[-1].dropoff, home)
        
        return distance

    # convert link string to link list to handle saving's key, i.e. str(10, 6) to (10, 6)
    def get_node(self, link):
        nodes = link.split(',')
        return [int(nodes[0]), int(nodes[1])]
    
    def print_solution(self):

        count = 0
        numbers = []
        for d in self.drivers:
            lids =[]
            count += len(d.route)
            for load in d.route:
                lids.append(int(load.id))
                numbers.append(int(load.id))
            print(lids)
        # print(count)
        # print(len(set(numbers)))
        # nat_numbers = [i for i in range(1, 201)]
        # print(set(nat_numbers) - set(numbers))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution_naive.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    # file_path = ".\Training Problems\problem13.txt"
    s = Solution()
    s.solve(file_path)
    s.print_solution()
