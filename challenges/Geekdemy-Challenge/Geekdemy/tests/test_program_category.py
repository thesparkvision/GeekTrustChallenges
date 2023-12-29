from unittest import TestCase
from src.schemas.program_category import ProgramCategory

class TestProgramCategory(TestCase):

    def setUp(self):
        self.program_category = ProgramCategory(name="DIPLOMA", cost=1000.0, discount=0.1)

    def test_get_name(self):
        self.assertEqual(self.program_category.get_name(), "DIPLOMA")

    def test_get_cost(self):
        self.assertEqual(self.program_category.get_cost(), 1000.0)

    def test_get_discount(self):
        self.assertEqual(self.program_category.get_discount(), 100.0)