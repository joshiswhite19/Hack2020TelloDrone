# Hackathon To-Do List

## Main Objectives

- Drone shall patrol a designated area, which shall be clearly marked
- Drone shall not leave the designated drone patrolling area
- When the drone identifies a specified household item, the drone shall execute an action assigned by the participant
- Drone shall take appropriate action for a given target (ignore, follow, flag for hugging)
- (Optional, Advanced) When an object such as a ball enters the patrol area, the drone shall stop its previous activity and follow the object until it leaves the patrol area

## Key Components (in order of importance)

- Designated area detection and control (opencv and flight controls)
- Household object identification (opencv)
- Identified object record keeping and management
- Appropriate action logic

## Secondary Components

- Drone status checking
- Aborts, safety
- Simulation mode
- Exception handling
