from copy import deepcopy
from typing import List
from .bogie import Bogie

class BogieChain:
    def __init__(self, bogies: List[Bogie] = []):
        self.head_bogie = None
        self.tail_bogie = None

        if len(bogies) > 0:
            self.create_bogie_chain(bogies)

    def __create_bogie_chain__(self, bogies: List[Bogie] = []) -> None:
        head_bogie = bogies[0]
        no_of_bogies = len(bogies)

        current_bogie_index = 1
        current_bogie = head_bogie
        next_bogie = None
        while current_bogie_index < no_of_bogies:
            next_bogie = bogies[current_bogie_index]
            next_bogie.prev_bogie = current_bogie
            current_bogie.next_bogie = current_bogie
            current_bogie_index += 1 

        self.head_bogie = head_bogie
        if next_bogie:
            tail_bogie = next_bogie
        else:
            tail_bogie = head_bogie
        self.tail_bogie = tail_bogie

    @staticmethod
    def __copy__(cls, existing_bogie_chain: 'BogieChain') -> 'BogieChain':
        head_bogie = deepcopy(existing_bogie_chain.head_bogie)

        current_bogie = head_bogie
        next_bogie = None
        while current_bogie and current_bogie.next_bogie:
            next_bogie = deepcopy(current_bogie.next_bogie)
            next_bogie.prev_bogie = current_bogie
            current_bogie.next_bogie = next_bogie
            current_bogie = next_bogie

        if next_bogie:
            tail_bogie = next_bogie
        else:
            tail_bogie = head_bogie

        new_bogie_chain = BogieChain(head_bogie, tail_bogie)
        return new_bogie_chain