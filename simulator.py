from visual_grid_game import VisualGridHuntGame
from agent import ModelBasedAgent


def run_simulation():

    env = VisualGridHuntGame(
        width=10,
        height=10,
        num_food=5,
        num_opponents=0
    )

    agent = ModelBasedAgent()

    print("======================================")
    print(" IT3012 Practical 02")
    print(" Simple Reflex Agent")
    print("======================================")

    while not env.is_done():

        percept = env.get_percept()

        action = agent.sense_and_act(
            percept
        )

        print(
            f"Percept: {percept} "
            f"| Action: {action}"
        )

        env.execute_action(
            action
        )

    print()
    print("Game Over!")
    print(
        f"Final Score: {env.score}"
    )
    print(
        f"Steps: {env.steps}"
    )


if __name__ == "__main__":
    run_simulation()