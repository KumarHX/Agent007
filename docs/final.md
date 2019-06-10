---
layout: default
title:  Final
---

# Agent007: The A* Scholar Final Report

## Video:

## Project Summary:

### Problem Statement:
Agent 007 spawns on a flat map and has a time limit to pick up as many high value items as possible. Agent knows item locations but not item values (could be negative).

### Environment:
The enviornment consists of a 120x120 flat world map with 30 predetermined distinct spawned items. The agent has a certain amount of time to grab as many high value items as possible. Each item is distinct with a distinct value. The map is not completely observable, all item positions are known to the agent but not item values. The agent is in constant motion and changes in the agent's positional degree direction lead to changes in movement direction.

### Problems to Solve:
value: item value is unknown to the agent
clustering: this agent does not account for clusters of items that may not be the best individual node to go to but would lead to a higher overall score due to proximity of other items in the area.
![](ClusteringVisualized.png?raw=true)<br>



### Seperate Enviornments:
There are two different environment types we want to test our AI on: Sparce and Cluster.

Sparse maps will have the item set very spread out. 

Cluster maps will have the item set clustered together in bunches. 

Different agents will be employed in these different areas. (1): random agent (random movements), (2): agent relying mainly on the constant hueristic and (3): agent relying mainly on the learned hueristic. This will help our evaluation of our AI (detailed in evaluation section).

### Item Stats
ITEM SET = 'bowl': -5, 'red_mushroom': 5, 'brown_mushroom': 5, 'pumpkin': -5, 'egg': -25, 'sugar': -10, 'carrot': -10, 'cooked_rabbit': 10, 'baked_potato': 5, 'bread': 10, 'melon': 5, 'cookie': 5, 'mushroom_stew': 20, 'pumpkin_pie': 20, 'rabbit_stew': 50, 'melon_seeds': -50, 'pumpkin_seeds': -50, 'wheat': -30, 'apple': 5, 'diamond': 50, 'bone': -25, 'beetroot_soup': 20, 'golden_apple': 15, 'golden_carrot': -5, 'bow': -5,'coal': -20, 'glass_bottle': -25, 'golden_sword': -15, 'golden_axe': -15, 'golden_hoe': -15

The range of individual scores (-50,50)
Agent Starting Position [0.5, 0.5]
45 seconds (time limit) = 900 ticks
0.22 movement in 1 tick. 
900 times 0.22 = 198 location change

Sparse Map:
![](SparseMap.png?raw=true)
Item Locations (corresponds with item set)
GOAL_POSITIONS = [[-36, -36], [-29, -23], [36, -28], [-25, 41], [-5, -35], [-7, 16], [-18, -10], [1, -23], [43, 37],
                  [26, 37],
                  [32, 8], [-41, -40], [41, -5], [-35, 33], [-22, -3], [0, -7], [-17, -43], [-22, -11], [-13, -18],
                  [-42, 28],
                  [1, 41], [6, 15], [-5, 40], [3, -29], [37, -22], [-16, -30], [-30, 32], [16, 17], [-17, 39], [20, 23]]


Highest Potential Score (Sparse):
rabbit_stew, 11 location change, 50 points
beetroot_soup, 13 location change, 20 points
diamond, 22.3 location change, 50 points
pumpkin_pie, 3.5 location change, 30 points 
golden_apple, 12.8 location change, 15 points
bread, 14.2 location change, 10 points
baked_potato, 7.2 location change, 5 points
melon, 14.3 location change, 5 points
beetroot_soup, 18.94 location change, 20 points
mushroom_stew, 16.83 location change, 20 points
cooked_rabbit, 7.62 location change,  10 points 
apple,  8.92 location change, 5 points
red_mushroom, 12.53 location change 5 points
MAX SCORE: 245 points

Cluster Map:
![](ClusterMap.png?raw=true)<br>
Our AI should solve the issue of going for valuable individual items rather than higher value clusters. 
## Approach:

### Thesis of Solution:
The agent uses a constant hueristic to evaluate the reward for each item given the distance to the item from the current position while factoring the item value and finding high value clusters of items by utilizing a learned hueristic built from past runs. The learned hueristic AI solves the problem of item value and clustering.

### Building the constant hueristic
The constant hueristic utilizes the constant variable of item location with respect to the agent's current location to guide the agent's movement.

g(n) : giving the agent position x1, y1, giving each item’s position x2, y2, calculate the distance between the agent and each item using formula D = sqrt ((x2 - x1)^2 + (y2 - y1)^2) 

### Building the learned hueristic
The learned hueristic is a set of past runs stored in a dictionary. There is a 50% chance the agent will choose a random item and a 50% chance the agent will choose the closest item when running the trials for the learned hueristic. After many runs, the dictionary will hold many different item pickup sequences with a score attributed to the run. This dictionary will then help guide agent movement (lookup current picked up item with prev runs, choose highest run, make next pickup next in stored sequence).

Key, value dictionary built with each entry representing a training run.
key: list of items picked up.
value: Average item pick up score per path (reward).
Save finished run in dictionary (learn from every run).

### Using the learned hueristic
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


## Sources
- [Learning Heuristic Functions For Large State Spaces](https://www.sciencedirect.com/science/article/pii/S0004370211000877?fbclid=IwAR3o29EXShje6HAfJ-OC908yusSttGQ1AaaLXFmG_2wmK_0_tiwZCSYQCDI) 
- [Learning Heuristic Search via Imitation](http://proceedings.mlr.press/v78/bhardwaj17a/bhardwaj17a.pdf)
- [Learning to Search More Efficiently from Experience: A Multi-Heuristic Approach](https://www.cs.cmu.edu/~maxim/files/learningtosearch_socs15.pdf)

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)







