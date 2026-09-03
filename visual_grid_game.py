# visual_grid_game.py

import random
import tkinter as tk


class VisualGridHuntGame:
    """
    A flexible grid environment.

    Practical 02:
    The agent does NOT receive its exact global position.
    Instead, it receives local percepts such as:
        - wall_ahead
        - food_here
        - visited information
    """

    def __init__(
        self,
        width=10,
        height=10,
        num_food=10,
        num_opponents=0,
        custom_walls=None
    ):

        self.width = width
        self.height = height

        # Agent starts at (0, 0)
        self.agent_pos = [0, 0]

        # ---------------------------------------------------------
        # Walls
        # ---------------------------------------------------------

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        # ---------------------------------------------------------
        # Food
        # ---------------------------------------------------------

        self.food_positions = set()

        while len(self.food_positions) < num_food:

            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)

            food_pos = (fx, fy)

            if (
                food_pos != (0, 0)
                and food_pos not in self.walls
            ):
                self.food_positions.add(food_pos)

        # ---------------------------------------------------------
        # Opponents
        # ---------------------------------------------------------

        self.opponents = []

        while len(self.opponents) < num_opponents:

            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)

            opponent_pos = [ox, oy]

            if (
                tuple(opponent_pos) != (0, 0)
                and tuple(opponent_pos) not in self.walls
                and tuple(opponent_pos) not in self.food_positions
            ):
                self.opponents.append(opponent_pos)

        # ---------------------------------------------------------
        # Agent direction
        # ---------------------------------------------------------

        self.facing = 'Right'

        # ---------------------------------------------------------
        # Game information
        # ---------------------------------------------------------

        self.score = 0
        self.steps = 0
        self.collision = False

    # =============================================================
    # PRACTICAL 02 - STEP 1.1
    # PARTIALLY OBSERVABLE PERCEPT
    # =============================================================

    def get_percept(self) -> dict:

        return {
            'agent_pos': list(self.agent_pos),

            'opponent_positions': [
                list(op)
                for op in self.opponents
            ],

            'smells_food':
                tuple(self.agent_pos)
                in self.food_positions,

            'hit_wall':
                tuple(self.agent_pos)
                in self.walls,

            'collision':
                self.collision,

            'score':
                self.score,

            'remaining_food':
                len(self.food_positions),

            # Practical 03
            'grid_size':
                (self.width, self.height),

            'walls':
                list(self.walls),

            'all_food':
                list(self.food_positions)
        }
    # =============================================================
    # Direction Helpers
    # =============================================================

    def get_left_direction(self):

        directions = [
            'Up',
            'Left',
            'Down',
            'Right'
        ]

        index = directions.index(self.facing)

        return directions[
            (index + 1) % 4
        ]

    def get_right_direction(self):

        directions = [
            'Up',
            'Right',
            'Down',
            'Left'
        ]

        index = directions.index(self.facing)

        return directions[
            (index + 1) % 4
        ]

    # =============================================================
    # Execute Action
    # =============================================================

    def execute_action(self, action: str):

        self.steps += 1

        # ---------------------------------------------------------
        # Turning
        # ---------------------------------------------------------

        if action in [
            'Up',
            'Down',
            'Left',
            'Right'
        ]:

            self.facing = action

        # ---------------------------------------------------------
        # Calculate new position
        # ---------------------------------------------------------

        new_pos = list(self.agent_pos)

        if action == 'Up':

            new_pos[1] = min(
                self.height - 1,
                self.agent_pos[1] + 1
            )

        elif action == 'Down':

            new_pos[1] = max(
                0,
                self.agent_pos[1] - 1
            )

        elif action == 'Left':

            new_pos[0] = max(
                0,
                self.agent_pos[0] - 1
            )

        elif action == 'Right':

            new_pos[0] = min(
                self.width - 1,
                self.agent_pos[0] + 1
            )

        # ---------------------------------------------------------
        # Wall collision
        # ---------------------------------------------------------

        if tuple(new_pos) in self.walls:

            self.score -= 5

        else:

            self.agent_pos = new_pos

        # ---------------------------------------------------------
        # Food collection
        # ---------------------------------------------------------

        current_pos = tuple(self.agent_pos)

        if current_pos in self.food_positions:

            self.food_positions.remove(current_pos)

            self.score += 20

        # ---------------------------------------------------------
        # Opponent movement
        # ---------------------------------------------------------

        for op in self.opponents:

            move = random.choice(
                [
                    'Up',
                    'Down',
                    'Left',
                    'Right',
                    'Stay'
                ]
            )

            if move == 'Up' and op[1] < self.height - 1:
                op[1] += 1

            elif move == 'Down' and op[1] > 0:
                op[1] -= 1

            elif move == 'Left' and op[0] > 0:
                op[0] -= 1

            elif move == 'Right' and op[0] < self.width - 1:
                op[0] += 1

            if op == self.agent_pos:

                self.score -= 50

                self.collision = True

    # =============================================================
    # Game End
    # =============================================================

    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 60
            or self.collision
        )


# =================================================================
# GUI
# =================================================================

class GridGameGUI:

    def __init__(
        self,
        root,
        width=10,
        height=10,
        num_food=10,
        num_opponents=0,
        walls=None,
        agent_type="AStar"
    ):

        self.root = root

        self.root.title(
            "IT3012 - Practical 04 - A* Search"
        )

        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            custom_walls=walls
        )

        # ---------------------------------------------------------
        # Select Agent
        # ---------------------------------------------------------

        from agent import SearchAgent

        self.agent = SearchAgent()

        # Select algorithm
        self.agent.active_algo = agent_type

        # ---------------------------------------------------------
        # Canvas
        # ---------------------------------------------------------

        max_canvas_dim = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_dim // self.env.width,
                max_canvas_dim // self.env.height
            )
        )

        canvas_w = (
            self.env.width
            * self.cell_size
        )

        canvas_h = (
            self.env.height
            * self.cell_size
        )

        self.canvas = tk.Canvas(
            root,
            width=canvas_w,
            height=canvas_h,
            bg="white"
        )

        self.canvas.pack()

        # ---------------------------------------------------------
        # Label
        # ---------------------------------------------------------

        self.label = tk.Label(
            root,
            text="Score: 0 | Steps: 0",
            font=("Arial", 14)
        )

        self.label.pack(pady=10)

        # ---------------------------------------------------------
        # Button
        # ---------------------------------------------------------

        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12)
        )

        self.btn.pack(pady=5)

        self.draw_grid()

    # =============================================================
    # Draw Grid
    # =============================================================

    def draw_grid(self):

        self.canvas.delete("all")

        # ---------------------------------------------------------
        # Grid cells
        # ---------------------------------------------------------

        for x in range(self.env.width):

            for y in range(self.env.height):

                x1 = (
                    x
                    * self.cell_size
                )

                y1 = (
                    self.env.height
                    - 1
                    - y
                ) * self.cell_size

                x2 = (
                    x1
                    + self.cell_size
                )

                y2 = (
                    y1
                    + self.cell_size
                )

                if (x, y) in self.env.walls:

                    fill = "#64748b"

                else:

                    fill = "#f1f5f9"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="#cbd5e1"
                )

        # ---------------------------------------------------------
        # Food
        # ---------------------------------------------------------

        for fx, fy in self.env.food_positions:

            offset = (
                self.cell_size
                * 0.25
            )

            x1 = (
                fx
                * self.cell_size
                + offset
            )

            y1 = (
                (
                    self.env.height
                    - 1
                    - fy
                )
                * self.cell_size
                + offset
            )

            self.canvas.create_oval(
                x1,
                y1,
                x1 + self.cell_size * 0.5,
                y1 + self.cell_size * 0.5,
                fill="#f59e0b",
                outline="#d97706"
            )

        # ---------------------------------------------------------
        # Opponents
        # ---------------------------------------------------------

        for ox, oy in self.env.opponents:

            offset = (
                self.cell_size
                * 0.2
            )

            x1 = (
                ox
                * self.cell_size
                + offset
            )

            y1 = (
                (
                    self.env.height
                    - 1
                    - oy
                )
                * self.cell_size
                + offset
            )

            self.canvas.create_rectangle(
                x1,
                y1,
                x1 + self.cell_size * 0.6,
                y1 + self.cell_size * 0.6,
                fill="#990000",
                outline="#7a0000"
            )

        # ---------------------------------------------------------
        # Agent
        # ---------------------------------------------------------

        ax, ay = self.env.agent_pos

        offset = (
            self.cell_size
            * 0.15
        )

        x1 = (
            ax
            * self.cell_size
            + offset
        )

        y1 = (
            (
                self.env.height
                - 1
                - ay
            )
            * self.cell_size
            + offset
        )

        self.canvas.create_oval(
            x1,
            y1,
            x1 + self.cell_size * 0.7,
            y1 + self.cell_size * 0.7,
            fill="#000066",
            outline="#1e3a8a"
        )

    # =============================================================
    # Simulation
    # =============================================================

    def run_loop(self):

        self.btn.config(
            state="disabled"
        )

        def step():

            if not self.env.is_done():

                # -------------------------------------------------
                # Get percept from environment
                # -------------------------------------------------

                percept = self.env.get_percept()

                # -------------------------------------------------
                # Agent chooses action
                # -------------------------------------------------

                action = self.agent.sense_and_act(
                    percept
                )

                # -------------------------------------------------
                # Environment executes action
                # -------------------------------------------------

                self.env.execute_action(
                    action
                )

                # -------------------------------------------------
                # Update GUI
                # -------------------------------------------------

                self.draw_grid()

                self.label.config(
                    text=(
                        f"Algorithm: {self.agent.active_algo} | "
                        f"Score: {self.env.score} | "
                        f"Steps: {self.env.steps} | "
                        f"Action: {action}"
                    )
                )

                self.root.after(
                    300,
                    step
                )

            else:

                # -------------------------------------------------
                # Game finished
                # -------------------------------------------------

                if self.env.collision:

                    text = (
                        "Collision! Game Over! "
                        f"Final Score: {self.env.score}"
                    )

                elif len(self.env.food_positions) == 0:

                    text = (
                        f"{self.agent.active_algo} Finished! "
                        f"All food collected! "
                        f"Final Score: {self.env.score}"
                    )

                else:

                    text = (
                        f"{self.agent.active_algo} Finished! "
                        f"Final Score: {self.env.score}"
                    )

                self.label.config(
                    text=text
                )

                self.btn.config(
                    state="normal"
                )

        step()

# =================================================================
# MAIN
# =================================================================
if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=10,
        height=10,
        num_food=10,
        num_opponents=0,
        agent_type="AStar"
    )

    root.mainloop()