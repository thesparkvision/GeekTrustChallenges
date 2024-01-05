from unittest import TestCase
from src.schemas.program_category import ProgramCategory
from src.schemas.program import Program

class TestProgram(TestCase):

    def setUp(self):
        self.program_category = ProgramCategory(name="DIPLOMA", cost=2000.0, pro_discount=0.1)
        self.program = Program(category=self.program_category)

    def test_get_category(self):
        self.assertEqual(self.program.get_category(), self.program_category)