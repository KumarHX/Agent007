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
import os
import random
import sys
import time
import json
import random
import errno
import math
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

malmoutils.fix_print()

agent_host = MalmoPython.AgentHost()
malmoutils.parse_command_line(agent_host)

# Task parameters:
NUM_GOALS = 100
ARENA_WIDTH = 180
ARENA_BREADTH = 180
MOB_TYPE = "Endermite"  # Change for fun, but note that spawning conditions have to be correct - eg spiders will require darker conditions.


# Display parameters:
CANVAS_BORDER = 20
CANVAS_WIDTH = 400
CANVAS_HEIGHT = CANVAS_BORDER + ((CANVAS_WIDTH - CANVAS_BORDER) * ARENA_BREADTH / ARENA_WIDTH)
CANVAS_SCALEX = old_div((CANVAS_WIDTH-CANVAS_BORDER),ARENA_WIDTH)
CANVAS_SCALEY = old_div((CANVAS_HEIGHT-CANVAS_BORDER),ARENA_BREADTH)
CANVAS_ORGX = old_div(-ARENA_WIDTH,CANVAS_SCALEX)
CANVAS_ORGY = old_div(-ARENA_BREADTH,CANVAS_SCALEY)

# Agent parameters:
agent_stepsize = 1
agent_search_resolution = 30
agent_edge_weight = -100
agent_turn_weight = 0


#GOAL_TYPES = ['apple','book','egg','beef','chicken',
#              'potato','golden_carrot','porkchop','paper','diamond']

#GOAL_TYPES_WITH_REWARDS = { 'apple': 10,
#                            'book': 200,
#                            'egg': -10,
#                            'beef': -100,
#                            'chicken': -50,
#                            'potato': 50,
#                            'golden_carrot': 100,
#                            'porkchop': -150,
#                            'paper': 120,
#                            'diamond': 180}

GOAL_TYPES = ["bowl", "red_mushroom", "brown_mushroom", "pumpkin", "egg", "sugar", 
              "carrot", "cooked_rabbit", "baked_potato", "bread", "melon", "cookie"]

GOAL_TYPES_WITH_REWARDS = {'bowl': -1, 'red_mushroom':5, 'brown_mushroom':5, 'pumpkin':-5, 'egg': -25, 'sugar':-10,
               'carrot': -10, 'cooked_rabbit': 10, 'baked_potato': 5, 'bread': 2,
               'melon': 5, 'cookie':5,
               'mushroom_stew': 50, 'pumpkin_pie': 50, 'rabbit_stew': 100,
               'melon_seeds': -100, 'pumpkin_seeds': -50
              }

food_recipes = {'mushroom_stew': ['bowl', 'red_mushroom'],
                'pumpkin_pie': ['pumpkin', 'egg', 'sugar'],
                'rabbit_stew': ['cooked_rabbit', 'carrot', 'baked_potato', 'red_mushroom', 'bowl'],
                'melon_seeds': ['melon'],
                'pumpkin_seeds': ['pumpkin'],
               }

GOAL_POSITIONS = [[50,-87],[4,14],[-65,31],[1,50],[-48,24],[-51,-12],[-41,-32],[4,-55],[28,-46],[29,-60],[78,27],[-57,53],[70,67],[-87,-71],[8,-8],[7,-10],[-15,60],[-75,30],[11,-9],
                  [-30,-62],[26,-33],[-21,-73],[-61,-74],[13,-77],[-48,15],[7,14],[-53,-46],[-45,-12],[6,27],[-26,-60],[46,-15],[-50,-27],[24,-32],[-62,-33],[-15,-12],[75,-18],
                  [-56,63],[-52,-76],[77,55],[-85,-68],[-31,-23],[-32,-72],[2,59],[68,-71],[-71,58],[34,74],[-61,-8],[-8,61],[-35,-47],[-75,-28],[73,86],[-64,-33],
                  [-18,30],[11,76],[15,-40],[-79,80],[24,83],[-49,-7],[32,-68],[-59,14],[-33,-17],[26,37],[42,-31],[28,80],[36,32],[-6,13],[-72,-28],[-12,-79],[27,-39],
                  [13,-90],[79,-67],[-29,30],[74,-5],[-23,-69],[22,30],[38,25],[57,73],[46,7],[-56,-15],[42,-76],[46,-69],[19,-52],[54,23],[-2,-73],[0,-24],[-10,-1],[-85,71],
                  [9,-2],[30,-73],[47,-40],[-8,36],[87,-14],[-18,88],[43,-81],[-83,-6],[-57,-27],[29,-33],[15,-90],[39,-62],[22,-66]]

def getItemXML():
    ''' Build an XML string that contains some randomly positioned goal items'''
    xml=""
    for item in range(NUM_GOALS):
        X = str(GOAL_POSITIONS[item][0])
        Z = str(GOAL_POSITIONS[item][1])
        if item < 10 :
            xml += '''<DrawItem x="''' + X + '''" y="210" z="''' + Z + '''" type="''' + GOAL_TYPES[item] + '''"/>'''
        else:
            k = item
            while ( k > 9):
                k -= 10
            xml += '''<DrawItem x="''' + X + '''" y="210" z="''' + Z + '''" type="''' + GOAL_TYPES[k] + '''"/>'''
    return xml

def getCorner(index: object, top: object, left: object, expand: object = 0, y: object = 206) -> object:
    ''' Return part of the XML string that defines the requested corner'''
    x = str(-(expand+old_div(ARENA_WIDTH,2))) if left else str(expand+old_div(ARENA_WIDTH,2))
    z = str(-(expand+old_div(ARENA_BREADTH,2))) if top else str(expand+old_div(ARENA_BREADTH,2))
    return 'x'+index+'="'+x+'" y'+index+'="' +str(y)+'" z'+index+'="'+z+'"'

def getRewardXml():
    xml = ""
    for keys, values in GOAL_TYPES_WITH_REWARDS.items():
        xml += '''<Item type = "''' + str(keys) + '''" reward="''' + str(values) + '''"/>'''
    
    return xml

def getMissionXML(summary):
    ''' Build an XML mission string.'''
    spawn_end_tag = ' type="mob_spawner" variant="' + MOB_TYPE + '"/>'
    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + summary + '''</Summary>
        </About>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <AllowSpawning>false</AllowSpawning>
                <AllowedMobs>''' + MOB_TYPE + '''</AllowedMobs>
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
                <ContinuousMovementCommands turnSpeedDegs="960"/>
                <AbsoluteMovementCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="'''+str(ARENA_WIDTH)+'''" yrange="2" zrange="'''+str(ARENA_BREADTH)+'''" />
                </ObservationFromNearbyEntities>
                <ObservationFromFullStats/>
                <RewardForCollectingItem>
                   ''' + getRewardXml() + '''
                </RewardForCollectingItem>''' + malmoutils.get_video_xml(agent_host) + '''
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
    if flash:
        canvas.create_rectangle(0,0,CANVAS_WIDTH,CANVAS_HEIGHT,fill="#ff0000") # Pain.
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
            cost = float(GOAL_TYPES_WITH_REWARDS[items['name']]) / hypotenuse
            items_value.append(cost)

    return items_value

def getItem(entities, item_value):
    goal_item = {}
    print(item_value)

    z_value = 0.0
    x_value = 0.0

    for ent in entities:
        if (ent['name'] == 'The Hunted'):
            x_value = ent['x']
            z_value = ent['z']

        if (ent['name'] != 'The Hunted'):
            if (total_commands %10 == 0 and len(item_value) > 0):
                random_index = random.randint(0, len(item_value) - 1)
                if ((float(GOAL_TYPES_WITH_REWARDS[ent['name']]) / math.sqrt((x_value - ent['x'])** 2 + (z_value - ent['z'])**2)) == item_value[random_index]):
                    goal_item = ent
                    return goal_item

            elif ((float(GOAL_TYPES_WITH_REWARDS[ent['name']]) / math.sqrt((x_value - ent['x'])** 2 + (z_value - ent['z'])**2)) == max(item_value)):
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
    
    # convert radius to angle
    angle = ((angle / math.pi * 180) - current_angle)%360

    if angle < 180:
        angle /= 360
    elif angle > 180:
        angle = (angle - 360)/360

    return angle

validate = True
# Create a pool of Minecraft Mod clients.
# By default, mods will choose consecutive mission control ports, starting at 10000,
# so running four mods locally should produce the following pool by default (assuming nothing else
# is using these ports):
my_client_pool = MalmoPython.ClientPool()
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10001))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10002))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10003))

if agent_host.receivedArgument("test"):
    num_reps = 1
else:
    num_reps = 30000

current_yaw = 0
current_life = 0

for iRepeat in range(num_reps):
    mission_xml = getMissionXML(MOB_TYPE + " Apocalypse #" + str(iRepeat))
    my_mission = MalmoPython.MissionSpec(mission_xml,validate)
    max_retries = 3
    # Set up a recording
    my_mission_record = malmoutils.get_default_recording_object(agent_host, "Mission_" + str(iRepeat))
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

    # main loop:
    total_reward = 0
    total_commands = 0
    flash = False

    while world_state.is_mission_running:
        world_state = agent_host.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            if "Yaw" in ob:
                current_yaw = ob['Yaw']

            if "Life" in ob:
                life = ob['Life']
                if life < current_life:
                    flash = True
                current_life = life


            if "entities" in ob:
                entities = ob['entities']
                drawMobs(entities, flash)
                item_value = CalculateDistance(entities)
                best_yaw = findAngle(entities, getItem(entities, item_value))

                #best_yaw = getBestAngle(entities, current_yaw, current_life)
                #difference = best_yaw - current_yaw;
                #while difference < -180:
                #    difference += 360;
                #while difference > 180:
                #    difference -= 360;
                #difference /= 180.0;

                agent_host.sendCommand("turn " + str(best_yaw))
                total_commands += 1

        if world_state.number_of_rewards_since_last_state > 0:
            # A reward signal has come in - see what it is:
            total_reward += world_state.rewards[-1].getValue()
        time.sleep(0.02)
        flash = False

    # mission has ended.
    for error in world_state.errors:
        print("Error:",error.text)
    if world_state.number_of_rewards_since_last_state > 0:
        # A reward signal has come in - see what it is:
        total_reward += world_state.rewards[-1].getValue()

    print("We stayed alive for " + str(total_commands) + " commands, and scored " + str(total_reward))
    time.sleep(1) # Give the mod a little time to prepare for the next mission.
