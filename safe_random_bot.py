import random

DIRECTIONS = ["up", "down", "left", "right"]

MOVE_DELTA = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0)
}

#The following function randomly chooses a move from a list of moves that lead to free board squares.  If every move either leads this snake off the game board or into an opponent's body, the function randomly chooses a move from "DIRECTIONS."
def safe_random_bot(state, snake_index):
    board = state["board"]
    snakes = board["snakes"]
    you = snakes[snake_index]

    head = you["body"][0]
    neck = you["body"][1] if len(you["body"]) > 1 else None

    width = board["width"]
    height = board["height"]

    occupied = set()
    for snake in snakes:
        for seg in snake["body"]:
            occupied.add((seg["x"], seg["y"]))

    #To create a list of moves that lead to free board squares:
    safe_moves = []

    for move in DIRECTIONS:
        dx, dy = MOVE_DELTA[move]
        nx, ny = head["x"] + dx, head["y"] + dy

        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            continue

        if neck and nx == neck["x"] and ny == neck["y"]:
            continue

        if (nx, ny) in occupied:
            continue

        safe_moves.append(move)

    #To randomly choose a move from "safe_moves":
    if safe_moves:
        return random.choice(safe_moves)

    #To choose a move randomly if every immediate board square is occupied:
    return random.choice(DIRECTIONS)
