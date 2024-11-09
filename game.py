import copy
from player import Player
from chopsticks_logger import logger
import time
import json

solved_counter = 0

class Game():
    def __init__(self, player1_type, player2_type, l1=1, r1=1, l2=1, r2=1, turn='Player 1'):
        self.player1 = Player(player1_type, l1, r1)
        self.player2 = Player(player2_type, l2, r2)
        self.turn = turn
        self.score = None
        if not self.player1.is_alive and not self.player2.is_alive:
            raise ValueError("Cannot initialize game with both players dead, c'mon man")
        if not self.player1.is_alive:
            self.winner = 'Player 2'
        elif not self.player2.is_alive:
            self.winner = 'Player 1'
        else:
            self.winner = None
        self.positions = [self.key()]
        self.solved_positions = {"Player 1": {}, "Player 2": {}}

    def make_position(self):
        return f"{self.player1.left_hand.fingers}{self.player1.right_hand.fingers}{self.player2.left_hand.fingers}{self.player2.right_hand.fingers}"
    
    def print(self):
        print(self.make_position())
    
    def print_status(self):
        print(f"Player 1: Left hand: {self.player1.left_hand.fingers} | Right hand: {self.player1.right_hand.fingers}")
        print(f"Player 2: Left hand: {self.player2.left_hand.fingers} | Right hand: {self.player2.right_hand.fingers}")
        print(f"Turn: {self.turn}")
        if self.winner is not None:
            print(f"Winner: {self.winner}")
    
    def move(self, action_type, attacking_hand_str, attacked_hand_str, simulate=False):
        if action_type != 'attack':
            raise ValueError('Undefined attack type')

        self.attack(self.attacking_player(), self.attacked_player(), attacking_hand_str, attacked_hand_str, simulate)
        
        if not self.player1.is_alive:
            self.winner = 'Player 2'
            if not simulate:
                print('Player 2 wins!')
        elif not self.player2.is_alive:
            self.winner = 'Player 1'
            if not simulate:
                print('Player 1 wins!')
        elif self.player1.is_alive and self.player2.is_alive:
            self.winner = None
        else:
            raise ValueError("Invalid is_alive for some player.")
        
        if self.key() in self.positions:
            self.winner = 'Tie'
            if not simulate:
                print('Game Ties!')
                
        self.positions.append(self.key())
        

    def attack(self, attacking_player, attacked_player, attacking_hand_str, attacked_hand_str, simulate=False):
        
        if attacking_hand_str == 'r':
            attacking_hand = attacking_player.right_hand
        elif attacking_hand_str == 'l':
            attacking_hand = attacking_player.left_hand
        else:
            raise ValueError('Invalid attacking hand input')
        
        if attacked_hand_str == 'r':
            attacked_hand = attacked_player.right_hand
        elif attacked_hand_str == 'l':
            attacked_hand = attacked_player.left_hand
        else:
            raise ValueError('Invalid attacking hand input')

        if not attacking_hand.is_alive or not attacked_hand.is_alive:
            raise ValueError('Attacking dead hand or with dead hand')
        
        attacked_player.receive_attack(attacking_hand.fingers, attacked_hand_str)
        
        if not simulate:
            print(f"{self.turn} is attacking with {attacking_hand_str.upper()} hand ({attacking_hand.fingers} fingers) "
                  f"against {('Player 2' if self.turn == 'Player 1' else 'Player 1')}'s {attacked_hand_str.upper()} hand.")
        

    def get_alive_hands(self):
        alive_attacking_hands = []
        if self.attacking_player().left_hand.is_alive:
            alive_attacking_hands.append('l')
        if self.attacking_player().right_hand.is_alive:
            alive_attacking_hands.append('r')

        alive_attacked_hands = []
        if self.attacked_player().left_hand.is_alive:
            alive_attacked_hands.append('l')
        if self.attacked_player().right_hand.is_alive:
            alive_attacked_hands.append('r')
            
        return alive_attacking_hands, alive_attacked_hands
    
    def create_next_generation(self):
        next_generation_positions = []
        alive_attacking_hands, alive_attacked_hands = self.get_alive_hands()
            
        for attacking_hand_str in alive_attacking_hands:
            for attacked_hand_str in alive_attacked_hands:
                try:
                    game_copy = copy.deepcopy(self)
                    game_copy.move('attack', attacking_hand_str, attacked_hand_str, simulate=True)
                    next_generation_positions.append((game_copy.make_position(), ('attack', attacking_hand_str, attacked_hand_str)))
                except ValueError as e:
                    print(e)
        return next_generation_positions
    
    def attacking_player(self):
        if self.turn == 'Player 1':
            return self.player1
        else:
            return self.player2
        
    def attacked_player(self):
        if self.turn == 'Player 1':
            return self.player2
        else:
            return self.player1
    
    def start(self):
        while(True):
            self.play_turn()
            self.print_status()
            if self.winner is not None:
                print(f'{self.winner} wins')
                break
            
    def play_turn(self):
        if self.attacking_player().is_human:
            self.play_human_turn()
        else:
            self.play_computer_turn()
        self.turn = 'Player 1' if self.turn == 'Player 2' else 'Player 2'
        self.solved_positions = {"Player 1": {}, "Player 2": {}}
        self.positions.append(self.key())

    
    def play_human_turn(self):
        while True:
            attacking_hand_str = input(f'{self.turn}, attack with your left or right hand? (l/r)')
            attacked_hand_str = input(f'{self.turn}, attack other players left or right hand? (l/r)')
            try:
                self.move('attack', attacking_hand_str, attacked_hand_str)
                break
            except ValueError as e:
                print(e)
                
    def play_computer_turn(self):
        print(f"Computer Playing... Turn: {self.turn}")

        score, best_move, minimax_tree = Game.minimax(self, self, self.turn)
        print(f"Predicted outcome from perspective of {self.turn}: {score}")
        print(f"Best move to get to that score: {best_move}")

    
        try:
            if best_move:
                action_type, attacking_hand_str, attacked_hand_str = best_move
                self.move(action_type, attacking_hand_str, attacked_hand_str)
                print(f"Computer chose to {action_type} with {attacking_hand_str} attacking {attacked_hand_str}")
            else:
                print("No valid move found")
                
        except ValueError as e:
            print(e)
    
       

    def key(self):
        return (self.make_position(), self.turn)
  
    
    @staticmethod        
    def minimax(init_game, game, player_to_max, depth=0, visited_positions=None, is_maximizing=True):
        global solved_counter
        if visited_positions is None:
            visited_positions = game.positions
        
      
        if game.winner is not None:            
            if player_to_max == game.winner:
                return 1, None, {'pos': game.key(), 'score': 1, 'type': 'leaf'}
            elif game.winner == 'Tie':
                return 0, None, {'pos': game.key(), 'score': 0, 'type': 'leaf'}
            else:
                return -1, None, {'pos': game.key(), 'score': -1, 'type': 'leaf'}
        
        best_score = -2 if is_maximizing else 2
        best_move = None
        
        next_gen = game.create_next_generation()
        tree = {'pos': game.key(), 'children': []}    
        for position, move in next_gen:
            
            new_game = Game(
                game.player1.player_type, game.player2.player_type, 
                int(position[0]), int(position[1]), int(position[2]), int(position[3]),
                'Player 1' if game.turn == 'Player 2' else 'Player 2'
            )
            
            key = new_game.key()
            
            if key in visited_positions:
                loop_detected = True
                tree['children'].append({'score': 0, 'pos': position, 'move': move, 'loop': True})
                score = 0                
            else:            
                visited_positions_copy = copy.deepcopy(visited_positions)
                visited_positions_copy.append(key)
                
                if init_game.solved_positions[player_to_max].get(key) is not None:
                    already_solved = True
                    score, solved_position = init_game.solved_positions[player_to_max][key]

                    tree['children'].append({'score': score, 'pos': position, 'move': move, 'already_solved': True}) 
                
               
                else:
                    score, child_move, child_tree = Game.minimax(init_game, new_game, player_to_max, depth + 1, visited_positions_copy, not is_maximizing)
                    init_game.solved_positions[player_to_max][key] = score, position
                    tree['children'].append(child_tree)
                    solved_counter = solved_counter + 1


            if is_maximizing and score > best_score:
                best_score = score
                best_move = copy.deepcopy(move)
            elif not is_maximizing and score < best_score:
                best_score = score
                best_move = copy.deepcopy(move)

        tree['score'] = best_score
        tree['move'] = best_move
        return best_score, best_move, tree