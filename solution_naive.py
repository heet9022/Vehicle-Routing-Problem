import evaluateShared as es
import sys

class Driver:
    def __init__(self, location = es.Point(0,0), distanceTravelled = 0.0, loads = []):
        self.currentLoc = location
        self.distanceTravelled = distanceTravelled
        self.loads = loads

class Solution:

    def solve(self, file_path):
        home = es.Point(0,0)
        vrp = es.loadProblemFromFile(file_path)
        loadByID ={}
        for load in vrp.loads:
            loadByID[load.id] = load
        drivers = [Driver()]
            
        for load in vrp.loads:

            currentDriver = drivers[-1]
            
            additional_distance = es.distanceBetweenPoints(currentDriver.currentLoc, load.pickup) \
                                + es.distanceBetweenPoints(load.pickup, load.dropoff) \
                                + es.distanceBetweenPoints(load.dropoff, home)
            
            if currentDriver.distanceTravelled + additional_distance <= 12*60:
                currentDriver.currentLoc = load.dropoff
                currentDriver.distanceTravelled += additional_distance
                currentDriver.loads.append(load)
            else:
                distanceTravelled = es.distanceBetweenPoints(home, load.pickup) \
                                + es.distanceBetweenPoints(load.pickup, load.dropoff)
                drivers.append(Driver(load.dropoff, distanceTravelled, [load]))
        
        for driver in drivers:
            lids =[]
            for load in driver.loads:
                lids.append(int(load.id.rstrip('\r')))
            print(lids)
   


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solution_naive.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    Solution().solve(file_path)