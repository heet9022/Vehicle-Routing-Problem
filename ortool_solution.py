import evaluateShared as es
import sys

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class Solution:

    def print_solution(self, loads, manager, routing, solution):

        # print(f"Objective: {solution.ObjectiveValue()}")
        total_distance = 0
        for vehicle_id in range(len(loads)):
            index = routing.Start(vehicle_id)
            plan_output = f"Route for vehicle {vehicle_id}:\n"
            route_distance = 0
            while not routing.IsEnd(index):
                plan_output += f" {manager.IndexToNode(index)} -> "
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )
            plan_output += f"{manager.IndexToNode(index)}\n"
            plan_output += f"Distance of the route: {route_distance}\n"
            print(plan_output)
            total_distance += route_distance
        print(f"Total Distance of all routes: {total_distance}")

    def solve(self, filepath):
        vrp = es.loadProblemFromFile(file_path)

        nodes = [[i, i + 1] for i in range(1, len(vrp.loads)*2, 2)]

        loadByID ={}
        for load in vrp.loads:
            loadByID[int(load.id)] = load
        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager((len(vrp.loads)*2) + 1, len(vrp.loads), 0)
        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Define cost of each arc.
        def distance_callback(from_index, to_index):
            """Returns the euclidean distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)

            if from_node == 0:
                from_coord = es.Point(0,0)
            elif from_node % 2 == 0 :
                from_coord = loadByID[from_node // 2].dropoff
            else:
                from_coord = loadByID[(from_node+1) // 2].pickup

            if to_node == 0:
                to_coord = es.Point(0,0)
            elif to_node % 2 == 0 :
                to_coord = loadByID[to_node // 2].dropoff
            else:
                to_coord = loadByID[(to_node+1) // 2].pickup

            return es.distanceBetweenPoints(from_coord, to_coord)
        
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # #Defining Vehicle Addition cost
        for vehicle_id in range(len(vrp.loads)):
            routing.SetFixedCostOfVehicle(500, vehicle_id)
        
        # Add Distance constraint.
        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            720,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name,
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(1)

        # Define Transportation Requests.
        for node in nodes:
            pickup_index = manager.NodeToIndex(node[0])
            delivery_index = manager.NodeToIndex(node[1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
            )
            routing.solver().Add(
                distance_dimension.CumulVar(pickup_index)
                <= distance_dimension.CumulVar(delivery_index)
            )

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
        )

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            self.print_solution(vrp.loads, manager, routing, solution)

if __name__ == "__main__":
    if len(sys.argv) != 2:

        print("Usage: python solution_naive.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    Solution().solve(file_path)