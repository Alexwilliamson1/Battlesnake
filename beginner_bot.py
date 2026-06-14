import random
from collections import deque

DIRECTIONS = ["up", "down", "left", "right"]

MOVE_DELTA = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0)
}

#To choose a move based on free board space, health, and the distance between this snake's head and a smaller opponent's head if that distance is only one square:
def beginner_bot(state, snake_index):
    board = state["board"]
    snakes = board["snakes"]
    you = snakes[snake_index]

    head = you["body"][0]
    neck = you["body"][1] if len(you["body"]) > 1 else None
    health = you["health"]

    width = board["width"]
    height = board["height"]

    food = board["food"]

    #To determine which directions this snake can move in so that it occupies a free board square:
    valid_moves = []

    for move in DIRECTIONS:
        dx, dy = MOVE_DELTA[move]
        new_head = {"x": head["x"] + dx, "y": head["y"] + dy}

        if not is_safe(new_head, board, snakes, neck, width, height):
            continue

        valid_moves.append((move, new_head))

    if not valid_moves:
        return random.choice(DIRECTIONS)

    #To score the moves in "valid_moves":
    scored_moves = []

    for move, new_head in valid_moves:
        score = 0

        #To score free space:
        space = flood_fill_space(new_head, board, snakes, width, height)
        score += space * 0.1

        #To score the distance to the nearest food object if this snake's health is less than 50: 
        if health < 50 and food:
            dist = min(manhattan(new_head, f) for f in food)
            score += 10 / (dist + 1)

        #To increase the score if the head of a smaller opponent is within one square of this snake's head:
        for other in snakes:
            if other is you or other["health"] <= 0:
                continue

            if len(other["body"]) < len(you["body"]):
                enemy_head = other["body"][0]
                if manhattan(new_head, enemy_head) == 1:
                    score += 5

        scored_moves.append((score, move))

    #To choose the move that corresponds to the highest score:
    scored_moves.sort(reverse=True)
    best_score = scored_moves[0][0]

    best_moves = [m for s, m in scored_moves if s == best_score]

    return random.choice(best_moves)

#To determine if the given coordinate location, "pos," is beyond the boundaries of the game board or coincides with the body of this or another snake:
def is_safe(pos, board, snakes, neck, width, height):
    x, y = pos["x"], pos["y"]

    if x < 0 or x >= width or y < 0 or y >= height:
        return False

    if neck and x == neck["x"] and y == neck["y"]:
        return False

    for snake in snakes:
        for segment in snake["body"]:
            if x == segment["x"] and y == segment["y"]:
                return False

    return True

#The following function calculates the "Manhattan" distance between board squares "a" and "b."  The shortest path between "a" and "b" that gaurantees a snake's survival may differ from the "Manhattan" distance, which excludes game objects such as snake bodies.
def manhattan(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

#To calculate the number of free squares connected to the square located at "start":
def flood_fill_space(start, board, snakes, width, height, max_depth=50):
    visited = set()
    queue = deque([start])
    count = 0

    occupied = set()
    for snake in snakes:
        for seg in snake["body"]:
            occupied.add((seg["x"], seg["y"]))

    while queue and count < max_depth:
        pos = queue.popleft()
        key = (pos["x"], pos["y"])

        if key in visited:
            continue
        visited.add(key)
        count += 1

        for dx, dy in MOVE_DELTA.values():
            nx, ny = pos["x"] + dx, pos["y"] + dy

            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in occupied and (nx, ny) not in visited:
                    queue.append({"x": nx, "y": ny})

    return count
