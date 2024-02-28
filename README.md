# VRP Solver

This program is a solution to the Vehicle Routing Problem for Pickup and Delivery (VRPPD) with constraint on distance travelled by each driver. It efficiently assigns loads to drivers while minimizing total distance travelled.

Each load has a pickup location and a dropoff location, each specified by a Cartesian point. A driver completes a load by driving to the pickup location, picking up the load, driving to the dropoff, and dropping off the load. The time required to drive from one point to another, in minutes, is the Euclidean distance between them. That is, to drive from $(x_1, y_1)$ to $(x_2, y_2)$ takes $\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$ minutes.

As an example, suppose a driver located at $(0,0)$ starts a load that picks up at $(50,50)$ and delivers at $(100,100)$. This would take $2 \times \sqrt{2 \times 50^2} \approx 141.42$ minutes of drive time to complete: $\sqrt{(50-0)^2 + (50-0)^2}$ minutes to drive to the pickup, and $\sqrt{(100-50)^2 + (100-50)^2}$ minutes to the dropoff.

Each driver starts and ends his shift at a depot located at $(0,0)$. A driver may complete multiple loads on his shift, but may not exceed $12$ hours of total drive time. That is, the total Euclidean distance of completing all his loads, including the return to $(0,0)$, must be less than $12 \times 60$.


A VRP solution contains a list of drivers, each of which has an ordered list of loads to be completed. All loads must be assigned to a driver.

The total cost of a solution is given by the formula:
$$total Cost = 500*number Of Drivers + total Number Of Driven Minutes$$

## Installation

```
git clone https://github.com/heet9022/Vehicle-Routing-Problem.git
cd Vehicle-Routing-Problem
```
## Usage

```
python3 solution.py <input_file_path>
```

## Evaluation

```
python3 evaluateShared.py --cmd "python3 solution.py" --problemDir "Training Problems"
```

## Input File Format

The problem input contains a list of loads. Each load is formatted as an id followed by pickup and dropoff locations in (x,y) floating point coordinates. An example input with four loads is

```
loadNumber pickup dropoff
1 (-50.1,80.0) (90.1,12.2)
2 (-24.5,-19.2) (98.5,1,8)
3 (0.3,8.9) (40.9,55.0)
4 (5.3,-61.1) (77.8,-5.4)
```
## Output File Format
The program writes a solution to stdout. The solution lists, on separate lines, each driver’s ordered list of loads as a schedule. An example solution to the above problem could be:

```
[1]
[4,2]
[3]
```
This solution means one driver does load 1, another driver does load 4 followed by load 2, and a final driver does load 3.

## References

[Clarke and Wright Savings algorithm](https://web.mit.edu/urban_or_book/www/book/chapter6/6.4.12.html)