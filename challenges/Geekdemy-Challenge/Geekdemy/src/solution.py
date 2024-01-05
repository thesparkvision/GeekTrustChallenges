from typing import List
from datetime import date, datetime
from enum import Enum

from src.schemas.program import Program
from src.schemas.program_website import ProgramWebsite
from src.schemas.program_category import ProgramCategory

class ProgramNames(Enum):
    CERTIFICATION = "CERTIFICATION"
    DEGREE = "DEGREE"
    DIPLOMA = "DIPLOMA"

class Solution(object):

    def __init__(self, input_lines: List[str]) -> None:
        self.input_lines = input_lines
        self.program_categories = {
            "DIPLOMA": ProgramCategory("DIPLOMA", 2500, 0.01),
            "CERTIFICATION": ProgramCategory("CERTIFICATION", 3000, 0.02),
            "DEGREE": ProgramCategory("DEGREE", 5000, 0.03)
        }
        self.program_website = ProgramWebsite()
        self.bill = None

    def add_program(self, category: str, quantity: int):
        program_category = self.program_categories[category]
        for _ in range(quantity):
            program = Program(program_category)
            self.program_website.add_program_to_cart(program)

    def process_input(self) -> None:        
        for line in self.input_lines:
            line = line.strip()
            
            if "ADD_PROGRAMME" in line:
                _, category, quantity = line.split(" ")
                self.add_program(category, int(quantity))

            elif "APPLY_COUPON" in line:
                _, coupon_code = line.split(" ")
                self.program_website.apply_coupon(coupon_code)

            elif "ADD_PRO_MEMBERSHIP" in line:
                self.program_website.add_pro_membership()
        
    def process_output(self) -> None:
        self.bill = self.program_website.buy_programs_in_cart()

    def print_output(self) -> None:
        self.bill.print_receipt()