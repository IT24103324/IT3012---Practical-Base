# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""
#test
    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

import random

class SimpleReflexAgent:
    """
    Step 1.2: A Simple Reflex Agent that reacts ONLY to the current percept.
    Notice there is no __init__ method to store memory.
    """
    def sense_and_act(self, percept: dict) -> str:
        # Condition-Action Rules (IF-THEN logic)
        if percept.get('food_here'):
            return 'Stay'  # Action when on food
            
        elif percept.get('wall_ahead'):
            return 'Left'  # Deterministic action: always turn left if blocked
            
        else:
            return 'Up'    # Default action: always move up if clear


class ModelBasedAgent:
    """
    Step 1.3: A Model-Based Agent that maintains an internal state (memory)
    to escape infinite loops.
    """
    def __init__(self):
        # Initialize internal memory state
        self.last_action = None
        self.consecutive_walls_hit = 0

    def sense_and_act(self, percept: dict) -> str:
        # 1. Update Internal State (Transition & Sensor Model)
        if percept.get('wall_ahead'):
            self.consecutive_walls_hit += 1
        else:
            self.consecutive_walls_hit = 0

        # 2. Condition-Action Rules querying both Percept AND Memory
        if percept.get('food_here'):
            action = 'Stay'
            
        elif percept.get('wall_ahead'):
            # If we've hit a wall multiple times in a row, our memory tells us 
            # turning 'Left' isn't working, so we try something else.
            if self.consecutive_walls_hit > 1:
                action = 'Right'
            else:
                action = 'Left'
                
        else:
            action = 'Up'

        # 3. Record the action we are about to take
        self.last_action = action
        return action