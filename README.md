# Risky-AI

*Credit to github.com user [ncsereoka](#https://github.com/ncsereoka) - most of the framework for this package was cribbed directly from his repo [risky-game](#https://github.com/ncsereoka/risky-game)*

*Risk® is a registered trademark of Hasbro, Inc. This code base is intended for educational or research purposes only. All rights and privileges belong to their respective owners.*

## Overview

This package serves as a framework for automating games of the board game Risk as a means to develop algorithmic and AI agents for research in the fields of Machine Learning, Deep Learning, Neural Networking, and general AI development.

### Unimplemented Features
This implementation is currently missing the following features:
- Cards
    - Under published rules, cards are awarded when players capture territories, and can be traded in for units at the start of their turn. This mechanic is not currently implemented.
- Fortify
    - Under published rules, a player may optionally move all but one unit from any territory they own into another *adjacent* territory they own. This mechanic is not currently implemented.

## Structure
The game is divided into a series of Class objects. Their hierarchy is described as follows:
- Game
    - State
        - Player(s)
            - Agent
        - Board
            - Continents
                - Territories
            - Borders
        - Deck (*not yet implemented*)

### Game
Contains methods for rolling dice, resolving attack rounds, determining a winner, and turn order. 

### State
Stores the current state of the game in progress, including the Board itself and the Players playing the game. Contains methods to update heuristics related to the board state as a whole, generate a random board state, and generate lists of territories
(among other things)

### Player
Stores attributes related to the individuals or agent playing the game, and includes methods required to play a game. These methods include adding units to a Player's unit pool, allocating units to defend a territory, and the pattern of play used when attacking a territory (among others).

### Agent
The algorithm a Player users to play a game. This implementation currenly includes a Human agent and a Random agent*.

\* The Random Agent makes random legal decisions for every possible decision point with one exception - whether or not to attack. Under the published game rules, a player must decide whether or not to attack at the beginning of the turn and at the end of every combat round. In practice, setting this value to random results in non-terminating games when playing against other random agents as the density of attacks (that is to say the number of attacks that occur per turn) is too low to properly advance the game state toward conclusion. Instead, the unit counts tended to rise out of control (in at least one observed case, toward the ***thousands***).

### Board
The board itself. Contains Territories, Continents (groups of Territories), and Borders (connections between Territories). Also contains methods to generate a Board from a database, and to identify which player owns which Territories / Continents.

## Getting Started
The file risk/main.py serves as the entry point for the rest of the framework. Currently, this implementation assumes the use of a database backend (SQL Server in this case). The files in the SQL folder can be used to create a database to support this project. Additionally, the file ./sql/scripts/db_create.sql can be used to create the database and insert the default board all at once. Additionally, the files ./sql/schemas/sim.sql, ./sql/tables/sim/sim_games.sql, and ./sql/tables/sim/sim_rounds.sql can be used to create a schema to store simulated combats (see the ./model directory for more information).

## Model
Previous work on creating an AI to play Risk depends largely on predicting the probability that an attack against a particular territory will be successful. Statisticians generally use Markov Chains to determine nested probabilities (i.e. probability that D will occur given A, B, and C occurring in that order). While Markov Chains are very precise, they are A) computationally expensive, and B) not something I know how to implement. 

The Model folder contains the file sim.py, which can be used to simulate attacks in which the Attacker keeps up the attack until either they are no longer allowed to do so or until all of the defender's units are destroyed. 

The Model folder also includes a Jupyter notebook and two .json files. The .json files describe an XGBoost model and tuned hyperparameters generated from a series of simulations as described above - each combination of 1-30 Attackers and 1-30 Defenders was simulated 10,000 times each to generate a total of 9,000,000 simulated attacks. These attacks were fed into an XGBoost Classifier. This classifier then underwent hyperparameter tuning as described in the Jupyter file to produce the final model.

While not quite as accurate as the Markov Chain approach, this approach generates very close approximations of probability, and scales up well.

## Planned Work (ToDo)
- Add the Card mechanic 
- Add the Fortify mechanic
- Expose the board state to an Agent
    - Currently, the board state is passed to the agent during specific function calls. This method makes the evaluation of board position and the planning of future moves inefficient, as separate function calls (and thus separate evaluations) would need to be made to first decide whether the agent want to attack or not and then to decide where and how to attack. 
    - By exposing the game state to the Agent directly, the Agent should be able to plan and then perform it's turn without creating multiple function calls
- Add functionality to Agent to determine where to place units during the Setup phase