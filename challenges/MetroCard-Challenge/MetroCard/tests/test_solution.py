from unittest import TestCase, mock
from datetime import date
import io

from src.solution import Solution

class TestSolution(TestCase):

    def setUp(self):
        self.input_lines = [
            "BALANCE 1 100",
            "CHECK_IN 1 ADULT AIRPORT"
        ]

    def test_process_input(self):
        solution_instance = Solution(self.input_lines)
        solution_instance.process_input()

    def test_process_output(self):
        solution_instance = Solution(self.input_lines)
        solution_instance.process_input()

        solution_instance.process_output()

    def test_print_output(self):
        solution_instance = Solution(self.input_lines)
        solution_instance.process_input()
        solution_instance.process_output()

        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            solution_instance.print_output()

        expected_output = [
            "TOTAL_COLLECTION CENTRAL 0 0",
            "PASSENGER_TYPE_SUMMARY",
            "TOTAL_COLLECTION AIRPORT 202 0",
            "PASSENGER_TYPE_SUMMARY",
            "ADULT 1"
        ]
        expected_output = "\n".join(expected_output)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)