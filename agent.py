# agent.py

from collections import deque
import heapq
import math


class SearchAgent:
    """
    Goal-Based / Planning Agent for Practical 04.

    Supports:
    - BFS
    - DFS
    - UCS
    - AStar
    """

    def __init__(self):
        # Stores the planned sequence of actions
        self.plan = []

        # Select search algorithm
        # Options:
        # "BFS"
        # "DFS"
        # "UCS"
        # "AStar"
        self.active_algo = "AStar"

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

            neighbors.append(
                (new_state, action)
            )

        return neighbors

    # =============================================================
    # BFS SEARCH
    # =============================================================

    def bfs_search(self, start, goal, grid_size, walls):

        # FIFO Queue
        frontier = deque()

        frontier.append(
            (start, [])
        )

        # Reached set
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

        frontier.append(
            (start, [])
        )

        # Reached set
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

        # Stores cheapest known cost
        reached = {}

        while frontier:

            cost, state, path = heapq.heappop(
                frontier
            )

            # Skip if already reached with lower cost
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
    # MANHATTAN DISTANCE
    # =============================================================

    def manhattan_distance(self, pos, goal):

        x1, y1 = pos
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)

    # =============================================================
    # EUCLIDEAN DISTANCE
    # =============================================================

    def euclidean_distance(self, pos, goal):

        x1, y1 = pos
        x2, y2 = goal

        return math.sqrt(
            (x1 - x2) ** 2 +
            (y1 - y2) ** 2
        )

    # =============================================================
    # A* SEARCH
    # =============================================================

    def astar_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size,
        heuristic_type='manhattan'
    ):

        # ---------------------------------------------------------
        # Priority Queue
        # ---------------------------------------------------------

        frontier = []

        # g(n) = 0 at start
        start_g = 0

        # ---------------------------------------------------------
        # Calculate h(n)
        # ---------------------------------------------------------

        if heuristic_type == 'euclidean':

            start_h = self.euclidean_distance(
                start_pos,
                goal_pos
            )

        else:

            start_h = self.manhattan_distance(
                start_pos,
                goal_pos
            )

        # f(n) = g(n) + h(n)
        start_f = start_g + start_h

        # Format:
        # (f_cost, g_cost, current_pos, path_taken)

        heapq.heappush(
            frontier,
            (
                start_f,
                start_g,
                start_pos,
                []
            )
        )

        # ---------------------------------------------------------
        # Reached States
        # ---------------------------------------------------------

        reached_states = set()

        # ---------------------------------------------------------
        # Search
        # ---------------------------------------------------------

        while frontier:

            f_cost, g_cost, current_pos, path_taken = (
                heapq.heappop(frontier)
            )

            # -----------------------------------------------------
            # Goal Test
            # -----------------------------------------------------

            if current_pos == goal_pos:

                return path_taken

            # -----------------------------------------------------
            # Skip already reached states
            # -----------------------------------------------------

            if current_pos in reached_states:

                continue

            reached_states.add(
                current_pos
            )

            # -----------------------------------------------------
            # Current position
            # -----------------------------------------------------

            x, y = current_pos

            width, height = grid_size

            # -----------------------------------------------------
            # Four possible movements
            # -----------------------------------------------------

            possible_moves = [
                ("Up", (x, y + 1)),
                ("Down", (x, y - 1)),
                ("Left", (x - 1, y)),
                ("Right", (x + 1, y))
            ]

            # -----------------------------------------------------
            # Expand neighbors
            # -----------------------------------------------------

            for action, next_pos in possible_moves:

                nx, ny = next_pos

                # Check grid boundaries
                if nx < 0 or nx >= width:
                    continue

                if ny < 0 or ny >= height:
                    continue

                # Check walls
                if next_pos in walls:
                    continue

                # Check reached states
                if next_pos in reached_states:
                    continue

                # -------------------------------------------------
                # Calculate new g(n)
                # -------------------------------------------------

                new_g = g_cost + 1

                # -------------------------------------------------
                # Calculate new h(n)
                # -------------------------------------------------

                if heuristic_type == 'euclidean':

                    new_h = self.euclidean_distance(
                        next_pos,
                        goal_pos
                    )

                else:

                    new_h = self.manhattan_distance(
                        next_pos,
                        goal_pos
                    )

                # -------------------------------------------------
                # Calculate new f(n)
                # -------------------------------------------------

                new_f = new_g + new_h

                # New path
                new_path = path_taken + [action]

                # -------------------------------------------------
                # Add to priority queue
                # -------------------------------------------------

                heapq.heappush(
                    frontier,
                    (
                        new_f,
                        new_g,
                        next_pos,
                        new_path
                    )
                )

        # No solution
        return []

    # =============================================================
    # Find Closest Food
    # =============================================================

    def find_closest_food(
        self,
        start,
        food_positions
    ):

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
            start = tuple(
                percept["agent_pos"]
            )

            # Find closest food
            goal = self.find_closest_food(
                start,
                percept["all_food"]
            )

            # No food remaining
            if goal is None:

                return "Stay"

            # -----------------------------------------------------
            # Get environment information
            # -----------------------------------------------------

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

            elif self.active_algo == "AStar":

                self.plan = self.astar_search(
                    start_pos=start,
                    goal_pos=goal,
                    walls=walls,
                    grid_size=grid_size,
                    heuristic_type="manhattan"
                )

        # ---------------------------------------------------------
        # Execute next action from plan
        # ---------------------------------------------------------

        if self.plan:

            return self.plan.pop(0)

        # No path found
        return "Stay"


# =============================================================
# TEST HEURISTIC FUNCTIONS
# =============================================================

if __name__ == "__main__":

    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 4)

    print(
        "Manhattan Distance:",
        agent.manhattan_distance(
            start,
            goal
        )
    )

    print(
        "Euclidean Distance:",
        agent.euclidean_distance(
            start,
            goal
        )
    )