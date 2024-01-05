from unittest import TestCase
from unittest.mock import patch, MagicMock
from datetime import date
from src.schemas.program import Program
from src.schemas.program_category import ProgramCategory
from src.schemas.program_website import ProgramWebsite
from src.solution import Solution, ProgramNames

class TestSolution(TestCase):

    def setUp(self):
        self.input_lines = [
            "ADD_PROGRAMME CERTIFICATION 2",
            "ADD_PROGRAMME DIPLOMA 1",
            "APPLY_COUPON DEAL_G20",
            "ADD_PRO_MEMBERSHIP"
        ]

        self.program_categories = {
            "DIPLOMA": ProgramCategory("DIPLOMA", 2500, 0.1),
            "CERTIFICATION": ProgramCategory("CERTIFICATION", 3000, 0.2),
            "DEGREE": ProgramCategory("DEGREE", 5000, 0.5)
        }

        self.program = Program(category=self.program_categories["DIPLOMA"])

    @patch('src.solution.ProgramWebsite')
    def test_process_input(self, mock_program_website):
        solution = Solution(self.input_lines)
        solution.process_input()

        self.assertEqual(mock_program_website.return_value.add_program_to_cart.call_count, 3)
        mock_program_website.return_value.apply_coupon.assert_called_with('DEAL_G20')
        self.assertEqual(mock_program_website.return_value.add_pro_membership.call_count, 1)

    @patch('src.solution.ProgramWebsite')
    def test_process_output(self, mock_program_website):
        solution = Solution(self.input_lines)
        solution.process_input()
        solution.process_output()

        mock_program_website.return_value.buy_programs_in_cart.assert_called_once()

    @patch('src.solution.ProgramWebsite')
    def test_print_output(self, mock_program_website):
        mock_bill = MagicMock()
        mock_bill.print_receipt.return_value = None

        solution = Solution(self.input_lines)
        solution.process_input()
        solution.process_output()
        solution.print_output()

        mock_program_website.return_value.buy_programs_in_cart.assert_called_once()
        mock_program_website.return_value.buy_programs_in_cart.return_value.print_receipt.assert_called_once()