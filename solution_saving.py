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
            self.loadByID[load.id] = load
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

        for saving in savings:

            link  = saving[0]

            # If not all loads are assigned
            if len(self.assigned) != len(vrp.loads):

                link = self.get_node(link)

                # condition a. Either, neither i nor j have already been assigned to a route, 
                # ...in which case a new route is initiated including both i and j.
                if (link[0] not in self.assigned) and (link[1] not in self.assigned):

                    # calculate distance
                    cost = self.computeDistance([self.loadByID(link[0]), self.loadByID(link[1])], True, True)
                    if cost <= 12*60:
                        d = Driver()
                        d.route = [self.loadByID(link[0]), self.loadByID(link[1])]
                        self.drivers.append(d)
                        self.assigned[link[0]] = d
                        self.assigned[link[1]] = d
  
                        print('\t','Link ', link, ' fulfills criteria a), so it is created as a new route')
                    else:
                        print('\t','Though Link ', link, ' fulfills criteria a), it exceeds maximum load, so skip this link.')


    def computeDistance(self, nodes, from_depot, to_depot):

        distance = 0.0
        for i in range(len(nodes)):
            distance += es.distanceBetweenPoints(nodes[i].pickup, nodes[i].delivery)
            if i != (len(nodes) - 1):
                distance += es.distanceBetweenPoints(nodes[i].delivery, nodes[i+1].pickup)

        home = es.Point(0,0)
        if nodes:
            if from_depot:
                distance += es.distanceBetweenPoints(home, nodes[0].pickup)
            if to_depot:
                distance += es.distanceBetweenPoints(nodes[-1].delivery, home)
        
        return distance

    # convert link string to link list to handle saving's key, i.e. str(10, 6) to (10, 6)
    def get_node(self, link):
        nodes = link.split(',')
        return [int(nodes[0]), int(nodes[1])]
    
    # determine if a node is interior to a route
    def interior(self, node, route):
        try:
            i = route.index(node)
            # adjacent to depot, not interior
            if i == 0 or i == (len(route) - 1):
                label = False
            else:
                label = True
        except:
            label = False
        
        return label
    
    # merge two routes with a connection link
    def merge(route0, route1, link):
        # if route0.index(link[0]) != (len(route0) - 1):
        #     route0.reverse()
        
        # if route1.index(link[1]) != 0:
        #     route1.reverse()
            
        return route0 + route1
    
    # determine 4 things:
    # 1. if the link in any route in routes -> determined by if count_in > 0
    # 2. if yes, which node is in the route -> returned to node_sel
    # 3. if yes, which route is the node belongs to -> returned to route id: i_route
    # 4. are both of the nodes in the same route? -> overlap = 1, yes; otherwise, no
    def which_route(self, link, routes):
        # assume nodes are not in any route
        node_sel = list()
        i_route = [-1, -1]
        count_in = 0
        

        for node in link:
            if node in self.assigned:
                node_sel.append(node)

        for route in routes:
            for node in link:
                try:
                    route.index(node)
                    i_route[count_in] = routes.index(route)
                    node_sel.append(node)
                    count_in += 1
                except:
                    pass
                    
        if i_route[0] == i_route[1]:
            overlap = 1
        else:
            overlap = 0
            
        return node_sel, count_in, i_route, overlap

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution_naive.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    Solution().solve(file_path)