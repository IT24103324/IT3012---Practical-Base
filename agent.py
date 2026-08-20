class SimpleReflexAgent:
    """
    Simple Reflex Agent.

    Uses only the current percept.
    Does not maintain memory/history.
    """

    def sense_and_act(self, percept: dict) -> str:

        # Rule 1:
        # IF food is here THEN collect it
        if percept['food_here']:
            return 'Suck'

        # Rule 2:
        # IF wall is ahead THEN turn left
        elif percept['wall_ahead']:
            return 'Left'

        # Rule 3:
        # ELSE move forward
        else:
            return 'Forward'


class ModelBasedAgent:
    """
    Model-Based Agent.

    Maintains internal state/memory about visited cells
    and previous actions.
    """

    def __init__(self):

        # Internal memory
        self.visited_cells = set()

        # Last action performed
        self.last_action = None

        # Internal estimated position
        self.internal_position = [0, 0]

        # Current direction
        self.direction = 'Right'

        # Number of consecutive wall encounters
        self.wall_count = 0

    def sense_and_act(self, percept: dict) -> str:

        # =====================================================
        # 1. UPDATE INTERNAL STATE
        # =====================================================

        # Record current estimated position
        current_cell = tuple(
            self.internal_position
        )

        self.visited_cells.add(
            current_cell
        )

        # =====================================================
        # 2. FOOD RULE
        # =====================================================

        if percept['food_here']:

            action = 'Suck'

            self.last_action = action

            return action

        # =====================================================
        # 3. WALL DETECTED
        # =====================================================

        if percept['wall_ahead']:

            self.wall_count += 1

            # Change direction when wall encountered
            if self.wall_count % 2 == 1:

                action = 'Left'

            else:

                action = 'Right'

            self.last_action = action

            self.update_internal_state(action)

            return action

        # =====================================================
        # 4. NORMAL MOVEMENT
        # =====================================================

        self.wall_count = 0

        action = 'Forward'

        self.last_action = action

        self.update_internal_state(action)

        return action

    def update_internal_state(self, action):

        """
        Update the internal model based on the
        selected action.
        """

        # -----------------------------------------------------
        # Turning
        # -----------------------------------------------------

        if action == 'Left':

            directions = [
                'Up',
                'Left',
                'Down',
                'Right'
            ]

            index = directions.index(
                self.direction
            )

            self.direction = directions[
                (index + 1) % 4
            ]

        elif action == 'Right':

            directions = [
                'Up',
                'Right',
                'Down',
                'Left'
            ]

            index = directions.index(
                self.direction
            )

            self.direction = directions[
                (index + 1) % 4
            ]

        # -----------------------------------------------------
        # Moving forward
        # -----------------------------------------------------

        elif action == 'Forward':

            if self.direction == 'Up':
                self.internal_position[1] += 1

            elif self.direction == 'Down':
                self.internal_position[1] -= 1

            elif self.direction == 'Left':
                self.internal_position[0] -= 1

            elif self.direction == 'Right':
                self.internal_position[0] += 1


class GreedyGridAgent:
    """
    Kept for compatibility with the original starter code.
    """

    def __init__(self):

        self.actions_pool = [
            'Forward',
            'Left',
            'Right'
        ]

    def sense_and_act(self, percept: dict) -> str:

        if percept.get('food_here', False):
            return 'Suck'

        if percept.get('wall_ahead', False):
            return 'Left'

        return 'Forward'