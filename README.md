# Chopsticks Minimax

Welcome to the **Chopsticks** game! This project implements a console-based version of the finger-counting children's game "Chopsticks." In this game, players take turns using their fingers to “attack” each other's hands, aiming to eliminate the opponent by strategically transferring finger counts.

## Table of Contents

-   [Overview](#overview)
-   [Gameplay Rules](#gameplay-rules)
-   [How to Run](#how-to-run)
-   [Algorithm](#algorithm)

## Overview

This Chopsticks game is a two-player game where each player (human or computer) attempts to knock out the opponent's hands by transferring finger counts strategically. The implementation features an AI using the Minimax algorithm to evaluate potential moves, making it challenging for human players.

## Gameplay Rules

-   **Initial Setup**: Each player starts with one finger raised on each hand.
-   **Turns**: Players take turns attacking the opponent.
    -   **Attacking**: Choose a hand to attack with and an opponent's hand to attack.
    -   **Damage**: When a hand attacks, its finger count is added to the attacked hand's fingers.
-   **Rollover**: This version of Chopsticks has a rollover, meaning when an attack results in more than five fingers, the resulting fingers is the fingers mod five.
-   **Winning**: The game ends when both hands of one player reach 0 fingers, making them "dead."
-   **Splitting**: This version of chopsticks doesn't include splitting, only attacks.

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/chopsticks-game.git
    cd chopsticks-game
    ```
1. Run the game file:
    ```bash
    python3 game.py
    ```

## Algorithm

The Minimax algorithm in this Chopsticks game implementation powers the AI player, enabling it to evaluate potential moves and choose the optimal one. Here’s a breakdown of how the algorithm works.

### Mapping out the tree

For each node in a generation, an array of its children, the next generation (g1), is generated. However, as this algorithm searches vertically, all the children of the next generation (g2) arent generated until the child of the first child (g1) is generated. This continues, with the first children of each generation mapping out the first branch of the tree.

### Leaves/Base Cases

-   **Win**: The game is won, meaning one of the players has lost both hands. If the player to max is the winner, the score fo the leaf is 1, and if the player to max is the loser, the score is -1.
-   **Tie**: The game is in a loop, meaning the current simulated position has been seen before in its specific branch. The score of the leaf is 0. If this was not in place, the tree would never finish as it would get stuck in a loop.

### Value assessment

In a minimax algorithm, after every leaf is found, values are assigned to nodes in ascending order. The algorithm alternates between the minimizing and maximizing player, with the maximizing player being the player who's turn it is. If the leaves of a node are (1, 0, and 0), and the player is maximizing, then 1 is the greatest number, and therefore the value of that node. For the leaves are (1, 0, -1, 1) with a minimizing player, -1 is assigned to the node as it is the smallest value. This continues up the tree until the original node has a score.

### Pruning

Without pruning, this task is too large for a laptop to reasonably compute. The main pruning method in this algorithm is remembering all previously calculated positions and their score using a dictionary, so that when a previously solved position is run into, it doesn't need to be recalculated. This also applies to all types reversals to a position, with appropriate modifications to the move and score.
