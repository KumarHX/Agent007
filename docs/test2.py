from __future__ import print_function
from __future__ import division
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Demo of mob_spawner block - creates an arena, lines it with mob spawners of a given type, and then tries to keep an agent alive.
# Just a bit of fun - no real AI in here!

from future import standard_library
standard_library.install_aliases()
from builtins import range
from past.utils import old_div
from queue import PriorityQueue
import os
import random
import sys
import time
import json
import time
import errno
import math
import itertools
from collections import defaultdict, deque
if sys.version_info[0] == 2:
    # Workaround for https://github.com/PythonCharmers/python-future/issues/262
    import Tkinter as tk
else:
    import tkinter as tk
from collections import namedtuple

try:
    import MalmoPython
    import malmoutils
except ImportError:
    import malmo.MalmoPython as MalmoPython
    import malmo.malmoutils as malmoutils

# Task parameters:
NUM_GOALS = 7
ARENA_WIDTH = 100
ARENA_BREADTH = 100
MOB_TYPE = "Endermite"

# Display parameters:
CANVAS_BORDER = 20
CANVAS_WIDTH = 400
CANVAS_HEIGHT = CANVAS_BORDER + ((CANVAS_WIDTH - CANVAS_BORDER) * ARENA_BREADTH / ARENA_WIDTH)
CANVAS_SCALEX = old_div((CANVAS_WIDTH-CANVAS_BORDER),ARENA_WIDTH)
CANVAS_SCALEY = old_div((CANVAS_HEIGHT-CANVAS_BORDER),ARENA_BREADTH)
CANVAS_ORGX = old_div(-ARENA_WIDTH,CANVAS_SCALEX)
CANVAS_ORGY = old_div(-ARENA_BREADTH,CANVAS_SCALEY)

# Map 1 7
GOAL_TYPES = ['iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow']
GOAL_POSITIONS = [[10, 2],[-3, 14],[30, 5],[-28, -13],[2, 8],[9, -4],[21, 30]]
Items_Info = {"iron_shovel" : [10, 2], "iron_pickaxe" : [-3, 14], "iron_axe": [30, 5], "flint_and_steel":[-28, -13], "apple":[2, 8],
              "bow": [9, -4], "arrow":[21, 30]}

# MAP 2 8
#GOAL_TYPES =  ['iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow','coal']
#GOAL_POSITIONS = [[-30 ,  23 ], [11 ,  -27 ], [27 ,  -12 ], [-12 ,  7 ], [-4 ,  -28 ], [21, -23], [-13 ,  -27 ], [6 ,  23 ]]
#Items_Info = {"iron_shovel" : [-30, 23], "iron_pickaxe" : [11, -27], "iron_axe": [27, -12], "flint_and_steel":[-12 , 7], "apple":[-4 ,  -28],
#              "bow": [21, -23], "arrow":[-13, -27], "coal": [6,23]}

# MAP 3 9
#GOAL_TYPES =  ['iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow','coal','diamond']
#GOAL_POSITIONS = [[-14 ,  -9 ],[23 ,  18 ], [10 ,  29 ], [-12 ,  7 ], [-4 ,  -28 ],[-30, 23], [-13 ,  -27 ], [6 ,  23 ],[-28 ,  -30 ]]
#Items_Info = {"iron_shovel" : [-14, -9], "iron_pickaxe" : [23, 18], "iron_axe": [10, 29], "flint_and_steel":[-12 , 7], "apple":[-4 ,  -28],
#              "bow": [30, -23], "arrow":[-13, -27], "coal": [6,23], "diamond": [-28, -30]}

# MAP 4 10
#GOAL_TYPES =  ['iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow','coal','diamond','iron_ingot']
#GOAL_POSITIONS = [[21 ,  -23 ], [-28 ,  -30 ], [23 ,  -19 ], [-17 ,  19 ], [14 ,  -3 ], [-13, -27],[6 ,  23 ],[-14 ,  -9 ],[10 ,  29 ],[-12 ,  7 ]]
#Items_Info = {"iron_shovel" : [21, -23], "iron_pickaxe" : [-28, -30], "iron_axe": [23, -19], "flint_and_steel":[-17 , 19], "apple":[14,  -3],
#              "bow": [-13, -27], "arrow":[6, 23], "coal": [-14, -9], "diamond": [10, 29], "iron_ingot": [-12, 7]}

# MAP 5 11
#GOAL_TYPES =  ['iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow','coal','diamond','iron_ingot', 'gold_ingot']
#GOAL_POSITIONS = [[17 ,  3 ], [6 ,  20 ], [-30 ,  23 ], [-4 ,  -28 ], [23 ,  18 ],[1, -11], [-13, -27],[6 ,  23 ],[-14 ,  -9 ],[10 ,  29 ],[-12 ,  7 ]]
#Items_Info = {"iron_shovel" : [17, 3], "iron_pickaxe" : [6, 20], "iron_axe": [-30, 23], "flint_and_steel":[-4, -28], "apple":[23,  18],
#              "bow": [1, -11], "arrow":[-13, -27], "coal": [6, 23], "diamond": [-14, -9], "iron_ingot": [10, 29], "gold_ingot": [-12, 7]}

def getItemXML():
    ''' Build an XML string that contains some randomly positioned goal items'''
    xml=""
    for item in range(NUM_GOALS):
        X = str(GOAL_POSITIONS[item][0])
        Z = str(GOAL_POSITIONS[item][1])
        xml += '''<DrawItem x="''' + X + '''" y="210" z="''' + Z + '''" type="''' + GOAL_TYPES[item] + '''"/>'''
    return xml

def getCorner(index: object, top: object, left: object, expand: object = 0, y: object = 206) -> object:
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+old_div(ARENA_WIDTH,2))) if left else str(expand+old_div(ARENA_WIDTH,2))
    z = str(-(expand+old_div(ARENA_BREADTH,2))) if top else str(expand+old_div(ARENA_BREADTH,2))
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'

def getMissionXML(summary):
    ''' Build an XML mission string.'''
    spawn_end_tag = ' type="mob_spawner" variant="' + MOB_TYPE + '"/>'
    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + summary + '''</Summary>
        </About>

        <ModSettings>
            <MsPerTick>15</MsPerTick>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <AllowSpawning>false</AllowSpawning>
                <Weather>clear</Weather>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
                <DrawingDecorator>
                    <DrawCuboid ''' + getCorner("1",True,True,expand=1) + " " + getCorner("2",False,False,y=226,expand=1) + ''' type="grass"/>
                    <DrawCuboid ''' + getCorner("1",True,True,y=210) + " " + getCorner("2",False,False,y=226) + ''' type="air"/>

                    <DrawLine ''' + getCorner("1",True,True) + " " + getCorner("2",True,False) + spawn_end_tag + '''
                    <DrawLine ''' + getCorner("1",True,True) + " " + getCorner("2",False,True) + spawn_end_tag + '''
                    <DrawLine ''' + getCorner("1",False,False) + " " + getCorner("2",True,False) + spawn_end_tag + '''
                    <DrawLine ''' + getCorner("1",False,False) + " " + getCorner("2",False,True) + spawn_end_tag + '''
                    <DrawCuboid x1="-5" y1="206" z1="-5" x2="5" y2="206" z2="5" ''' + spawn_end_tag + '''
                    ''' + getItemXML() + '''
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>The Hunted</Name>
            <AgentStart>
                <Placement x="0.5" y="210.0" z="0.5"/>
                <Inventory>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ChatCommands/>
                <ContinuousMovementCommands turnSpeedDegs="920"/>
                <AbsoluteMovementCommands/>
                <MissionQuitCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="100" zrange="'''+str(ARENA_BREADTH)+'''" />
                </ObservationFromNearbyEntities>
                <ObservationFromFullInventory flat="false"/>
                <ObservationFromFullStats/>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

recordingsDirectory="FleeRecordings"
try:
    os.makedirs(recordingsDirectory)
except OSError as exception:
    if exception.errno != errno.EEXIST: # ignore error if already existed
        raise

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

root = tk.Tk()
root.wm_title("AI TRACE")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, borderwidth=0, highlightthickness=0, bg="black")
canvas.pack()
root.update()

def canvasX(x):
    return (old_div(CANVAS_BORDER,2)) + (0.5 + old_div(x,float(ARENA_WIDTH))) * (CANVAS_WIDTH-CANVAS_BORDER)

def canvasY(y):
    return (old_div(CANVAS_BORDER,2)) + (0.5 + old_div(y,float(ARENA_BREADTH))) * (CANVAS_HEIGHT-CANVAS_BORDER)

def drawMobs(entities, flash):
    canvas.delete("all")
    canvas.create_rectangle(canvasX(old_div(-ARENA_WIDTH,2)), canvasY(old_div(-ARENA_BREADTH,2)), canvasX(old_div(ARENA_WIDTH,2)), canvasY(old_div(ARENA_BREADTH,2)), fill="#888888")
    for ent in entities:
        if ent["name"] == MOB_TYPE:
            canvas.create_oval(canvasX(ent["x"])-2, canvasY(ent["z"])-2, canvasX(ent["x"])+2, canvasY(ent["z"])+2, fill="#ff2244")
        elif ent["name"] in GOAL_TYPES:
            canvas.create_oval(canvasX(ent["x"])-3, canvasY(ent["z"])-3, canvasX(ent["x"])+3, canvasY(ent["z"])+3, fill="#4422ff")
        else:
            canvas.create_oval(canvasX(ent["x"])-4, canvasY(ent["z"])-4, canvasX(ent["x"])+4, canvasY(ent["z"])+4, fill="#22ff44")
    root.update()

def findAI(entities):
    for ent in entities:
        if ent["name"] == MOB_TYPE:
            continue
        elif ent["name"] in GOAL_TYPES:
            continue
        else:
            return ent

def permutation(lst): 
  
    # If lst is empty then there are no permutations 
    if len(lst) == 0: 
        return [] 
  
    # If there is only one element in lst then, only 
    # one permuatation is possible 
    if len(lst) == 1: 
        return [lst] 
  
    # Find the permutations for lst if there are 
    # more than 1 characters 
  
    l = [] # empty list that will store current permutation 
  
    # Iterate the input(lst) and calculate the permutation 
    for i in range(len(lst)): 
       m = lst[i] 
  
       # Extract lst[i] or m from the list.  remLst is 
       # remaining list 
       remLst = lst[:i] + lst[i+1:] 
  
       # Generating all permutations where m is first 
       # element 
       for p in permutation(remLst): 
           l.append([m] + p) 
    return l

def calculateBFS(values):
    PathDistance = {}
    ''' calculate the BFS distance ''' 

    for combinations in values:
        totalDistance = 0;
        first_item = combinations[0]
        firstitem_position = Items_Info.get(first_item)
        firstitem_distance = math.sqrt((0.5- firstitem_position[0])** 2 + (0.5 - firstitem_position[1])**2)
        totalDistance += firstitem_distance
        prevItem_position = firstitem_position
        i = 1
        while(i < len(combinations)):
            item = combinations[i]
            item_position = Items_Info.get(item)
            item_distance = math.sqrt((prevItem_position[0]- item_position[0])** 2 + (prevItem_position[1] - item_position[1])**2)
            totalDistance += item_distance
            prevItem_position = item_position
            i = i + 1
        PathDistance[totalDistance] = combinations
   
    all_path = sorted(PathDistance.items())

    optimal_path = all_path[0]

    return optimal_path

def beginpath(values):
    pathBegin = {}
    for items in values:
        item_position = Items_Info.get(items)
        item_distance = math.sqrt((0.5- item_position[0])** 2 + (0.5 - item_position[1])**2)
        pathBegin[item_distance] = items

    return pathBegin

def heuristic(a, b):
    if type(a) != tuple:
        a = Items_Info.get(a)
    if type(b) != tuple:
        b = Items_Info.get(b)

    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1) **2)

def a_star(start):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        
        for next in GOAL_TYPES:
            new_cost = cost_so_far[current] + heuristic(current, next)

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

def CalculateDistance(entities):
    items_value = []

    z_value = 0.0
    x_value = 0.0
    
    for items in entities:
        if (items['name'] == 'The Hunted'):
            x_value = items['x']
            z_value = items['z']

    for items in entities:
        if (items['name'] != 'The Hunted'):
            hypotenuse = math.sqrt((x_value - items['x'])** 2 + (z_value - items['z'])**2)
            items_value.append(hypotenuse)

    return items_value

def getItem(entities, item_value):
    goal_item = {}

    z_value = 0.0
    x_value = 0.0

    for ent in entities:
        if (ent['name'] == 'The Hunted'):
            x_value = ent['x']
            z_value = ent['z']

        if (ent['name'] != 'The Hunted'):
            if (math.sqrt((x_value - ent['x'])** 2 + (z_value - ent['z'])**2)) == min(item_value):
                goal_item = ent
                return goal_item

    return goal_item

def getRandomItem(entities, item_value):
    goal_item = {}

    z_value = 0.0
    x_value = 0.0

    for ent in entities:
        if (ent['name'] == 'The Hunted'):
            x_value = ent['x']
            z_value = ent['z']

        if (ent['name'] != 'The Hunted'):
            random_index = random.randint(0, len(item_value) - 1)
           # if ((float(GOAL_TYPES_WITH_REWARDS[ent['name']]) / math.sqrt((x_value - ent['x'])** 2 + (z_value - ent['z'])**2)) == item_value[random_index]):
            if (math.sqrt((x_value - ent['x'])** 2 + (z_value - ent['z'])**2)) == item_value[random_index]:
                 goal_item = ent
                 return goal_item

    return goal_item

def getItemFromPath(entities, index, optimal_path):
    goal_item = {}
    item_to_get = ""

    item_to_get = optimal_path[index]

    for items in inventory:
        if item_to_get == items['type']:
            index += 1
    item_to_get = optimal_path[index]

    for ent in entities:
        if ent['name'] == item_to_get:
            goal_item = ent
            return goal_item

    return goal_item

def findAngle(entities, value_item):
    us = findAI(entities)

    if len(value_item) == 0:
        return 0
 
    angle = 0

    current_angle = us['yaw']

    xx = value_item['x'] - us['x']
    yy = value_item['z'] - us['z']  
    
    if xx <= 0:
        if yy < 0:
           angle = (math.pi) - math.atan(math.fabs(xx) / math.fabs(yy)) 
        else:
            # when both on the x-axis
            if yy == 0:
                angle = math.pi/2
            else:
                angle = math.atan(math.fabs(xx) / math.fabs(yy))

    else:
        if yy <= 0:
           angle = -math.atan(math.fabs(yy) / math.fabs(xx)) - (math.pi / 2)

        else:
           angle = -math.atan(math.fabs(xx) / math.fabs(yy))
    
    # convert radian to angle
    angle = ((angle / math.pi * 180) - current_angle)%360

    if angle < 180:
        angle /= 360
    elif angle > 180:
        angle = (angle - 360)/360

    return angle


if __name__ == '__main__':

    # Create a pool of Minecraft Mod clients.
    # By default, mods will choose consecutive mission control ports, starting at 10000,
    # so running four mods locally should produce the following pool by default (assuming nothing else
    # is using these ports):
    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10001))

    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print('ERROR:', e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        print(agent_host.getUsage())
        exit(0)

    start_time = time.time()

    # BFS path
    BFS = permutation(GOAL_TYPES)
    path_distance = calculateBFS(BFS)
    total_distance = path_distance[0]
    optimal_path = path_distance[1]

    current_yaw = 0

    path = set()
    distance = 0.0

    for iRepeat in range(1):
        random_item = {}
        index = 0

        my_mission = MalmoPython.MissionSpec(getMissionXML("Agent007 #" + str(iRepeat)), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        max_retries = 3

        for retry in range(max_retries):
            try:
            # Attempt to start the mission:
                agent_host.startMission( my_mission, my_client_pool, my_mission_record, 0, "predatorExperiment" )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission",e)
                    print("Is the game running?")
                    exit(1)
                else:
                    time.sleep(2)

        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()

        agent_host.sendCommand("move 1")

        # main loop
        while world_state.is_mission_running:
            world_state = agent_host.getWorldState()
            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                ob = json.loads(msg)

                if "Yaw" in ob:
                    current_yaw = ob['Yaw']
                if "inventory" in ob:
                    inventory = ob['inventory']

                if "entities" in ob:
                    entities = ob['entities']
                    drawMobs(entities, False)

                if len(random_item) == 0:
                    random_item = getItemFromPath(entities, index, optimal_path)

                for items in inventory:
                    if len(random_item) != 0:
                        if random_item['name'] == items['type']:
                                index += 1
                                try:
                                    random_item = getItemFromPath(entities, index, optimal_path)
                                except:
                                        tp_command = "tp " + str(0.5)+ " 210 " + str(0.5)
                                        agent_host.sendCommand(tp_command)
                                        time.sleep(0.02)
                                        agent_host.sendCommand('quit')

                    else:
                        random_item = getItemFromPath(entities, index, optimal_path)

               
                best_yaw = findAngle(entities, random_item)
                agent_host.sendCommand("turn " + str(best_yaw))

                if index >= len(optimal_path):
                     tp_command = "tp " + str(0.5)+ " 210 " + str(0.5)
                     agent_host.sendCommand(tp_command)
                     time.sleep(0.02)
                     agent_host.sendCommand('quit')



                # Greedy Shortest Path

              #  item_value = CalculateDistance(entities)

              #  if len(item_value) == 0:
              #      tp_command = "tp " + str(0.5) + " 210 " + str(0.5)
              #      agent_host.sendCommand(tp_command)
              #      time.sleep(0.02)
              #      agent_host.sendCommand('quit')

              #  if len(random_item) == 0:
              #     random_item = getItem(entities, item_value)
              #     if (len(item_value) != 0):
              #         distance += min(item_value)

              #  for items in inventory:
              #      if len(random_item) != 0:
              #          if random_item['name'] == items['type']:
              #              random_item = getItem(entities, item_value)
              #              if len(item_value) != 0:
              #                  distance += min(item_value)
              #      else:
              #           random_item = getItem(entities, item_value)
              #           if len(item_value) != 0:
              #                  distance += min(item_value)
                
              #  if len(random_item) != 0:
              #      path.add(random_item["name"])

              #  best_yaw = findAngle(entities, random_item)
              #  agent_host.sendCommand("turn " + str(best_yaw))

              # A*
              #  if len(random_item) == 0:
              #      a_starpath = a_star((0.5, 0.5))
              #      path_dict = a_starpath[1]
              #      starpath = sorted(path_dict.items(), key = lambda kv: kv[1])
              #      random_item = starpath[1][0]

              #  for items in inventory:
              #      if len(random_item) != 0:
              #          if random_item['name'] == items['type']:
              #              for ent in entities:
              #                  if (ent['name'] == 'The Hunted'):
              #                      x_value = ent['x']
              #                      z_value = ent['z']
              #              a_starpath = a_star((x_value, z_value))
              #              path_dict = a_starpath[1]
              #              starpath = sorted(path_dict.items(), key = lambda kv: kv[1])
              #              random_item = starpath[1][0]
              #      else:
              #          a_starpath = a_star((0.5, 0.5))
              #  best_yaw = findAngle(entities, random_item)
              #  agent_host.sendCommand("turn " + str(best_yaw))

            time.sleep(0.01)
        
    ## mission has ended.
   
    for error in world_state.errors:
        print("Error:",error.text)

    #if world_state.number_of_rewards_since_last_state > 0:
    #    print("The agent scored " + str(total_reward))
    print("Time Needed: {}".format(time.time() - start_time))
    path = list(path)
    print("Optimal Path: {}".format(path))
    print("Total Distance Travelled: {}".format(distance))

   # print("Optimal Path: {}".format(optimal_path))
   # print("Total Distance Travelled: {}".format(total_distance))
   
    time.sleep(1) # Give the mod a little time to prepare for the next mission.