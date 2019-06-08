---
layout: default
title:  Final
---

# Agent007: The A* Scholar Final Report

## Status Report Video

## Project Summary:

### Environment:
A large flat world map with many predetermined placed spawned items. Agent has a certain amount of time to grab as many high value items as possible. Each item is distinct with a distinct value. The map is completely observable, all item positions and item values are known to Agent. The agent is in constant motion and changes in thr agent's degree direction lead to changes in movement direction.

### Thesis of Solution:
The agent uses a constant hueristic for reward of each item given distance to item from current position + item value and a learned hueristic built from past runs to find clusters of items. The learned hueristic AI solves the problem of going for best singular item but missing item cluster locations that would lead to better overall scores. 

### Seperate Enviornments:
There are three different environment types: Sparce, Dense and Middle. Sparse will not have many items (30), dense will have many items (100) and middle will have an average amount (60). Different agents will be employed in these different areas. (1): random agent (random movements), (2): agent relying mainly on the constant hueristic and (3): agent relying mainly on the learned hueristic. This will help our evaluation of our AI (detailed in evaluation section).

## Approach:

### Building the constant hueristic
The constant hueristic utilizes the constant variables of item location and item value with respect to location to guide movement.

g(n) : giving the agent position x1, y1, giving each item’s position x2, y2, calculate the distance between the agent and each item using formula D = sqrt ((x2 - x1)^2 + (y2 - y1)^2) 

Find the best items that the agent need to pick up based on the calculation reward/ distance of the item. This basically gives the reward per step. Find the maximum (reward/step) and let the agent turns to the angle where the item located. 

### Building the learned hueristic
Key, value dictionary built with each entry representing a training run.
key; list of items picked up
value: Average item pick up score per path (reward/# of items).
Each trail run chooses a random item to go for and then applies randomness and the constant hueristic for further item pickups. If the score is greater than a minimum threshold score, the item is picked up. After the dicionary is build (agent is trained) every item pick up for future runs will reference next item to pick up given current picked up item depending on which list holds current item and the highest score future item is selected. 

### The Different Agents
Strategy 1: map exploration (high randomness)
Random item selection 25%
Reliance on constant hueristic: 90%
Reliance on learned hueristic: 10%

Strategy 2: value grab
Random item selection 5%
Reliance on constant hueristic: 10%
Reliance on learned hueristic: 90%

Strategy 3: balance
Random item selection 12.5%
Reliance on constant hueristic: 50%
Reliance on learned hueristic: 50%

## Evaluation:
f(n): reward / # of items, we didn’t count number of steps because the path is continuous, the depending factor is the item pickup sequence. Also, because the agent is trying to reach out the best score and each item is unique with a unique score, reward/# of items is a fair metric to evaluate performance of a run.

#### Sparse Map:
Shortest path with giving reward / step score (average score) = 180
We only have five runs for this algorithm since the score will always be the same. 5 runs just to prove that the agent is always picking up the optimal items.

Random 20 runs:
The agent scored 65.0
The agent scored -25.0
The agent scored -10.0
The agent scored -5.0
The agent scored -85.0
The agent scored 15.0
The agent scored 10.0
The agent scored 50.0
The agent scored -35.0
The agent scored -30.0
The agent scored 50.0
The agent scored 10.0
The agent scored 0.0
The agent scored 0.0
The agent scored 45.0
The agent scored -50.0
The agent scored -65.0
The agent scored -15.0
The agent scored 15.0
The agent scored -35.0
Total Score: -95 
Average: -4.75

![](randomVSConstant.png?raw=true)



## Sources
- [Learning Heuristic Functions For Large State Spaces](https://www.sciencedirect.com/science/article/pii/S0004370211000877?fbclid=IwAR3o29EXShje6HAfJ-OC908yusSttGQ1AaaLXFmG_2wmK_0_tiwZCSYQCDI) 
- [Learning Heuristic Search via Imitation](http://proceedings.mlr.press/v78/bhardwaj17a/bhardwaj17a.pdf)
- [Learning to Search More Efficiently from Experience: A Multi-Heuristic Approach](https://www.cs.cmu.edu/~maxim/files/learningtosearch_socs15.pdf)

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)







