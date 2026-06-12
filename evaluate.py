import random
import floodfill
import collision
import maxn

#A heuristic function that calculates a "score" for each snake player, given the state of the game board:
def evaluate_board(game_state, weights):
    board = game_state["board"]
    board_width = board["width"]
    board_height = board["height"]
    board_area = board_width * board_height 
    snakes = board["snakes"]
    scores = []
 
#To score Voronoi area:
    directions = {
        "right": (1, 0),
        "left": (-1, 0),
        "up": (0, 1),
        "down": (0, -1)
    }

    territories = floodfill.compute_voronoi(game_state)

    for snake_index, snake in enumerate(snakes):
        if snake["health"] <= 0:
            scores.append(float("-inf"))
            continue
        score = 0
        head = snake["body"][0]
        territory_score = 0
        voronoi_norm = territories[snake_index] / board_area
        if game_state["turn"] > 0:
            territory_score = weights["territory"] * voronoi_norm             

#To score accessible area:
        raw_area = floodfill.flood_fill(game_state, head["x"], head["y"], snake_index)
        area_score = weights["accessible_area"] * raw_area
              
#To score the largest future accessible area:
        best_future_area = 0
        for move_name, (dx, dy) in directions.items(): 
            nx = head["x"] + dx
            ny = head["y"] + dy
            if collision.is_obstacle(nx, ny, game_state, snake_index):
                continue

            sim_state = maxn.simulate_move(game_state, snake_index, move_name)
            future_area = floodfill.flood_fill(sim_state, nx, ny, snake_index)
            best_future_area = max(best_future_area, future_area)

        future_area_score = weights["max_future_area"] * (best_future_area - snake["length"])

#To score snake body length:
        hunger_factor_length = 0
        num_opponents = 0
        diff_score = 0
        length_score = 0
        for i_index, opp in enumerate(snakes):
            if i_index == snake_index:
                continue
            else:
                diff = snake["length"] - opp["length"]
                diff_score += diff * weights["length"]
                num_opponents += 1
        if num_opponents > 0:
            length_score = diff_score / num_opponents
        else:
            length_score = diff_score
            
#To score the distance to the nearest food object:
        food_score = 0
        closest_food = floodfill.nearest_food_dist(game_state, head["x"], head["y"], snake_index)

        if closest_food is not None:
            hunger_factor = weights["hunger_factor"]
            if hunger_factor < 1:
                hunger_factor = max(0.3, (100 - snake["health"]) / 100)
            food_weight = (hunger_factor + hunger_factor_length) / 2
            multiple = weights["closest_food"]
            food_score = hunger_factor * (weights["if_reachable_food"] - (multiple * closest_food))
                                
        else:
            food_score = weights["if_no_reachable_food"]
            #score -= (100 - snake["health"])    
        
#To score the distance to the head of a shorter snake:
        nearby_opp_score = 0
        shorter_heads = [(opp["body"][0]["x"], opp["body"][0]["y"]) for opp in snakes if opp["length"] < snake["length"]]
        nearest_head = floodfill.nearest_head(game_state, head["x"], head["y"], snake_index)
        if nearest_head is not None:
            hx, hy = nearest_head
            dist = abs(head["x"] - hx) + abs(head["y"] - hy)
            if (hx, hy) in shorter_heads:
                if dist <= 2:
                    nearby_opp_score = weights["smaller_opponent_dist1"]
                
                elif dist <= 4:
                    nearby_opp_score = weights["smaller_opponent_dist2"]

                else:
                    nearby_opp_score = max(0, weights["smaller_opponent_dist3"] - 3 * dist)
        
            else:
                if dist <= 2:
                    nearby_opp_score = weights["larger_opponent_dist1"]


                elif dist <= 4:
                    nearby_opp_score = weights["larger_opponent_dist2"]

#To score "tail reachability" according to the game turn, accessible area, and health:
        tail_score = 0
        turn_factor = min(1.0, game_state["turn"] / 100)
        area_factor = min(1.0, snake["length"] / max(1, raw_area))
        health_factor = max(0.3, (100 - snake["health"]) / 100)
        tail_weight = (turn_factor + area_factor + health_factor) / 3

        if snake["length"] > 3:
            if floodfill.can_reach_tail(game_state, head["x"], head["y"], snake_index):
                tail_score = weights["reachable_tail"] * tail_weight
                                                    
            else:
                if area_score < snake["length"]:
                    tail_score = weights["unreachable_tail1"] * tail_weight

                else:
                    tail_score = weights["unreachable_tail2"] * tail_weight
        
#To generate a random number between -var_range and var_range to be added to the score:
        var_range = weights["random_variability"]
        variability = random.uniform(-var_range, var_range) * max(0.2, 1 - game_state["turn"] / 100)
        var_score = variability  

#To score victory:
        victory_score = 0
        if len(snakes) == 1:
            victory_score = weights["victory"]

#A dictionary for the score:
        move_factors = { 
                   "territory": territory_score,
                   "accessible_area": area_score,
                    "max_future_area": future_area_score,
                    "length": length_score,
                    "food": food_score,
                    "nearby_opponent": nearby_opp_score,
                    "tail_reachability": tail_score,
                    "random_variability": var_score,
                    "victory": victory_score,
        }

        score = (
            move_factors["territory"] +
            move_factors["accessible_area"] +
            move_factors["max_future_area"] +
            move_factors["length"] +
            move_factors["food"] +
            move_factors["nearby_opponent"] +
            move_factors["tail_reachability"] +
            move_factors["random_variability"] +
            move_factors["victory"]
        )

        scores.append(score)
        #Uncomment the following to output the individual scores calculated for one's snake each turn:
        #if snake["id"] == game_state["you"]["id"]:
            #for key, value in move_factors.items():
                #print(key, value)
    
    return scores
