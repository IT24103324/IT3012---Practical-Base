# agent.py

from collections import deque
import heapq


class SearchAgent:
    """
    Goal-Based / Planning Agent for Practical 03.

    Supports:
    - BFS
    - DFS
    - UCS
    """

    def __init__(self):
        # Stores the planned sequence of actions
        self.plan = []

        # Change this to:
        # "BFS", "DFS", or "UCS"
        self.active_algo = "BFS"

    # =============================================================
    # Get Valid Neighbors
    # =============================================================

    def get_neighbors(self, state, grid_size, walls):

        x, y = state

        width, height = grid_size

        possible_moves = [
            ("Up", (x, y + 1)),
            ("Down", (x, y - 1)),
            ("Left", (x - 1, y)),
            ("Right", (x + 1, y))
        ]

        neighbors = []

        for action, new_state in possible_moves:

            nx, ny = new_state

            # Check grid boundaries
            if nx < 0 or nx >= width:
                continue

            if ny < 0 or ny >= height:
                continue

            # Check walls
            if new_state in walls:
                continue

            neighbors.append((new_state, action))

        return neighbors

    # =============================================================
    # BFS SEARCH
    # =============================================================

    def bfs_search(self, start, goal, grid_size, walls):

        # FIFO Queue
        frontier = deque()

        frontier.append((start, []))

        # Graph-search reached set
        reached = {start}

        while frontier:

            state, path = frontier.popleft()

            # Goal test
            if state == goal:
                return path

            # Expand neighbors
            for next_state, action in self.get_neighbors(
                state,
                grid_size,
                walls
            ):

                if next_state not in reached:

                    reached.add(next_state)

                    new_path = path + [action]

                    frontier.append(
                        (next_state, new_path)
                    )

        # No solution
        return []

    # =============================================================
    # DFS SEARCH
    # =============================================================

    def dfs_search(self, start, goal, grid_size, walls):

        # LIFO Stack
        frontier = []

        frontier.append((start, []))

        # Graph-search reached set
        reached = {start}

        while frontier:

            state, path = frontier.pop()

            # Goal test
            if state == goal:
                return path

            # Expand neighbors
            for next_state, action in self.get_neighbors(
                state,
                grid_size,
                walls
            ):

                if next_state not in reached:

                    reached.add(next_state)

                    new_path = path + [action]

                    frontier.append(
                        (next_state, new_path)
                    )

        # No solution
        return []

    # =============================================================
    # UCS SEARCH
    # =============================================================

    def ucs_search(self, start, goal, grid_size, walls):

        # Priority Queue
        # Format:
        # (cost, state, path)

        frontier = []

        heapq.heappush(
            frontier,
            (0, start, [])
        )

        # Stores the cheapest known cost
        reached = {}

        while frontier:

            cost, state, path = heapq.heappop(frontier)

            # If we already reached this state cheaper,
            # skip this path.
            if state in reached and reached[state] <= cost:
                continue

            reached[state] = cost

            # Goal test
            if state == goal:
                return path

            # Expand neighbors
            for next_state, action in self.get_neighbors(
                state,
                grid_size,
                walls
            ):

                new_cost = cost + 1

                if (
                    next_state not in reached
                    or new_cost < reached[next_state]
                ):

                    new_path = path + [action]

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            next_state,
                            new_path
                        )
                    )

        # No solution
        return []

    # =============================================================
    # Find Closest Food
    # =============================================================

    def find_closest_food(self, start, food_positions):

        if not food_positions:
            return None

        closest_food = None
        closest_distance = float("inf")

        for food in food_positions:

            distance = (
                abs(start[0] - food[0])
                + abs(start[1] - food[1])
            )

            if distance < closest_distance:

                closest_distance = distance
                closest_food = food

        return closest_food

    # =============================================================
    # SENSE AND ACT
    # =============================================================

    def sense_and_act(self, percept):

        # ---------------------------------------------------------
        # If there is no current plan, create a new plan
        # ---------------------------------------------------------

        if not self.plan:

            # Current agent position
            start = tuple(percept["agent_pos"])

            # Find closest food
            goal = self.find_closest_food(
                start,
                percept["all_food"]
            )

            # No food remaining
            if goal is None:
                return "Stay"

            # Get environment information
            grid_size = percept["grid_size"]

            walls = set(
                tuple(wall)
                for wall in percept["walls"]
            )

            # -----------------------------------------------------
            # Select Search Algorithm
            # -----------------------------------------------------

            if self.active_algo == "BFS":

                self.plan = self.bfs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            elif self.active_algo == "DFS":

                self.plan = self.dfs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

            elif self.active_algo == "UCS":

                self.plan = self.ucs_search(
                    start,
                    goal,
                    grid_size,
                    walls
                )

        # ---------------------------------------------------------
        # Execute next action from plan
        # ---------------------------------------------------------

        if self.plan:

            return self.plan.pop(0)

        # If no path exists
        return "Stay"