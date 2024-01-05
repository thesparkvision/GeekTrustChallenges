from .program_category import ProgramCategory

class Program:
    def __init__(self, category: ProgramCategory):
        self._category = category

    def get_category(self) -> ProgramCategory:
        return self._category