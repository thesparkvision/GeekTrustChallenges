class ProgramCategory:
    def __init__(self, name: str, cost: float, pro_discount: float):
        self._name: str = name
        self._cost: float = cost
        self._pro_discount: float = pro_discount
    
    def get_name(self) -> str:
        return self._name

    def get_cost(self) -> float:
        return self._cost

    def get_pro_discount(self) -> float:
        return self._cost * self._pro_discount