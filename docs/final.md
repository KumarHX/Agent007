---
layout: default
title:  Final
---

# Agent007: The A* Scholar Final Report

## Video:

## Project Summary:
Agent 007 is spawned on a fixed point on a flat 60x60 grid. This map generates item spawns with the locations known to the agent. The agent wants to pick up all the items on the grid with the most optimal path. The paths are judged based on distance travelled. 
The agent wants to find the most optimal path (least distance travelled) in the shortest amount of time possible. 
<Picture of example grid>

## Approaches:
Breadth First Search:
Breadth first search will always find the most optimal solution, but it will do it rather slowly. Suppose there are 4 items on the map:
STARTPOINT, A,B,C,D
Each of these items will get expanded out with every single other item and generate every possible path. In the case of 4 items, this will lead to 4! + 4 (28) different combinations of item pickups.The distance (score) of each run is stored and the lowest score is returned as the optimal solution.

<a href="url"><img src="BFStree.png" align="center" height="300" width="600" ></a>

As the item number on the map increases, this algorithm scales very poorly. At ten items, the algorithm takes 10! + 10 runs (3,628,810) to find the optimal path.


<a href="url"><img src="gridOne.png" align="center" height="300" width="600" ></a>

Greedy Best First Algorithm

Each grid on this map represents a possible item sequence path. The agent will keep expanding until every single grid is explored. (teal grid in this case means the path was explored). If we say the yellow grid is the optimal path, it will not stop once that path has been found, since it has no way of knowing that is optimal till checking every unexplored path. However, if we can reduce the number of exploration paths we need to generate, we can substantially speed up the algorithm. With n items, this algorithm takes n! + n or O(n!) time to run. 

<a href="url"><img src="gridTwo.png" align="center" height="300" width="600" ></a>

The greedy best first Algorithm runs much faster than the Breadth First Search algorithm. It finds the closest item given most recent item pickup or spawn point (constantly recalculating at runtime) until a path sequence is found. The greedy best first search is NOT guaranteed to find the optimal solution. 

Random Cavet: 
Since the greedy algorithm will always choose the same path, we implemented an element of choosing a random item at times to see if some different path will eventually lead to the optimal outcome. 

Greedy Q-Learning Implementation
The agent evaluates the reward for each item given the distance to the item from its current position while factoring the randomness element and continues to find the lowest distance sequence building from knowledge gained from previous runs. 

A* Algorithm 
The A* algorithm uses an admissible heuristic to optimistically find the optimal solution. As long as the cost the heuristic estimates to reach the goal is not higher than the lowest possible cost from the current point in the path, it is admissible.

<a href="url"><img src="gridThree.png" align="center" height="300" width="600" ></a> 

Each grid on this map represents a possible item sequence path. The agent will expand different paths based on the heuristic until the all the items are picked up in one of the paths  (teal grid in this case means the path was explored). If we say the yellow grid is the optimal path, it will be the first path to finish getting all items and that sequence shall return. With n items, this algorithm takes O(b^d) time to run. 
b is the branching factor (the average number of successors per state)
d is depth of solution

Heuristic #1 distance:
f(n) = c(n) + h(n)
c(n) = sum of distance from all items in the current path.
h(n) = minimum distance item from current item.

Heuristic #2 item cluster:
Each item is scored by 1/distance to all other items. Agent position is considered an item.
f(n) = c(n) + h(n)
c(n) = sum of item cluster from all items in the current path.
h(n) = minimum cluster item from current item.


## Evaluation:
Map size = 
Breadth First Search Finds optimal path in: 
Does Greedy Algorithm Find optimal path?
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
Greedy Q-Learning Implementation analysis
A* Search Heuristic 1 Finds optimal path in: 
A* Search Heuristic 2 Finds optimal path in: 

Map size = 
Breadth First Search Finds optimal path in: 
Does Greedy Algorithm Find optimal path?
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
Greedy Q-Learning Implementation analysis
A* Search Heuristic 1 Finds optimal path in: 
A* Search Heuristic 2 Finds optimal path in: 

Map size =
Breadth First Search Finds optimal path in: 
Does Greedy Algorithm Find optimal path?
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
Greedy Q-Learning Implementation analysis
A* Search Heuristic 1 Finds optimal path in: 
A* Search Heuristic 2 Finds optimal path in: 

Map size = 
Breadth First Search Finds optimal path in: 
Does Greedy Algorithm Find optimal path?
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
Greedy Q-Learning Implementation analysis
A* Search Heuristic 1 Finds optimal path in: 
A* Search Heuristic 2 Finds optimal path in: 

Graph 
Y-axis is time taken to find optimal path
X-axis is number of items on map 
4 linear plots for each strategy 
 
Analysis

## References:


Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)

Source Code:


