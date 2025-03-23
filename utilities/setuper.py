import random
from utilities.data import CHARACTERS, dialogues
import re

class Setuper:
    def __init__(self):
        self.characters = CHARACTERS
    
    def initRoles(self, previous):
        

        """
        This function initialized roles
        it takes array of 2 values as arguement
        these are two indexes that were choosen during the previous game
        and removes them from the possible choices, so no 2 consecutive pairs are choosen

        it return touple of 5 values. 
        result[0] is index of choosen murderer
        result[1] is index of choosen victim
        result[2] is index of the character that gives a key observation
        result[3] is index of the character that has false accusation for some character
        result[4] is index of the character that is falsely accused, but has an alibi
        """

        

        
        #choosing murderer and victim
        possible_choices = [i for i in range(5)]


        murderer_index = random.choice(possible_choices)
        victim_index = random.choice(possible_choices)

        while murderer_index == previous[0]:
            murderer_index = random.choice(possible_choices)
        possible_choices.remove(murderer_index)

        while victim_index == previous[1]:
            victim_index = random.choice(possible_choices)
        possible_choices.remove(victim_index)

        key_observer_index = random.choice(possible_choices)
        possible_choices.remove(key_observer_index)


        false_accuser, has_alibi = possible_choices


        
        return (self.characters[murderer_index], self.characters[victim_index], self.characters[key_observer_index], self.characters[false_accuser], self.characters[has_alibi])
    

    def parse_dialogue(self, text):
        pattern = re.compile(r"###\s*name::(?P<name>.*?)\s*Personal Statement::(?P<personal_statement>.*?)\s*Observation::(?P<observation>.*?)\s*###", re.DOTALL)
        matches = pattern.findall(text)

        parsed_data = []

        for match in matches:
            name, personal_statement, observation = match
            parsed_data.append({
                "name": name.strip(),
                "Personal Statement": personal_statement.strip(),
                "Observation": observation.strip()
            })

        dialogues = parsed_data
