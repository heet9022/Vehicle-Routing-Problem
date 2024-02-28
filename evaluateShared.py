import subprocess
import os
import sys
import io
import math
import time
import argparse

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def toString(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

def distanceBetweenPoints(p1, p2):
    xDiff = p1.x - p2.x
    yDiff = p1.y - p2.y
    return math.sqrt(xDiff*xDiff + yDiff*yDiff)
    
class Load:
    def __init__(self, id, pickup, dropoff):
        self.id = id
        self.pickup = pickup
        self.dropoff = dropoff
        
class VRP:
    def __init__(self, loads):
        self.loads = loads
    def toProblemString(self):
        s = "loadNumber pickup dropoff\n"
        for idx, load in enumerate(self.loads):
            s += str(idx+1) + " " + load.pickup.toString() + " " + load.dropoff.toString() + "\n"
        return s
        
def loadProblemFromFile(filePath):
    f = open(filePath, "r")
    problemStr = f.read()
    f.close()
    return loadProblemFromProblemStr(problemStr)

def getPointFromPointStr(pointStr):
    pointStr = pointStr.replace("(","").replace(")","")
    splits = pointStr.split(",")
    return Point(float(splits[0]), float(splits[1]))

def loadProblemFromProblemStr(problemStr):
    loads = []
    buf = io.StringIO(problemStr)
    gotHeader = False
    while True:
        line = buf.readline()
        if not gotHeader:
            gotHeader = True
            continue
        if len(line) == 0:
            break
        line = line.replace("\n", "")
        splits = line.split()
        id = splits[0]
        pickup = getPointFromPointStr(splits[1])
        dropoff = getPointFromPointStr(splits[2])
        loads.append(Load(id, pickup, dropoff))
    return VRP(loads)
        
def loadSolutionFromString(solutionStr):
    schedules = []
    buf = io.StringIO(solutionStr)
    while True:
        line = buf.readline()
        if len(line) == 0:
            break
        if ('[' not in line) or (']' not in line):
            return schedules, "Solution format incorrect. Expected all lines to be in format [{load_id}, {load_id}, ...], but got this: " + line
        line = line.replace('[','')
        line = line.replace(']','')
        line = line.replace('\n','')
        line = line.replace(' ','')
        splits = line.split(',')
        schedule = []
        for loadID in splits:
            schedule.append(loadID)
        schedules.append(schedule)
    return schedules, ""
    
def loadCountOrAssignmentError(problem, solutionSchedules):
    solutionLoadIDs = {}
    for schedule in solutionSchedules:
        for loadID in schedule:
            if loadID in solutionLoadIDs:
                return "load " + loadID + " was included in at least two driver schedules"
            solutionLoadIDs[loadID] = True
        
    if len(solutionLoadIDs) != len(problem.loads):
        return "the solution load count is not equal to the problem load count"
        
    for load in problem.loads:
        if load.id not in solutionLoadIDs:
            return "load " + load.id + " was not assigned to a driver"
    
    return ""

def getDistanceOfScheduleWithReturnHome(schedule, loadByID):
    distance = 0.0
    home = Point(0,0)
    currentLoc = home
    for loadID in schedule:
        load = loadByID[loadID]
        #to pickup
        distance += distanceBetweenPoints(currentLoc, load.pickup)
        currentLoc = load.pickup
        #to dropoff
        distance += distanceBetweenPoints(currentLoc, load.dropoff)
        currentLoc = load.dropoff
    distance += distanceBetweenPoints(currentLoc, home)
    return distance
        
def getSolutionCostWithError(problem, solutionSchedules):
    err = loadCountOrAssignmentError(problem, solutionSchedules)
    if err != "":
        return 0, err
    
    return getSolutionCost(problem, solutionSchedules)

def getSolutionCost(problem, solutionSchedules):
    loadByID ={}
    for load in problem.loads:
        loadByID[load.id] = load

    totalDrivenMinutes = 0.0
    for idx, schedule in enumerate(solutionSchedules):
        scheduleMinutes = getDistanceOfScheduleWithReturnHome(schedule, loadByID)
        if scheduleMinutes > 12*60:
            return 0, print("schedule idx " + str(idx) + " is invalid: driver runs for " + str(scheduleMinutes) + " minutes")
        totalDrivenMinutes += scheduleMinutes
    
    return 500*len(solutionSchedules) + totalDrivenMinutes, ""
    
def printSolutionFormatNag():
    print("Program should only print a solution (no debugging messages) in format that looks like this:")
    print("[1,4,9,7]")
    print("[5,2,3,8]")
    print("[10,6]")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--problemDir", help="Path to folder containing problems")
    parser.add_argument("--cmd", help="Command to run your program (not including a problem file)")
    args=parser.parse_args()

    files = [f for f in os.listdir(args.problemDir)]
    costs = []
    sumRunTime = 0.0
    
    for inputFile in files:
        if inputFile[0] == ".":
            continue
        print(inputFile)
        print("\trunning...")
        inputPath = args.problemDir + "/" + inputFile
        #run commands on input path
        cmd = args.cmd.split()
        cmd.append(inputPath)
        startTime = time.time()
        output = subprocess.check_output(cmd).decode("utf-8")
        runTime = time.time() - startTime
        print("\trun time:", runTime, "s")
        if runTime > 30:
            print("\t\tRun time constraint of 30s exceeded! Please reduce program runtime!")
        sumRunTime += runTime

        print("\tevaluating solution...")
        problem = loadProblemFromFile(inputPath)
        schedules, err = loadSolutionFromString(output)
        if err != "":
            print(err)
            printSolutionFormatNag()
            print("Observed:")
            print(output)
            exit()
        
        cost, err = getSolutionCostWithError(problem, schedules)
        if err != "":
            print(err)
            exit()
        costs.append(cost)
        print("\tcost: " + str(cost))

    meanCost = 0.0
    for cost in costs:
        meanCost += cost
    meanCost /= len(costs)
    print("mean cost: " + str(meanCost))
    print("mean run time: " + str(sumRunTime * 1000 / len(costs)) + "ms")
