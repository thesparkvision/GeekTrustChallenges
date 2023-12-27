from typing import Union

class Bogie:
    def __init__(
        self, 
        destination: Union[str, None] = None, 
        distance_remaining: Union[int, None] = None
    ) -> None:
        self.destination = destination
        self.distance_remaining = distance_remaining
        self.prev_bogie = None
        self.next_bogie = None

    def __str__(self):
        return f"Station {self.destination} Bogie"
    
    def __repr__(self):
        return f"[Station {self.destination} Bogie, Remaining Distance {self.distance_remaining}]"