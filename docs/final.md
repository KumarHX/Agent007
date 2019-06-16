---
layout: default
title:  Final
---

# Agent007: The A* Scholar Final Report

## Video:

## Project Summary:
Agent 007 is spawned on a fixed point on a flat 100x100 grid. This map generates item spawns with the locations known to the agent. The agent wants to pick up all the items on the grid with the most optimal path. The paths are judged based on distance travelled and the execution time. The goal of our project is to use different search strategies to solve this rendition of the traveling salesman problem. In other words, the agent wants to find the most optimal path, or the least distance travelled in the shortest amount of time possible. 

# NEED TO GET 4 DIFFERENT MAP ITEMS/PLEACEMENT IMAGE!!!!

<br>

## Approaches:
- **Breadth First Search Algorithm:**<br>
Breadth first search will always find the most optimal solution, but it will do it rather slowly. Suppose there are 4 items on the map, each of these items will get expanded out with every single other item and generate every possible path. This will lead to 4x3x2x1 = 24 different combinations of item pickups.
<br>
<a href="url"><img src="BFStree.png" align="center" height="300" width="600" ></a>
<br>
**Calculate Distance** <br>
Given agent position (x1, y1) and item position (x2, y2), we calculate the distance between the agent and the item using distance formula **D = sqrt((x2-x1)^2 + (y2-y1)^2)**. Then we store the total distance travelled of each combinations of item pickups and return the path which has the lowest distance score as the optimal solution.
<br>
<a href="url"><img src="gridOne.png" align="center" height="290" width="480" ></a>
<br>
Each grid on this map represents a possible item sequence path. The agent will keep expanding until every single grid is explored. A teal grid in this case indicates the path was explored. The agent will not stop once that the optimal path has been found, since it has no way of knowing that is optimal until every unexplored path is checked. However, if we can reduce the number of full paths explorations we need to generate and still guarantee finding the optimal path, we can substantially speed up our search. 

- **Greedy Search Algorithm**<br>
The Greedy Search algorithm runs much faster than the BFS algorithm. It only finds the closest item given the current agent position until a path sequence is found. Although it costs less time to finish the execution, the algorithm does not guaranteed to find the optimal path since it doesn't calculate the distance of all of the item pickup combinations.

<a href="url"><img src="gridTwo.png" align="center" height="300" width="600" ></a>
<br>

- **A* Algorithm** <br>
The A* algorithm uses an admissible heuristic to optimistically find the optimal solution. As long as the cost the heuristic estimates to reach the goal is not higher than the lowest possible cost from the current point in the path, it is admissible. In our case, the heuristics we choose cannot overpower the distance metric. 
<br>
<a href="url"><img src="gridThree.png" align="center" height="300" width="600" ></a> 
<br>
Each grid on this map represents a possible item sequence path. The agent will expand different paths based on the heuristic until all the items are picked up in one of the paths. If the yellow grid is the optimal path, it will be the first path to finish getting all items and that sequence shall return. If the hueristic is admissible, it will be the optimal path.  


<br>
Heuristic #1 distance:
<br>
f(n) = c(n) + h(n)
<br>
c(n) = sum of distance from all items in the current path.
<br>
h(n) = minimum distance item from current item.

<br>
Distance is an admissible hueristic since distance cannot overpower distance. 
<br>

<br>
Items close to many other items indicate a potential for less distance needed to travel if those items are expanded - we built the A* cluster heuristic around that ideal. The cluster heuristic acts as the sum of all distances to other items from each item/# of items times 0.05. Since we don’t want to have the agent picking up high cluster items across the map, we make it play a small role and still heavily rely on distance. NOTE: cannot prove admissibility, but provides optimal path in all 4 map variants.
<br>

<br>
<a href="url"><img src="ClusteringVisualized.png" align="center" height="300" width="600" ></a>
<br>

<br>
Heuristic #2 item cluster:
<br>
Each item is scored by 1/distance to all other items. Agent position is considered an item.
<br>
The cluster heuristic acts as sum of all distances to other items from item/# of items times 0.05 (lower importance)
<br>
f(n) = c(n) + h(n)
<br>
c(n) = cluster heuristic + distance 
<br>
h(n) = cluster value from current item + minimum distance from current item.
<br>
<br>

## Evaluation:
Map size = 
<br>
Breadth First Search Finds optimal path in: 
<br>
Does Greedy Algorithm Find optimal path?
<br>
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
<br>
Greedy Q-Learning Implementation analysis
<br>
A* Search Heuristic 1 Finds optimal path in: 
<br>
A* Search Heuristic 2 Finds optimal path in: 
<br>

Map size = 
<br>
Breadth First Search Finds optimal path in: 
<br>
Does Greedy Algorithm Find optimal path?
<br>
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
<br>
Greedy Q-Learning Implementation analysis
<br>
A* Search Heuristic 1 Finds optimal path in: 
<br>
A* Search Heuristic 2 Finds optimal path in: 
<br>


Map size = 
<br>
Breadth First Search Finds optimal path in: 
<br>
Does Greedy Algorithm Find optimal path?
<br>
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
<br>
Greedy Q-Learning Implementation analysis
<br>
A* Search Heuristic 1 Finds optimal path in: 
<br>
A* Search Heuristic 2 Finds optimal path in: 
<br>

Map size = 
<br>
Breadth First Search Finds optimal path in: 
<br>
Does Greedy Algorithm Find optimal path?
<br>
Does Greedy Algorithm Randomized Find optimal path in BFS time or less?
<br>
Greedy Q-Learning Implementation analysis
<br>
A* Search Heuristic 1 Finds optimal path in: 
<br>
A* Search Heuristic 2 Finds optimal path in: 
<br>
# NEED TO GET RUN VALUES TABLE!!

Graph 
Y-axis is time taken to find optimal path
X-axis is number of items on map 
4 linear plots for each strategy 

# CAN MAKE GRAPH AFTER RUN VALUES TABLE!!

<br>
Analysis:
As assumed, BFS scaled very poorly in execution time. Greedy Best First Algorithm had a higher likelyhood of finding the optimal solution in lower item maps. The Greedy Q-Learning Implementation did well in lower item maps and okay in higher item maps but did not manage to beat BFS in execution time for the middle item maps (indicating Greedy Q-Learning could have gotten lucky with the sequence in the higher item maps or the factorial increase of execution time makes high item BFS solutions so slow a greedy AI implementation is a better search strategy). A* hueristic #1 did the best out of all the search strategies except in the highest item map, where A* hueristic #2 found the optimal solution in less time than utilzing hueristic #1 indicating the clustering hueristic inclusion is very helpful in high density item maps (especially considering an extra cluster calculation has to be made for every item on the map with this hueristic). 

<br>
## References:
https://arxiv.org/pdf/1210.4913.pdf
http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
https://artint.info/2e/html/ArtInt2e.Ch3.S6.SS2.html
http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)

Source Code:


