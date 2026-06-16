import copy
import time
import evaluate
import collision
import floodfill

#The following function computes a "best move" based on the return values from "maxn."  The recursive depth of "maxn" is set by the value of "depth."
def find_best_move(game_state, snake_index, genome):
    best_move = None
    best_score = float("-inf")
    depth = 2

    for move in get_possible_moves(game_state, snake_index):
        new_state = simulate_move(game_state, snake_index, move)
        scores = max_n(new_state, depth - 1, next_snake(game_state, snake_index), genome)        
        if scores[snake_index] > best_score:
            best_score = scores[snake_index]
            best_move = move
    return best_move

#The following is a recursive function that assigns a number (score) to each player for each possible move that a player can make on a given turn.  The function returns the set of scores corresponding to the move that yields the highest score for the snake at the given index. 
def max_n(game_state, depth, snake_index, weights):
    board = game_state["board"]
    snakes = board["snakes"]
    head = snakes[snake_index]["body"][0]

    if depth == 0 or is_game_over(game_state):
        return evaluate.evaluate_board(game_state, weights)

    best_scores = [-float("inf")] * len(game_state["board"]["snakes"])

    for move in get_possible_moves(game_state, snake_index):
        new_state = simulate_move(game_state, snake_index, move)
        scores = max_n(new_state, depth - 1, next_snake(game_state, snake_index), weights)
            
        if scores[snake_index] > best_scores[snake_index]: 
            best_scores = scores

    return best_scores

#To compute the game state that results from the snake at the given index choosing the given move in the current game state:
def simulate_move(game_state, snake_index, move):
    new_state = copy.deepcopy(game_state)
    snake = new_state["board"]["snakes"][snake_index]
    head = snake["body"][0].copy()

    if move == "right":
        head["x"] += 1
    elif move == "left":
        head["x"] -= 1
    elif move == "up":
        head["y"] += 1
    elif move == "down":
        head["y"] -= 1
    else:
        raise ValueError(f"Unknown move: {move}")

    if collision.is_obstacle(head["x"], head["y"], new_state, snake_index):
        snake["health"] = 0
        return new_state

    ate_food = False
    for food in new_state["board"]["food"]:
        if food["x"] == head["x"] and food["y"] == head["y"]:
            ate_food = True
            new_state["board"]["food"].remove(food)
            snake["health"] = 100
            break

    new_body = [head] + snake["body"]

    if not ate_food:
        new_body.pop()
        snake["health"] -= 1

    snake["body"] = new_body
    snake["length"] = len(new_body)

    return new_state

#To compute a list of moves that the snake at "snake_index" can make such that it stays within the boundaries of the game board and occupies a free square:
def get_possible_moves(game_state, snake_index):
    head = game_state["board"]["snakes"][snake_index]["body"][0]
    moves = ["right", "left", "up", "down"]
    possible_moves = []
    for move in moves:
        if (move == "right"):
            if not collision.is_obstacle(head["x"] + 1, head["y"], game_state, snake_index):
                possible_moves.append(move)   
        elif (move == "left"):
            if not collision.is_obstacle(head["x"] - 1, head["y"], game_state, snake_index):
                possible_moves.append(move)  
        elif (move == "up"):
            if not collision.is_obstacle(head["x"], head["y"] + 1, game_state, snake_index):
                possible_moves.append(move)
        elif (move == "down"):
            if not collision.is_obstacle(head["x"], head["y"] - 1, game_state, snake_index):
                possible_moves.append(move)
    return possible_moves

#To increment the value of "snake_index":
def next_snake(game_state, snake_index):
    snakes = game_state["board"]["snakes"]
    return (snake_index + 1) % len(snakes)

#To determine when a game has ended:
def is_game_over(game_state):
    snakes = game_state["board"]["snakes"]
    alive_snakes = [s for s in snakes if s["health"] > 0]
    return len(alive_snakes) <= 1




