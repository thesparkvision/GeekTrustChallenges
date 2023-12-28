from .program_category import ProgramCategory

class Program:
    def __init__(self, category: ProgramCategory, quantity: int):
        self._category = category
        self._quantity = quantity

    def get_category(self) -> ProgramCategory:
        return self._category

    def get_quantity(self) -> int:
        return self._quantity