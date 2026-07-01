# Battlesnake

## Description:

This repository contains two programs: a Minimax implementation for Battlesnake and a genetic algorithm for optimizing the heuristic function for the Minimax implementation.  The two programs can be used together, but they run independently. 

The Minimax algorithm:

This program implements the MaxN, or multiplayer, version of the Minimax algorithm, which recursively evaluates every possible move by each player up to a certain number of moves in the future.  The move returned by the algorithm is the one that is considered to produce the best outcome for a player, assuming all other players will also choose moves that produce the best outcome for themselves.  

The MaxN algorithm creates a tree of all possible game moves, starting from the current game state.  Each level of the tree represents a future turn and branches to all the possible moves by each player for that turn.  Since multiple players move simultaneously each turn, the size of the tree grows exponentially and therefore the recursive depth that the algorithm can reach in the 500 ms Battlesnake turn time limit is much less than the number of turns in a competitive game.  For this program, the recursive depth is set to 3, but that number can be adjusted if hardware or other factors allow.

Once the recursive depth of the algorithm is reached, a heuristic function is called for each leaf node and subsequent node up the tree. This function quantifies the game state for each snake by calculating its distance to food objects and opponents, its Voronoi area, etc.  The results of these calculations are returned as a list of numbers or ‘scores,’  By choosing the moves or nodes that yield the highest ‘score’ for each player at every level of the tree, one can find the optimal move for a player for the current turn.  

The genetic algorithm:

A set of weights for the heuristic function in the MaxN algorithm have been chosen and defined in `main.py`.  Together these weights comprise a “genome” or unique scoring strategy for a Battlesnake, independent of the MaxN tree search.  To further optimize this strategy, a genetic algorithm can be used to find a new set of weights based on the results of game simulations.  

The game simulations are between 4 players: two players have “evolving” genomes and two players are pre-programmed ‘bots.’  The algorithm begins with a population of Battlesnakes with randomly initialized genomes.  For each generation, a series of games are simulated so that every member of the population competes against every other member.  The Battlesnakes with the best performing genomes are used to create the next population through a process of parent selection and genome mutation.  Statistics about each population are logged and the algorithm runs for the specified number of generations with the goal of finding optimal weights for a single genome.  

## Requirements:

To run the Battlesnake program, one requires: Python 3 or higher; Flask; “pip” for installing Python packages; an internet connection; and a public URL provider, such as ngrok.  To install Flask, run the command `pip install -r requirements.txt`.

To run the genetic algorithm, one requires Python 3 or higher.

## To run the Battlesnake program:

First, type “play.battlesnake.com” in a browser and click on the link to the “My Battlesnakes” page.  See the notes below for creating a Battlesnake.  If using ngrok to deploy your server, open a command-line interface, navigate to the directory containing the Battlesnake program’s source files, and run the command `ngrok http 8000`.

Open a second command-line interface, navigate to the directory containing the Battlesnake program’s source files, and run the command `python3 main.py`.  On the “My Battlesnakes” page displayed in your browser, click on the Battlesnake you created for this program, confirm that play.battlesnake.com is connected to the program’s server by clicking the “PING” button, then create a game.

## To run the genetic algorithm:

Open a command-line interface, navigate to the directory containing `genetic_algorithm.py`, and run the command `python3 genetic_algorithm.py`.  

## Notes:

The Battlesnake program is intended to be used for playing games on play.battlesnake.com.  Therefore, some setup is required.  First, create a user account on play.battlesnake.com.  Next, create a Battlesnake with a name and server URL.   A server URL is required for sending and receiving data to and from play.battlesnake.com during games.  One can obtain one in a variety of ways, the most common of which is by using a platform that provides application hosting or deployment services.  Some platforms that provide these services for free are: ngrok, Fly.io, Railway, Render, AWS, Google Cloud, and Microsoft Azure.  

The server URL used for testing the Battlesnake program was provided by ngrok.  To use ngrok, create a user account, open a command-line interface, and run the command `ngrok http` followed by the port on which your Battlesnake server runs.  The port in `server.py` is currently set to 8000, so the full command is `ngrok http 8000`.  A new window will open displaying information.  Beside the word “forwarding” will be a URL beginning with “https.”  Use this URL to create a Battlesnake.

This program was tested on macOS 15.7 using Clang. 
