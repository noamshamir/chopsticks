from chopsticks_logger import logger

class Hand():
    def __init__(self, fingers = 1):
        self.fingers = fingers
        self.is_alive = self.fingers != 0
        self.modifier = 5
          
    def modify_fingers(self, modifier):
        self.fingers = (modifier + self.fingers) % self.modifier
        self.is_alive = self.fingers != 0