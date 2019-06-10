---
layout: default
title:  Final
---

# Agent007: The A* Scholar Final Report

## Video:

## Project Summary:
Agent 007 spawns on a flat map and has a time limit to pick up as many high value items as possible. The size of the map is 120x120 
with 30 predetermined distinct spawned items. Each item is distinct with a distinct value. The map is not completely observable, all item's position are known to the agent but not item values. The agent has a certain amount of time to pick up any items, but the problem is that items can have negative values associated with them and some items may not be the best individual node to go to but would lead to a higher score due to proximity of other items in the area. Therefore, the agent need to use AI/ML algorithm to solve the problem, so that he can reach out the maximum score. In particular, we use A* Search algorithm.

![](ClusteringVisualized.png?raw=true)<br>

## Approach:
The A* search algorithm **A* = g(n) + h(n)** is used to calculate the value of each item which is equal to the sum of g(n) + h(n), where g(n) is the distance from the agent position to the item's position and h(n) is a heuristic function that estimates the cost of the item. The agent evaluate the reward for each item given the distance to the item from its current position while factoring the item value and finding high value clusters of items by utilizing the heuristic function built from past runs.

##### **Calculate the angle θ**
Since the agent movement is contiunous, we need to calculate the angle at which the agent turns. Given the agent position (x1, y1), and item position (x2, y2), using the inverse tangent function **arctan((x2 - x1) / (y2 - y1))** to find the radian and convert to angle.

##### **Calculate the distance g(n)**
Given the agent position (x1, y1), and item position (x2, y2), we calculate the distance between the agent and each item using formula **distance = sqrt ((x2 - x1)^2 + (y2 - y1)^2)**.

##### **Build the heuristic function f(n)**
We store a certain amount of random runs in dictionary which hold different item pickup sequences with a score attribute to it. The dictionary will be used later for training the agent of which item to pick up next. Initially the agent has 50% chance to randomly pick up an item and 50% chance to pick up the closest item. After multiple runs, the agent will look up the dictionary and find out the sequence which has the highest score, with 65% chance to pick up the item in the sequence or 35% chance to pick up the closest item. The newly generate sequence will be added to the dictionary if it is distinct, and this process will be repeated for the next run.

## Evaluation:
We evaluate our algorithm with the agent that:
- Randomly pick up item
- Pick up the closest item


### Seperate Enviornments:
There are two different environment types we want to test our AI on: Sparce and Cluster.
Sparse maps will have the item set very spread out. 
Cluster maps will have the item set clustered together in bunches. 

#### Sparse Map:
Choosing a random item after every pickup and at initialization: 
![](RandomSparse.png?raw=true)<br>
Avg. Score = -4.75 

Choosing a random item at initialization then employing shortest distance:
![](ShortestPathSparse.png?raw=true)<br>
Avg. Score = -28

Choosing item based on learned hueristic: 


#### Cluster Map:

Choosing a random item after every pickup and at initialization: 
![](RandomCluster.png?raw=true)<br>
Avg. Score = -14.25 

Choosing a random item at initialization then employing shortest distance:
![](ShortestPathCluster.png?raw=true)<br>
Avg. Score = -12.5

Choosing item based on learned hueristic: 

#### Results:


## References:
- [Learning Heuristic Functions For Large State Spaces](https://www.sciencedirect.com/science/article/pii/S0004370211000877?fbclid=IwAR3o29EXShje6HAfJ-OC908yusSttGQ1AaaLXFmG_2wmK_0_tiwZCSYQCDI) 
- [Learning Heuristic Search via Imitation](http://proceedings.mlr.press/v78/bhardwaj17a/bhardwaj17a.pdf)
- [Learning to Search More Efficiently from Experience: A Multi-Heuristic Approach](https://www.cs.cmu.edu/~maxim/files/learningtosearch_socs15.pdf)

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)


