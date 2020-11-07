# Hackathon To-Do List

## Main Objectives

- Drone shall patrol a designated area, which shall be clearly marked
- Drone shall not leave the designated drone patrolling area
- When the drone identifies a specified household item, the drone shall execute an action assigned by the participant
- Drone shall take appropriate action for a given target (ignore, follow, flag for hugging)
- (Optional, Advanced) When an object such as a ball enters the patrol area, the drone shall stop its previous activity and follow the object until it leaves the patrol area

## Key Components (in order of importance)

- Designated area detection and control (opencv and flight controls)
- - On start, scope out perimeter kinda like a 3d printer zeroing itself?
- Standard patrol procedure (flight controls)
- Household object identification (opencv)
- - Maybe use object mats?
- Identified object record keeping and management (mainly record keeping)
- - Make a dictionary of objects that stores timestamp and last known location
- Appropriate action logic (flight controls mainly)

## Secondary Components

- Drone status checking
- - Make sure it's in good condition before taking off and whatnot
- Aborts, safety
- - Keep away from objects and land safely if in weird state
- Simulation mode
- - Set up to help debug logic and whatnot
- Exception handling
- - Kinda feeds into everything else
give lots of hugs