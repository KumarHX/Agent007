---
layout: default
title:  Final
---

# Agent007: The A* Scholar Final Report

## Video:

## Project Summary:
Agent 007 spawns on a flat map and has a time limit to pick up as many high value items as possible. The size of the map is 120x120 
with 30 predetermined distinct spawned items. Each item is distinct with a distinct value. The map is not completely observable, all item's position are known to the agent but not item values. The agent has a certain amount of time to pick up any items, but the problem is that items can have negative values associated with and some items may not be the best individual node to go to but would lead to a higher score due to proximity of other items in the area. Therefore, the agent need to use AI/ML algorithm to solve the problem, so that he can reach out the maximum score.

![](ClusteringVisualized.png?raw=true)<br>

## Approach:
The agent uses A* search algorithm which is A* = g(n) + h(n), where g(n) is the distance from the agent position to the item's position and h(n) is a heuristic function that estimates the cost (reward) of the item. The agent evaluate the reward for each item given the distance to the item from its current position while factoring the item value and finding high value clusters of items by utilizing the heuristic function built from past runs.

#### **Calculate the distance**
Given the agent position (x1, y1), and item position (x2, y2), we calculate the distance between the agent and each item using formula **distance = sqrt ((x2 - x1)^2 + (y2 - y1)^2)**. 

### Building the learned heuristic
The learned hueristic is a set of past runs stored in a dictionary. There is a 50% chance the agent will choose a random item and a 50% chance the agent will choose the closest item when running the trials for the learned hueristic. After many runs, the dictionary will hold many different item pickup sequences with a score attributed to the run. This dictionary will then help guide agent movement (lookup current picked up item with prev runs, choose highest run, make next pickup next in stored sequence).

Key, value dictionary built with each entry representing a training run.
key: list of items picked up.
value: Average item pick up score per path (reward).
Save finished run in dictionary (learn from every run).

### Using the learned hueristic (rewrite)
Let's say we have 5 test runs in our dictionary.
Itemlist: score
A,V,C,D,E : 200
C:R:V:D:A : 150
M,N,O,P,R: -30
Q,A,S,T,P: 300
W,C,U,R: 270

We start with the highest sequence value first element.
Q,A,S,T,P: 300

Current list: Q

Then we either take the next highest value from list (50%) or a random item on map (50%)
Let's say this run randomly selected V.

Current list: Q,V

Then we either take the next highest value from list (50%) or a random item on map (50%)
Lets say the dictionary was selected. 

These two lists have V in them:
A,V,C,D,E : 200
C:R:V:D:A : 150

This list is higher:
A,V,C,D,E : 200

Next value: C.
Current list: Q,V,C
Then we either take the next highest value from list (50%) or a random item on map (50%)
Lets say the dictionary was selected. 

These three lists have C in them:
A,V,C,D,E : 200
C:R:V:D:A : 150
W,C,U,R: 270

This list is highest:
W,C,U,R: 270

Next value: U.
Current list: Q,V,C,U

End of time.
New path Q,V,C,U (score: 170)
added to dictionary.


## Evaluation:
f(n): reward, we didn’t count number of steps because the path is continuous, the depending factor is the item pickup sequence. Also, because the agent is trying to reach out the best score and each item is unique with a unique score, reward/# of items is a fair metric to evaluate performance of a run.

### Seperate Enviornments:
There are two different environment types we want to test our AI on: Sparce and Cluster.

Sparse maps will have the item set very spread out. 

Cluster maps will have the item set clustered together in bunches. 

Different agents will be employed in these different areas. (1): random agent (random movements), (2): agent relying mainly on the constant hueristic and (3): agent relying mainly on the learned hueristic. This will help our evaluation of our AI (detailed in evaluation section).

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


