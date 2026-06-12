#To determine if a game square is beyond the board's boundaries or is occupied by a snake:
def is_obstacle(neighbour_x, neighbour_y, game_state, snake_index):

    head = game_state["board"]["snakes"][snake_index]["body"][0]
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    snakes = game_state["board"]["snakes"]

    if neighbour_x < 0 or neighbour_x >= board_width or neighbour_y < 0 or neighbour_y >= board_height:
        return True

    for i, snake in enumerate(snakes):
        if snake["health"] <= 0:
            continue
        body_to_check = snake["body"]
        if i == snake_index:
            body_to_check = snake["body"][:-1] 
        for segment in body_to_check:
            if neighbour_x == segment["x"] and neighbour_y == segment["y"]:
                return True
                
    return False


#To determine if a game square is beyond the board's boundaries or is occupied by a snake's body, excluding its head:
def is_obstacle_except_heads(neighbour_x, neighbour_y, game_state, snake_index):

    head = game_state["board"]["snakes"][snake_index]["body"][0]
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    snakes = game_state["board"]["snakes"]

    if neighbour_x < 0 or neighbour_x >= board_width or neighbour_y < 0 or neighbour_y >= board_height:
        return True

    for i, snake in enumerate(snakes):
        if snake["health"] <= 0:
            continue
        body_to_check = snake["body"][1:]
        if i == snake_index:
            body_to_check = snake["body"][1:-1] 
        for segment in body_to_check:
            if neighbour_x == segment["x"] and neighbour_y == segment["y"]:
                return True
                
    return False


