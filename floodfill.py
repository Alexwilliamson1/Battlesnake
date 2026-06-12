import heapq
from collections import deque
import collision

#This files contains functions that use the 'flood fill' or breadth-first search algorithm to calculate the locations of game board objects and the distances and areas between and around them. 

#To compute the locations of all food objects reachable from the coordinates of the given head:
def find_reachable_food(head, game_state, snake_index):
    board = game_state["board"]
    food_list = board["food"]

    rows, cols = game_state['board']['height'], game_state['board']['width']
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(head["x"], head["y"])])
    visited[head["y"]][head["x"]] = True

    while queue:
        x, y = queue.popleft()

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and not collision.is_obstacle(nx, ny, game_state, snake_index):
                    visited[ny][nx] = True
                    queue.append((nx, ny))
    reachable_food = []
    for food in food_list:
        if visited[food["y"]][food["x"]]:
            reachable_food.append(food)

    return reachable_food

#To compute the number of free squares connected to the square at (start_x, start_y):
def flood_fill(game_state, start_x, start_y, snake_index):
    rows, cols = game_state['board']['height'], game_state['board']['width']
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(start_x, start_y)])
    if not (0 <= start_x < cols and 0 <= start_y < rows):
        return 0
    
    visited[start_y][start_x] = True
    accessible_cells = 0

    while queue:
        x, y = queue.popleft()
        accessible_cells += 1

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and not collision.is_obstacle(nx, ny, game_state, snake_index):
                    visited[ny][nx] = True
                    queue.append((nx, ny))

    return accessible_cells

#The following function determines whether there is a path between a snake's head at square (start_x, start_y) and its tail.  Checking 'tail reachability' is useful for determining whether a move is towards an open or closed area.
def can_reach_tail(game_state, start_x, start_y, snake_index):
    snakes = game_state["board"]["snakes"]
    target_tail = snakes[snake_index]["body"][-1]
    rows, cols = game_state['board']['height'], game_state['board']['width']
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(start_x, start_y)])
    
    visited[start_y][start_x] = True
    
    while queue:
        x, y = queue.popleft()
        if x == target_tail["x"] and y == target_tail["y"]:
            return True

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx]:
                    if nx == target_tail["x"] and ny == target_tail["y"]:
                        return True

                    if not collision.is_obstacle(nx, ny, game_state, snake_index):
                        visited[ny][nx] = True
                        queue.append((nx, ny))
                    
    return False

#The following function calculates the Voronoi area for each snake.  Voronoi area is the number of game squares that a player can reach before any other player.  Squares that are an equal distance from two or more players are excluded from the calculation.
def compute_voronoi(game_state):
    board = game_state["board"]
    width = board["width"]
    height = board["height"]
    snakes = board["snakes"]

    territories = [0] * len(snakes)
    blocked = set()
    for snake in snakes:
        for seg in snake["body"]:
            blocked.add((seg["x"], seg["y"]))

    owner = [[-1 for _ in range(height)] for _ in range(width)]
    queue = deque()  
    
    for idx, snake in enumerate(snakes):
        if snake["health"] <= 0:
            continue
        hx = snake["body"][0]["x"]
        hy = snake["body"][0]["y"]

        if (hx, hy) in blocked:
            blocked.remove((hx, hy))

        owner[hx][hy] = idx
        queue.append((hx, hy, idx))

        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            x, y, s_idx = queue.popleft()

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue

                if (nx, ny) in blocked:
                    continue

                if owner[nx][ny] == -1:
                    owner[nx][ny] = s_idx
                    queue.append((nx, ny, s_idx))

                elif owner[nx][ny] != s_idx and owner[nx][ny] >= 0:
                    owner[nx][ny] = -2

        for x in range(width):
            for y in range(height):
                o = owner[x][y]
                if o >= 0:
                    territories[o] += 1

    return territories

#To compute the distance from the given square at (start_x, start_y) to the nearest food object:
def nearest_food_dist(game_state, start_x, start_y, snake_index):
    food_positions = {(f["x"], f["y"]) for f in game_state["board"]["food"]}
    if not food_positions:
        return None

    width = game_state["board"]["width"]
    height = game_state["board"]["height"]

    visited = [[False] * width for _ in range(height)]
    q = deque()
    q.append((start_x, start_y, 0)) 
    visited[start_y][start_x] = True

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while q:
        x, y, dist = q.popleft()

        if (x, y) in food_positions:
            return dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height:
                if not visited[ny][nx] and not collision.is_obstacle(nx, ny, game_state, snake_index):
                    visited[ny][nx] = True
                    q.append((nx, ny, dist + 1))

    return None

#To compute the coordinates of the snake's head that is closest in distance to the square at (start_x, start_y):
def nearest_head(game_state, start_x, start_y, snake_index):
    snakes = game_state["board"]["snakes"]
    heads = []
    for idx, snake in enumerate(snakes):
        if idx != snake_index:
            hx = snake["body"][0]["x"]
            hy = snake["body"][0]["y"]
            heads.append((hx, hy))

    width = game_state["board"]["width"]
    height = game_state["board"]["height"]

    visited = [[False] * width for _ in range(height)]
    q = deque()
    q.append((start_x, start_y, 0))
    visited[start_y][start_x] = True

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    while q:
        x, y, dist = q.popleft()

        if (x, y) in heads:
            return (x, y)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if not visited[ny][nx] and not collision.is_obstacle_except_heads(nx, ny, game_state, snake_index):
                    visited[ny][nx] = True
                    q.append((nx, ny, dist + 1))

    return None



