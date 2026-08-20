from visual_grid_game import VisualGridHuntGame
from agent import SearchAgent


def run_search_simulation():

    env = VisualGridHuntGame(
        width=10,
        height=10,
        num_food=5,
        num_opponents=0
    )

    agent = SearchAgent()

    # =========================================================
    # CHANGE THIS TO:
    #
    # 'BFS'
    # 'DFS'
    # 'UCS'
    # =========================================================

    agent.active_algo = 'DFS'

    print(
        "======================================"
    )

    print(
        " IT3012 Practical 03"
    )

    print(
        f" Search Algorithm: "
        f"{agent.active_algo}"
    )

    print(
        "======================================"
    )

    while not env.is_done():

        percept = env.get_percept()

        action = agent.sense_and_act(
            percept
        )

        print(
            f"Position: {env.agent_pos} "
            f"| Food: {percept['all_food']} "
            f"| Action: {action} "
            f"| Score: {env.score}"
        )

        env.execute_action(
            action
        )

    print()

    print(
        "========== GAME OVER =========="
    )

    print(
        f"Final Score: {env.score}"
    )

    print(
        f"Steps: {env.steps}"
    )


if __name__ == '__main__':
    run_search_simulation()