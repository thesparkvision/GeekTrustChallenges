from typing import List, Dict, Union
from .bogie import Bogie
from .bogie_chain import BogieChain

class Train:
    def __init__(
        self, 
        name: str, 
        bogie_chain: BogieChain 
    ) -> None:
        self.name = name
        self.bogie_chain = bogie_chain
    
    @property
    def bogie_order(self) -> List[str]:
        station_names = []
        current_bogie = self.head_bogie
        while current_bogie:
            station_names.append(current_bogie.destination)
            current_bogie = current_bogie.next_bogie
        return station_names

    @property
    def next_destination(self) -> str:
        if not self.tail_bogie:
            return None
        return self.tail_bogie.destination
    
    @staticmethod
    def merge_trains(cls, first_train, second_train) -> 'Train':
        first_train_bogie_chain = BogieChain.__copy__(first_train.bogie_chain)
        second_train_bogie_chain = BogieChain.__copy__(second_train.bogie_chain)
        
        first_train_bogie = first_train_bogie_chain.head_bogie
        second_train_bogie =  second_train_bogie_chain.head_bogie

        new_bogie_chain = None

        if not first_train_bogie:
            new_bogie_chain = second_train_bogie_chain
        
        elif not second_train_bogie:
            new_bogie_chain = first_train_bogie_chain
        
        else:
            head_bogie = None
            tail_bogie = None
            root_bogie = Bogie()

            while first_train_bogie and second_train_bogie:
                if first_train_bogie.distance_remaining >= second_train_bogie.distance_remaining:
                    root_bogie.next_bogie = first_train_bogie
                    first_train_bogie.prev_bogie = root_bogie
                    first_train_bogie = first_train_bogie.next_bogie
                    tail_bogie = first_train_bogie
                else:
                    root_bogie.next_bogie = second_train_bogie
                    second_train_bogie.prev_bogie = root_bogie
                    second_train_bogie = second_train_bogie.next_bogie
                    tail_bogie = second_train_bogie
        
            if first_train_bogie:
                first_train_bogie.prev_bogie = root_bogie
                root_bogie.next_bogie = first_train_bogie
                tail_bogie = first_train_bogie_chain.tail_bogie

            if second_train_bogie:
                second_train_bogie.prev_bogie = root_bogie
                root_bogie.next_bogie = second_train_bogie
                tail_bogie = second_train_bogie_chain.tail_bogie

            new_bogie_chain = BogieChain(head_bogie, tail_bogie)

        new_train_name = first_train.name + second_train.name
        new_train = Train(
            name=new_train_name,
            bogie_chain=new_bogie_chain
        )
        return new_train
       
    def reach_next_station(self) -> None:
        tail_bogie = self.bogie_chain.tail_bogie
        if self.tail_bogie:
            prev_bogie = tail_bogie.prev_bogie
            prev_bogie.next_bogie = None
            self.bogie_chain.tail_bogie = prev_bogie

            #Update Remaining Distances for all bogies
            traversed_distance = tail_bogie.distance_remaining
            current_bogie = self.bogie_chain.head_bogie
            while current_bogie:
                current_bogie.distance_remaining - traversed_distance
                current_bogie = current_bogie.next_bogie