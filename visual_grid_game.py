import random
import tkinter as tk


class VisualGridHuntGame:
    """
    Grid environment for Practical 03.

    Provides global state information required by
    the SearchAgent.
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

        # Agent direction retained for GUI compatibility
        self.agent_direction = 'Right'

        # -----------------------------------------------------
        # Walls
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Food
        # -----------------------------------------------------

        self.food_positions = set()

        while len(self.food_positions) < num_food:

            fx = random.randint(
                0,
                self.width - 1
            )

            fy = random.randint(
                0,
                self.height - 1
            )

            food_pos = (fx, fy)

            if (
                food_pos != (0, 0)
                and food_pos not in self.walls
            ):
                self.food_positions.add(food_pos)

        # -----------------------------------------------------
        # Opponents
        # -----------------------------------------------------

        self.opponents = []

        while len(self.opponents) < num_opponents:

            ox = random.randint(
                0,
                self.width - 1
            )

            oy = random.randint(
                0,
                self.height - 1
            )

            opponent_pos = [ox, oy]

            if (
                tuple(opponent_pos) != (0, 0)
                and tuple(opponent_pos) not in self.walls
                and tuple(opponent_pos) not in self.food_positions
            ):
                self.opponents.append(opponent_pos)

        # -----------------------------------------------------
        # Game state
        # -----------------------------------------------------

        self.score = 0
        self.steps = 0
        self.collision = False

    # =========================================================
    # PRACTICAL 03 - GLOBAL PERCEPT
    # =========================================================

    def get_percept(self) -> dict:
        """
        Expose the global state required by the SearchAgent.
        """

        return {
            'agent_pos': list(self.agent_pos),

            'grid_size': (
                self.width,
                self.height
            ),

            'walls': list(self.walls),

            'all_food': list(
                self.food_positions
            ),

            'food_here': (
                tuple(self.agent_pos)
                in self.food_positions
            ),

            'score': self.score,

            'remaining_food': len(
                self.food_positions
            )
        }

    # =========================================================
    # ACTION EXECUTION
    # =========================================================

    def execute_action(self, action: str):
        """
        Execute an action produced by SearchAgent.

        Supported actions:
            Up
            Down
            Left
            Right
            Suck
            Forward
        """

        self.steps += 1

        # -----------------------------------------------------
        # SearchAgent movement actions
        # -----------------------------------------------------

        new_pos = list(self.agent_pos)

        if action == 'Up':

            new_pos[1] += 1
            self.agent_direction = 'Up'

        elif action == 'Down':

            new_pos[1] -= 1
            self.agent_direction = 'Down'

        elif action == 'Left':

            new_pos[0] -= 1
            self.agent_direction = 'Left'

        elif action == 'Right':

            new_pos[0] += 1
            self.agent_direction = 'Right'

        # -----------------------------------------------------
        # Forward action
        # -----------------------------------------------------

        elif action == 'Forward':

            if self.agent_direction == 'Up':
                new_pos[1] += 1

            elif self.agent_direction == 'Down':
                new_pos[1] -= 1

            elif self.agent_direction == 'Left':
                new_pos[0] -= 1

            elif self.agent_direction == 'Right':
                new_pos[0] += 1

        # -----------------------------------------------------
        # Suck action
        # -----------------------------------------------------

        elif action == 'Suck':

            current_pos = tuple(
                self.agent_pos
            )

            if current_pos in self.food_positions:

                self.food_positions.remove(
                    current_pos
                )

                self.score += 20

            return

        # -----------------------------------------------------
        # Check boundaries
        # -----------------------------------------------------

        outside_grid = (
            new_pos[0] < 0
            or new_pos[0] >= self.width
            or new_pos[1] < 0
            or new_pos[1] >= self.height
        )

        # -----------------------------------------------------
        # Check wall
        # -----------------------------------------------------

        if (
            outside_grid
            or tuple(new_pos) in self.walls
        ):

            self.score -= 5

        else:

            self.agent_pos = new_pos

        # -----------------------------------------------------
        # Collect food automatically
        # -----------------------------------------------------

        current_pos = tuple(
            self.agent_pos
        )

        if current_pos in self.food_positions:

            self.food_positions.remove(
                current_pos
            )

            self.score += 20

        # -----------------------------------------------------
        # Move opponents
        # -----------------------------------------------------

        for opponent in self.opponents:

            move = random.choice([
                'Up',
                'Down',
                'Left',
                'Right',
                'Stay'
            ])

            if (
                move == 'Up'
                and opponent[1] < self.height - 1
            ):
                opponent[1] += 1

            elif (
                move == 'Down'
                and opponent[1] > 0
            ):
                opponent[1] -= 1

            elif (
                move == 'Left'
                and opponent[0] > 0
            ):
                opponent[0] -= 1

            elif (
                move == 'Right'
                and opponent[0] < self.width - 1
            ):
                opponent[0] += 1

            # Collision
            if opponent == self.agent_pos:

                self.score -= 50
                self.collision = True

    # =========================================================
    # GAME OVER
    # =========================================================

    def is_done(self) -> bool:
        """
        Game ends when:

        1. All food has been collected
        2. Maximum number of steps reached
        3. Agent collides with opponent
        """

        return (
            len(self.food_positions) == 0
            or self.steps >= 60
            or self.collision
        )


# =============================================================
# GUI
# =============================================================

class GridGameGUI:

    def __init__(
        self,
        root,
        width=10,
        height=10,
        num_food=10,
        num_opponents=0,
        walls=None
    ):

        self.root = root

        self.root.title(
            "IT3012 - Practical 03 Search Agent"
        )

        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            custom_walls=walls
        )

        # -----------------------------------------------------
        # Canvas
        # -----------------------------------------------------

        max_canvas_dim = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_dim // width,
                max_canvas_dim // height
            )
        )

        canvas_w = width * self.cell_size
        canvas_h = height * self.cell_size

        self.canvas = tk.Canvas(
            root,
            width=canvas_w,
            height=canvas_h,
            bg="white"
        )

        self.canvas.pack()

        # -----------------------------------------------------
        # Label
        # -----------------------------------------------------

        self.label = tk.Label(
            root,
            text="Score: 0 | Steps: 0",
            font=("Arial", 14)
        )

        self.label.pack(pady=10)

        # -----------------------------------------------------
        # Button
        # -----------------------------------------------------

        self.btn = tk.Button(
            root,
            text="Start Random Simulation",
            command=self.run_loop,
            font=("Arial", 12)
        )

        self.btn.pack(pady=5)

        self.draw_grid()

    # =========================================================
    # DRAW GRID
    # =========================================================

    def draw_grid(self):

        self.canvas.delete("all")

        # -----------------------------------------------------
        # Draw grid cells
        # -----------------------------------------------------

        for x in range(self.env.width):

            for y in range(self.env.height):

                x1 = (
                    x * self.cell_size
                )

                y1 = (
                    self.env.height
                    - 1
                    - y
                ) * self.cell_size

                x2 = (
                    x1 + self.cell_size
                )

                y2 = (
                    y1 + self.cell_size
                )

                if (x, y) in self.env.walls:
                    color = "#64748b"
                else:
                    color = "#f1f5f9"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#cbd5e1"
                )

        # -----------------------------------------------------
        # Draw food
        # -----------------------------------------------------

        for fx, fy in self.env.food_positions:

            offset = (
                self.cell_size * 0.25
            )

            x1 = (
                fx * self.cell_size
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
                fill="#f59e0b"
            )

        # -----------------------------------------------------
        # Draw opponents
        # -----------------------------------------------------

        for ox, oy in self.env.opponents:

            offset = (
                self.cell_size * 0.2
            )

            x1 = (
                ox * self.cell_size
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
                fill="#990000"
            )

        # -----------------------------------------------------
        # Draw agent
        # -----------------------------------------------------

        ax, ay = self.env.agent_pos

        offset = (
            self.cell_size * 0.15
        )

        x1 = (
            ax * self.cell_size
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
            fill="#000066"
        )

    # =========================================================
    # RANDOM GUI SIMULATION
    # =========================================================

    def run_loop(self):

        self.btn.config(
            state="disabled"
        )

        def step():

            if not self.env.is_done():

                action = random.choice([
                    'Up',
                    'Down',
                    'Left',
                    'Right'
                ])

                self.env.execute_action(
                    action
                )

                self.draw_grid()

                self.label.config(
                    text=(
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

                self.label.config(
                    text=(
                        f"Game Over | "
                        f"Score: {self.env.score} | "
                        f"Steps: {self.env.steps}"
                    )
                )

                self.btn.config(
                    state="normal"
                )

        step()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=10,
        height=10,
        num_food=10,
        num_opponents=0
    )

    root.mainloop()