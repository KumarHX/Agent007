---
layout: default
title:  Status
---


# Agent007: The A* Scholar Status Report

## Status Report Video

<iframe src="https://www.youtube.com/embed/TTUUmLabrpc" frameborder="0" allowfullscreen=""></iframe>

## Project Summary:

### Environment:
A large flat world map with many random spawned items. 007 has a certain amount of time to grab as many high value items as possible. We are still debating on including mobs or pitfall spots or "point suck" holes on the map.  

<img src="https://i.ytimg.com/vi/CBZR5a8unpc/hqdefault.jpg">

### Current Status:
The current state utilizes the A* star algorithm and applies hueristics of shortest path from agent to items and hueristic of item value to grab close high value items for optimal solution. In further updates, we will employ a learned hueristic to look out for dangers on the map and look for potential path strategies that will lead to better outputs (removing the bias our paths take depending on agent spawn). There is a 10% chance a random move will be made. This is not optimal now since there is no learned search hueristic implemented yet, but this will be good in the future when our hueristic will learn from past runs (one static run won't teach much).

### Current Preformance:

### Learning Hueristic:
Learning from experience can significantly improve the performance of search based agents; effectively we would encode experiences from past runs to guide search.  

<img src="https://data-flair.training/blogs/wp-content/uploads/sites/2/2018/08/Heuristic-Search-in-Artificial-Intelligence-Python-01-1.jpg">

### Clear advantage of employing learned hueristic on current problem:
Our current approach is using the static hueristics to find a suboptimal solution. There is a heavy bias on agent spawn and close local high value items. We wish to implement a learned hueristic process like bootstrapping or imitation or an experience graphto remove bias. Bootstrapping is an iterative procedure that uses learning to create a series of heuristic functions. Initially, this procedure requires a heuristic function h0 and a set of states we call the bootstrap instances. There are no solutions given for any instances, and h0 is not assumed to be strong enough to solve any of the given instances. Imitation is an efficient algorithm that trains heuristic policies by imitating clairvoyant oracles - oracles that have full information about the world and demonstrate decisions that minimize search effort. Experience graphs also work well for our problem, assisting search with experience from previous runs.

### Potential Challenges We Can Add 
- crafting
- "point drain spots"
- enemy MOBs

### What can the AI algorithm do?
- crafting: dont know value of crafted item till after: Learn to go down some high craft item paths.
- "point drain spots": Don't know these spots before reaching them. Learn to avoid them.
- enemy MOBs: Paths that avoid mobs upon contact could do better.

### Implementation Strategy
Previous good paths will be saved in a database, a similarity check between current path and prev paths will be implemented, highest close scoring best path will be chosen, repeat till end of timer. If current path good, add to DB.

Pseudocode:<br>
1: procedure pastProcessingRuns:<br>
2:		PLDB <- buildDatabase(S,k) S is set of solved instances, k is samples per plan<br>
3:		PARTITIONDATABASE(PLDB,n) <- n is number of additional hueristics<br>
4: procedure inGameProcessing:<br>
5:		input: Problem isntance P(i) consistent hueristic h0 (distance + reward)<br>
6:		FINDHUERISTICCANDIDATES(P(i), n)<br>
7:		PLANWITHMHA*<br>
8:		IF PLAN GOOD:<br>
9:			UPDATEDB<br>
<br>
### How do we do with static hueristics and A* on potential challenges?
Not well

<iframe src="https://www.youtube.com//embed/tmKcxlXll-s" frameborder="0" allowfullscreen=""></iframe>

### Sources:
- [Learning Heuristic Functions For Large State Spaces](https://www.sciencedirect.com/science/article/pii/S0004370211000877?fbclid=IwAR3o29EXShje6HAfJ-OC908yusSttGQ1AaaLXFmG_2wmK_0_tiwZCSYQCDI) 
- [Learning Heuristic Search via Imitation](http://proceedings.mlr.press/v78/bhardwaj17a/bhardwaj17a.pdf)
- [Learning to Search More Efficiently from Experience: A Multi-Heuristic Approach](https://www.cs.cmu.edu/~maxim/files/learningtosearch_socs15.pdf)

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)

