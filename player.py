from hand import Hand
from chopsticks_logger import logger

class Player():
    def __init__(self, player_type, l=1, r=1):
        self.right_hand = Hand(r)
        self.left_hand = Hand(l)
        self.is_alive = self.right_hand.is_alive or self.left_hand.is_alive
        if player_type not in ['human', 'computer']:
            raise ValueError('Type must be "human" or "computer"')
        self.is_human = player_type == 'human'
        self.player_type = player_type

    def receive_attack(self, damage, attacked_hand_str):
        # Modify fingers and update the status for both hands and the player
        if attacked_hand_str == 'r':
            self.right_hand.modify_fingers(damage)
        elif attacked_hand_str == 'l':
            self.left_hand.modify_fingers(damage)
        else:
            raise ValueError('Invalid hand to be attacked')
        self.is_alive = self.left_hand.is_alive or self.right_hand.is_alive