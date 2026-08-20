from collections import deque
import heapq


class SearchAgent:
    """
    Goal-Based Search Agent for Practical 03.

    Supports:
        - Breadth-First Search (BFS)
        - Depth-First Search (DFS)
        - Uniform-Cost Search (UCS)
    """

    def __init__(self):
        # Stores the actions that the agent has planned
        self.plan = []

        # Select search algorithm
        self.active_algo = 'BFS'

    # =========================================================
    # GET VALID NEIGHBORS
    # =========================================================

    def get_neighbors(self, state, walls, grid_size):
        """
        Return valid neighboring states and their actions.

        Returns:
            [(new_state, action), ...]
        """

        x, y = state
        width, height = grid_size

        possible_moves = [
            ((x, y + 1), 'Up'),
            ((x, y - 1), 'Down'),
            ((x - 1, y), 'Left'),
            ((x + 1, y), 'Right')
        ]

        neighbors = []

        for new_state, action in possible_moves:

            nx, ny = new_state

            # Check boundaries
            if nx < 0 or nx >= width:
                continue

            if ny < 0 or ny >= height:
                continue

            # Check walls
            if new_state in walls:
                continue

            neighbors.append(
                (new_state, action)
            )

        return neighbors

    # =========================================================
    # BFS
    # =========================================================

    def bfs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):
        """
        Breadth-First Search.

        Uses a FIFO queue and a reached set.

        Returns:
            List of actions representing the shortest path,
            or None if no path exists.
        """

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)

        walls = {
            tuple(wall)
            for wall in walls
        }

        # FIFO queue
        frontier = deque()

        frontier.append(
            (start_pos, [])
        )

        # Prevent repeated exploration
        reached = {start_pos}

        while frontier:

            current, path = frontier.popleft()

            # Goal test
            if current == goal_pos:
                return path

            # Expand node
            for neighbor, action in self.get_neighbors(
                current,
                walls,
                grid_size
            ):

                if neighbor not in reached:

                    reached.add(neighbor)

                    new_path = path + [action]

                    frontier.append(
                        (neighbor, new_path)
                    )

        # Goal unreachable
        return None

    # =========================================================
    # DFS
    # =========================================================

    def dfs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):
        """
        Depth-First Search.

        Uses a LIFO stack and a reached set.

        Returns:
            A path of actions, or None.
        """

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)

        walls = {
            tuple(wall)
            for wall in walls
        }

        # LIFO stack
        frontier = []

        frontier.append(
            (start_pos, [])
        )

        # Prevent cycles
        reached = {start_pos}

        while frontier:

            current, path = frontier.pop()

            # Goal test
            if current == goal_pos:
                return path

            for neighbor, action in self.get_neighbors(
                current,
                walls,
                grid_size
            ):

                if neighbor not in reached:

                    reached.add(neighbor)

                    new_path = path + [action]

                    frontier.append(
                        (neighbor, new_path)
                    )

        return None

    # =========================================================
    # UCS
    # =========================================================

    def ucs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):
        """
        Uniform-Cost Search.

        Uses heapq priority queue.

        Every movement has a cost of 1.
        """

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)

        walls = {
            tuple(wall)
            for wall in walls
        }

        # Priority queue:
        # (cost, counter, state, path)

        frontier = []

        counter = 0

        heapq.heappush(
            frontier,
            (
                0,
                counter,
                start_pos,
                []
            )
        )

        # Best known cost for each state
        reached = {
            start_pos: 0
        }

        while frontier:

            cost, _, current, path = heapq.heappop(
                frontier
            )

            # Goal test
            if current == goal_pos:
                return path

            # Expand node
            for neighbor, action in self.get_neighbors(
                current,
                walls,
                grid_size
            ):

                new_cost = cost + 1

                if (
                    neighbor not in reached
                    or new_cost < reached[neighbor]
                ):

                    reached[neighbor] = new_cost

                    counter += 1

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            counter,
                            neighbor,
                            new_path
                        )
                    )

        return None

    # =========================================================
    # SEARCH SELECTOR
    # =========================================================

    def search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):
        """
        Select the search algorithm.
        """

        if self.active_algo == 'BFS':

            return self.bfs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )

        elif self.active_algo == 'DFS':

            return self.dfs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )

        elif self.active_algo == 'UCS':

            return self.ucs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )

        else:

            raise ValueError(
                "Invalid search algorithm: "
                + str(self.active_algo)
            )

    # =========================================================
    # FIND CLOSEST REACHABLE FOOD
    # =========================================================

    def create_plan(self, percept):
        """
        Create a plan from the current position
        to one of the remaining food locations.

        Tries food locations in increasing Manhattan
        distance order.
        """

        start_pos = tuple(
            percept['agent_pos']
        )

        all_food = [
            tuple(food)
            for food in percept['all_food']
        ]

        walls = {
            tuple(wall)
            for wall in percept['walls']
        }

        grid_size = percept['grid_size']

        if not all_food:
            return None

        # Try closest food first
        food_targets = sorted(
            all_food,
            key=lambda food:
                abs(start_pos[0] - food[0])
                +
                abs(start_pos[1] - food[1])
        )

        # Try each food until a path is found
        for food in food_targets:

            path = self.search(
                start_pos,
                food,
                walls,
                grid_size
            )

            if path is not None:

                return path

        return None

    # =========================================================
    # SENSE AND ACT
    # =========================================================

    def sense_and_act(
        self,
        percept: dict
    ) -> str:
        """
        Return the next action from the current plan.

        If the current plan is empty, create a new plan.
        """

        # -----------------------------------------------------
        # Create a new plan if necessary
        # -----------------------------------------------------

        if not self.plan:

            new_plan = self.create_plan(
                percept
            )

            if new_plan is not None:
                self.plan = new_plan

        # -----------------------------------------------------
        # Execute next planned action
        # -----------------------------------------------------

        if self.plan:

            return self.plan.pop(0)

        # No valid path
        return 'Stay'