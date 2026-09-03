# agent.py

class SimpleReflexAgent:
    """
    Simple Reflex Agent.

    The agent makes decisions only from the current percept.
    It does not maintain any history or internal state.
    """

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:

        # Condition-Action Rule 1
        # IF food is here THEN move onto the food
        if percept['food_here']:
            return percept['food_action']

        # Condition-Action Rule 2
        # IF there is a wall ahead THEN turn left
        if percept['wall_ahead']:
            return percept['turn_left']

        # Condition-Action Rule 3
        # ELSE move forward
        return percept['forward']


class ModelBasedAgent:
    """
    Model-Based Agent.

    This agent maintains an internal state using memory.
    It remembers cells that it has already visited.
    """

    def __init__(self):
        # Internal memory
        self.visited_cells = set()

        # Remember the previous action
        self.last_action = None

        # Current estimated position
        self.current_position = (0, 0)

    def sense_and_act(self, percept: dict) -> str:

        # ---------------------------------------------------------
        # Step 1: Update Internal State
        # ---------------------------------------------------------

        current_pos = percept['estimated_pos']

        # Record the current cell
        self.visited_cells.add(current_pos)

        # ---------------------------------------------------------
        # Step 2: Store the last action
        # ---------------------------------------------------------

        if self.last_action is not None:
            self.last_action = self.last_action

        # ---------------------------------------------------------
        # Step 3: Condition-Action Rules
        # ---------------------------------------------------------

        # IF food is here THEN move forward
        if percept['food_here']:
            action = percept['forward']

        # IF wall ahead AND left cell has not been visited
        # THEN turn left
        elif percept['wall_ahead'] and not percept['left_visited']:
            action = percept['turn_left']

        # IF wall ahead AND left cell is visited
        # THEN turn right
        elif percept['wall_ahead'] and percept['left_visited']:
            action = percept['turn_right']

        # IF forward cell has already been visited
        # THEN try another direction
        elif percept['forward_visited']:
            if not percept['right_visited']:
                action = percept['turn_right']
            elif not percept['left_visited']:
                action = percept['turn_left']
            else:
                action = percept['turn_right']

        # Otherwise continue forward
        else:
            action = percept['forward']

        # Store the action in memory
        self.last_action = action

        return action