class ProgramCategory:
    def __init__(self, name: str, cost: float, discount: float):
        self._name: str = name
        self._cost: float = cost
        self._discount: float = discount
    
    def get_name(self) -> str:
        return self._name

    def get_cost(self) -> float:
        return self._cost

    def get_discount(self) -> float:
        return self._discount