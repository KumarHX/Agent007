---
layout: default
title:  Status
---


# Agent007: The A* Scholar Status Report

## Status Report Video

<iframe src="https://www.youtube.com/embed/TTUUmLabrpc" frameborder="0" allowfullscreen=""></iframe>

## Project Summary:

### Environment:
A large flat world map with many random spawned items. 007 has a certain amount of time to grab as many high value items as possible. 

<img src="https://i.ytimg.com/vi/CBZR5a8unpc/hqdefault.jpg">

### Goal:
The current state utilizes the A* star algorithm and applies hueristics of shortest path from agent to items and hueristic of item value to grab close high value items for optimal solution. In further updates, we will employ a learned hueristic to look out for dangers on the map and look for potential path strategies that will lead to better outputs (removing the bias our paths take depending on agent spawn).

### Current Approach:
Our current approach is using the static hueristics to find a suboptimal solution. There is a heavy bias on agent spawn and close local high value items. We wish to implement a learned hueristic process like bootstrapping or imitation to remove bias. Bootstrapping is an iterative procedure that uses learning to create a series of heuristic functions. Initially, this procedure requires a heuristic function h0 and a set of states we call the bootstrap instances. Unlike previous machine learning approaches to creating heuristics, there are no solutions given for any instances, and h0 is not assumed to be strong enough to solve any of the given instances. Imitation is an efficient algorithm that trains heuristic policies by imitating clairvoyant oracles - oracles that have full information about the world and demonstrate decisions that minimize search effort.

### Sources:
- https://www.sciencedirect.com/science/article/pii/S0004370211000877?fbclid=IwAR3o29EXShje6HAfJ-OC908yusSttGQ1AaaLXFmG_2wmK_0_tiwZCSYQCDI
- http://proceedings.mlr.press/v78/bhardwaj17a/bhardwaj17a.pdf
- https://www.cs.cmu.edu/~maxim/files/learningtosearch_socs15.pdf



Source code: https://github.com/KumarHX/PROJECT




Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)

