import random

class Setuper:
    def __init__(self, characters):
        self.characters = characters
    
    def chooseMurdererAndVictim(self, previous):

        """
        This function initialized murdere and victim. 
        it takes array of 2 values as arguement
        these are two indexes that were choosen during the previous game
        and removes them from the possible choices, so no 2 consecutive pairs are choosen

        it return touple of 2 values. 
        result[0] is index of choosen murderer
        result[1] is index of choosen victim
        """

        prev_murderer_index = previous[0]
        prev_victim_index = previous[1]
        #choosing murderer and victim
        possible_choices = [i for i in range(6)]

        possible_choices.remove(prev_murderer_index)
        possible_choices.remove(prev_victim_index)

        murderer_index = random.choice(possible_choices)
        possible_choices.remove(murderer_index)
        victim_index = random.choice(possible_choices)

        
        return (self.characters[murderer_index], self.characters[victim_index])