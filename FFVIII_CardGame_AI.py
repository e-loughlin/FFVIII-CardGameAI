"""
 ___ _           _   ___         _                 __   _____ ___ ___ 
 | __(_)_ _  __ _| | | __|_ _ _ _| |_ __ _ ____  _  \ \ / /_ _|_ _|_ _|
 | _|| | ' \/ _` | | | _/ _` | ' \  _/ _` (_-< || |  \ v / | | | | | | 
 |_| |_|_||_\__,_|_| |_|\__,_|_||_\__\__,_/__/\_, |   \_/ |___|___|___|
   ___             _    ___                   |__/ ___                 
  / __|__ _ _ _ __| |  / __|__ _ _ __  ___    /_\ |_ _|                
 | (__/ _` | '_/ _` | | (_ / _` | '  \/ -_)  / _ \ | |                 
  \___\__,_|_| \__,_|  \___\__,_|_|_|_\___| /_/ \_\___|                
                                                              
title: final fantasy viii card game ai
author: evan loughlin
date: june 20, 2021

this program provides recommendations for the "best move", given a particular game state.
a simple minimax algorithm is implemented for this purpose.
the starting game state can be input in gamestate.yaml, specifying each of the 10 cards
in the game, their owner, their position (either "hand" or 1-9), and the card strength values.

refer to readme.md for detailed instructions.
"""

import argparse
import copy
import math
import os
from datetime import datetime
from enum import Enum

import yaml

# Constants
PLAYER = "p"
OPPONENT = "o"


# Define Card class
class Card:
    def __init__(self, symbol, owner, top, left, right, bottom):
        self.symbol = symbol
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.owner = owner

    def get_total_power(self):
        return self.top + self.left + self.bottom + self.right

    def __str__(self):
        output = "  {}-{}  \n".format(self.symbol, self.owner)
        output += " | {} | \n".format(self.top)
        output += " |{} {}| \n".format(self.left, self.right)
        output += " | {} | \n".format(self.bottom)
        return output


# Define GameState class
class GameState:
    def __init__(self):
        self.board = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
        }
        self.players = {PLAYER: Player(name=PLAYER), OPPONENT: Player(name=OPPONENT)}
        self.current_player = None
        self.points = {PLAYER: 0, OPPONENT: 0}
        self.previous_gamestate = None

    def get_winner(self):
        return PLAYER if self.points[PLAYER] > self.points[OPPONENT] else OPPONENT

    def game_over(self):
        return len(self.get_available_positions()) == 0

    def get_opposite_player(self):
        return OPPONENT if self.current_player == PLAYER else PLAYER

    def make_move(self, card_symbol, position, debug_file=None):
        card = self.players[self.current_player].hand[card_symbol]
        del self.players[self.current_player].hand[card_symbol]
        self.board[position] = card
        self.points[self.current_player] += 1

        other_player = self.get_opposite_player()
        neighbour_cards = self.get_neighbours(position)

        def check_neighbour(neighbour, direction):
            if neighbour != None and neighbour.owner == other_player:
                if getattr(card, direction) > getattr(neighbour, opposite[direction]):
                    neighbour.owner = self.current_player
                    self.points[self.current_player] += 1
                    self.points[other_player] -= 1

        opposite = {"top": "bottom", "left": "right", "right": "left", "bottom": "top"}
        for direction in opposite:
            check_neighbour(neighbour_cards[direction], direction)

        if debug_file:
            debug_file.write(str(self) + "\n")

        self.current_player = other_player

    def next_possible_moves(self):
        next_moves = []
        available_cards = list(self.players[self.current_player].hand.keys())
        available_positions = self.get_available_positions()
        for position in available_positions:
            for card in available_cards:
                next_moves.append((card, position))
        return next_moves

    def get_available_positions(self):
        return [pos for pos, card in self.board.items() if card is None]

    def get_neighbours(self, position):
        neighbours = {"left": None, "top": None, "right": None, "bottom": None}
        if position == 7:
            neighbours["bottom"] = self.board[4]
            neighbours["right"] = self.board[8]
        elif position == 8:
            neighbours["left"] = self.board[7]
            neighbours["bottom"] = self.board[5]
            neighbours["right"] = self.board[9]
        elif position == 9:
            neighbours["left"] = self.board[8]
            neighbours["bottom"] = self.board[6]
        elif position == 4:
            neighbours["right"] = self.board[5]
            neighbours["top"] = self.board[7]
            neighbours["bottom"] = self.board[1]
        elif position == 5:
            neighbours["right"] = self.board[6]
            neighbours["left"] = self.board[4]
            neighbours["top"] = self.board[8]
            neighbours["bottom"] = self.board[2]
        elif position == 6:
            neighbours["left"] = self.board[5]
            neighbours["top"] = self.board[9]
            neighbours["bottom"] = self.board[3]
        elif position == 1:
            neighbours["right"] = self.board[2]
            neighbours["top"] = self.board[4]
        elif position == 2:
            neighbours["right"] = self.board[3]
            neighbours["left"] = self.board[1]
            neighbours["top"] = self.board[5]
        elif position == 3:
            neighbours["top"] = self.board[6]
            neighbours["left"] = self.board[2]
        return neighbours

    def __str__(self):
        board_output = "-------------------------------------------\ncurrent player: {}  |  points: p = {}, o = {}\n".format(
            self.current_player, self.points[PLAYER], self.points[OPPONENT]
        )
        board_output += (
            display_cards_horizontally([self.board[7], self.board[8], self.board[9]])
            + "\n"
        )
        board_output += (
            display_cards_horizontally([self.board[4], self.board[5], self.board[6]])
            + "\n"
        )
        board_output += (
            display_cards_horizontally([self.board[1], self.board[2], self.board[3]])
            + "\n"
        )
        player_cards_output = display_cards_horizontally(
            self.players[PLAYER].hand.values()
        )
        opp_cards_output = display_cards_horizontally(
            self.players[OPPONENT].hand.values()
        )
        return "player (p) cards:\n{}\n\nopponent (o) cards:\n{}\n\nboard:\n{}".format(
            player_cards_output, opp_cards_output, board_output
        )


# Function to evaluate the game state
def evaluate_game_state(gamestate, player):
    other_player = gamestate.get_opposite_player()
    score = gamestate.points[player] - gamestate.points[other_player]

    # Positional advantage
    position_score = 0
    position_factor = 0.1

    corners = [1, 3, 7, 9]
    for corner in corners:
        if gamestate.board[corner] and gamestate.board[corner].owner == player:
            position_score += 1 / 9  # prioritize corners

    edges = [2, 4, 6, 8]
    for edge in edges:
        if gamestate.board[edge] and gamestate.board[edge].owner == player:
            position_score += 1 / 9 / 2  # prioritize edges

    score += position_score * position_factor

    # Remaining card score in hand advantage
    card_hand_advantage_score = 0
    card_hand_advantage_factor = 0.1

    for card in gamestate.players[player].hand.values():
        card_hand_advantage_score += card.get_total_power() / 40 / 9

    score += card_hand_advantage_score * card_hand_advantage_factor

    return score


# Minimax algorithm
def minimax(gamestate, ismaxturn, depth, max_depth, player):
    other_player = gamestate.get_opposite_player()
    if gamestate.game_over() or depth == max_depth:
        return gamestate.points[player] - gamestate.points[other_player]

    scores = []
    for move in gamestate.next_possible_moves():
        new_gamestate = copy.deepcopy(gamestate)
        card_symbol, position = move
        new_gamestate.make_move(card_symbol, position)

        score = minimax(new_gamestate, not ismaxturn, depth + 1, max_depth, player)
        scores.append(score)

    return max(scores) if ismaxturn else min(scores)


# Find the best move
def best_move(gamestate, max_depth=3, debug_file=None):
    bestscore = -math.inf
    bestmove = None

    for move in gamestate.next_possible_moves():
        card_symbol, position = move
        new_gamestate = copy.deepcopy(gamestate)
        new_gamestate.make_move(card_symbol, position)

        score = minimax(new_gamestate, True, 1, max_depth, gamestate.current_player)
        if debug_file:
            debug_file.write(f"Evaluating move {move}: score = {score}\n")
        if score > bestscore:
            bestscore = score
            bestmove = move

    if debug_file:
        debug_file.write(f"Best move: {bestmove} with score = {bestscore}\n")
    return bestmove


# Display cards horizontally
def display_cards_horizontally(cards):
    line1, line2, line3, line4 = "", "", "", ""
    for card in cards:
        if card is None:
            line1 += "       "
            line2 += " |   | "
            line3 += " |   | "
            line4 += " |   | "
        else:
            line1 += "  {}-{}  ".format(card.symbol, card.owner)
            line2 += " | {} | ".format(card.top)
            line3 += " |{} {}| ".format(card.left, card.right)
            line4 += " | {} | ".format(card.bottom)
    return "{}\n{}\n{}\n{}".format(line1, line2, line3, line4)


# Define Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = {}

    def __str__(self):
        return "{}:{}".format(self.name, list(self.hand.keys()))

    def hand_value(self):
        return sum([card.get_total_power() for card in self.hand.values()])


# Load game state from a YAML file
def gamestate_from_file(filename):
    with open(filename) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    gamestate = GameState()

    gamestate.points[PLAYER] = data["points"]["p"]
    gamestate.points[OPPONENT] = data["points"]["o"]
    gamestate.current_player = data["current_player"]

    def parse_card(card_data):
        symbol = card_data["symbol"]
        top = int(card_data["top"])
        left = int(card_data["left"])
        right = int(card_data["right"])
        bottom = int(card_data["bottom"])
        owner = card_data["owner"]
        return Card(symbol, owner, top, left, right, bottom)

    for card_data in data["cards"]:
        card = parse_card(card_data)
        position = card_data["position"]

        if position == "Hand":
            gamestate.players[card.owner].hand[card.symbol] = card
        else:
            gamestate.board[int(position)] = card

    return gamestate


# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Triple Triad AI")
    parser.add_argument(
        "--gamestate", required=True, help="YAML file containing the game state"
    )
    parser.add_argument(
        "--depth", type=int, default=3, help="Maximum depth for the minimax algorithm"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


# Main function
def main():
    args = parse_arguments()
    gamestate = gamestate_from_file(args.gamestate)

    debug_file = None
    if args.debug:
        debug_filename = f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        debug_file = open(debug_filename, "w")
        debug_file.write("Initial game state:\n")
        debug_file.write(str(gamestate) + "\n")

    best_move_choice = best_move(gamestate, args.depth, debug_file)
    if best_move_choice:
        card, position = best_move_choice
        gamestate.make_move(card, position, debug_file)
        winner = gamestate.get_winner()

        print(f"Best move: {card} at position {position}")
        print(f"Winner: {winner}")

        if debug_file:
            debug_file.write(f"Final game state:\n{gamestate}\n")
            debug_file.write(f"Winner: {winner}\n")
            debug_file.close()


if __name__ == "__main__":
    main()
