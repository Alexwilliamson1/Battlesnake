# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#

import random
import typing
from maxn import *

#Information for creating a Battlesnake, including one's username and customizable snake features:
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Alex",
        "color": "#FF7F0F", 
        "head": "shades",
        "tail": "mlh-gene",  
    }

#To start a game: 
def start(game_state: typing.Dict):
    print("A game has started.")

#To end a game:
def end(game_state: typing.Dict):
    print("A game has ended.\n")

#To compute and return a move each turn:
def move(game_state: typing.Dict) -> typing.Dict:
    snakes = game_state["board"]["snakes"]
    my_snake_id = game_state["you"]["id"]
    my_snake_index = 0
    genome = { 
       "territory": 25.0,
       "accessible_area": 0.21,
       "max_future_area": 0.45,
       "length": 5,
       "if_reachable_food": 280,
       "closest_food": 6,
       "hunger_factor": -1,
       "if_no_reachable_food": -100,
       "smaller_opponent_dist1": 220,
       "smaller_opponent_dist2": 160,
       "smaller_opponent_dist3": 140,
       "larger_opponent_dist1": -170,
       "larger_opponent_dist2": -70,
       "reachable_tail": 136,
       "unreachable_tail1": -120,
       "unreachable_tail2": -90,
       "random_variability": 0,
       "victory": 1000000,
    }

    for i, snake in enumerate(snakes):
        if snake["id"] == my_snake_id:
            my_snake_index = i

    next_move = find_best_move(game_state, my_snake_index, genome)
    return {"move": next_move}
    
#Calling "run_server":
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})

