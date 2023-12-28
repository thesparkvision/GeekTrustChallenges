from typing import List, Union
from abc import ABC

ENROLLEMENT_FEE_RULE_AMOUNT = 6666
ENROLLMENT_FEE_CHARGE = 500
PRO_MEMBERSHIP_FEE_CHARGE = 200
AVAILABLE_COUPONS = {"DEAL_G20", "DEAL_G5"}
PROGRAM_VALUES = {
    "DIPLOMA": {
        "cost": 2500,
        "discount": 0.1
    },
    "CERTIFICATION": {
        "cost": 3000,
        "discount": 0.2
    },
    "DEGREE": {
        "cost": 5000,
        "discount": 0.3
    }
}
class ProgramCategory:
    def __init__(self, name: str, cost: float, discount: float):
        self._name = name
        self._cost = cost
        self._discount = discount
    
    def get_name(self) -> str:
        return self._name

    def get_cost(self) -> float:
        return self._cost

    def get_discount(self) -> float:
        return self._discount

class Program:
    def __init__(self, category: ProgramCategory, quantity: int):
        self._category = category
        self._quantity = quantity

    def get_category(self) -> ProgramCategory:
        return self._category

    def get_quantity(self) -> int:
        return self._quantity

class ProgramWebsite:
    def __init__(self):
        self.programs_in_cart: List[Program] = []
        self.user_applied_coupons: List[str] = []
        self.is_pro_membership_taken: bool = False

    def add_program_to_cart(self, program: Program):
        self.programs_in_cart.append(program)
    
    def apply_coupon(self, coupon_code: str):
        if coupon_code not in AVAILABLE_COUPONS:
            raise Exception("Not a valid Coupon Code!")
        self.user_applied_coupons.append(coupon_code)

    def add_pro_membership(self):
        self.is_pro_membership_taken = True
    
    def _find_program_cost(self, program: Program):
        program_category = program.get_category()
        program_cost = program_category.get_cost()
        pro_discount: float = 0.0
        if self.is_pro_membership_taken:
            pro_discount = program_category.get_discount()
            program_cost -= pro_discount
        return program_cost, pro_discount

    def _find_sub_total_cost(self):
        sub_total_cost: float = 0.0
        total_pro_discount: float = 0.0
        for program in self.programs_in_cart:
            program_cost, pro_discount = self._find_program_cost(program)
            total_pro_discount += total_pro_discount
            sub_total_cost += program_cost
        return sub_total_cost, total_pro_discount

    def apply_enrollment_fee_if_any(self, amount: float):
        enrollment_fee: float = 0
        if amount < ENROLLEMENT_FEE_RULE_AMOUNT:
            enrollment_fee = ENROLLMENT_FEE_CHARGE
        return amount + enrollment_fee, enrollment_fee

    def _find_applicable_coupon(self, sub_total_cost: float):
        applicable_coupon = None

        if len(self.programs_in_cart) >= 4:
            applicable_coupon = "B4G1"

        if sub_total_cost >= 10000.0 and "DEAL_G20" in self.user_applied_coupons:
            applicable_coupon = "DEAL_G20"
        elif len(self.programs_in_cart) >= 2 and "DEAL_G5" in self.user_applied_coupons:
            applicable_coupon = "DEAL_G5"
        
        return applicable_coupon

    def find_lowest_valued_program(self, sub_total_cost):
        return min(self.programs_in_cart, key = lambda program: program.get_category().get_cost())

    def apply_B4G1_coupon(self, sub_total_cost):
        program = self.find_lowest_valued_program()
        discount = program.get_cost()
        return sub_total_cost - discount, discount

    def apply_DEAL_G20_coupon(self, sub_total_cost):
        discount_percent = 0.2
        discount = sub_total_cost * discount_percent
        return sub_total_cost - discount, discount

    def apply_DEAL_G5_coupon(self, sub_total_cost):
        discount_percent = 0.05
        discount = sub_total_cost * discount_percent
        return sub_total_cost - discount , discount

    def apply_coupon_discount_if_any(self, sub_total_cost, applicable_coupon):
        if not applicable_coupon:
            return sub_total_cost
        
        coupon_func = None
        match applicable_coupon:
            case "B4G1":
                coupon_func = self.apply_B4G1_coupon
            case "DEAL_G20":
                coupon_func = self.apply_DEAL_G20_coupon
            case "DEAL_G5":
                coupon_func = self.apply_DEAL_G5_coupon
        
        return coupon_func(sub_total_cost)

    def buy_programs_in_cart(self):
        bill = Bill()
        
        sub_total_cost, total_pro_discount = self._find_sub_total_cost()
        bill.update_sub_total_amount(sub_total_cost)

        if self.is_pro_membership_taken:
            bill.update_pro_membership_details(PRO_MEMBERSHIP_FEE_CHARGE, total_pro_discount)

        applicable_coupon = self._find_applicable_coupon(sub_total_cost)
        total_cost, coupon_discount = self.apply_coupon_discount_if_any(sub_total_cost, applicable_coupon)
        if applicable_coupon:
            bill.update_coupon_details(applicable_coupon, coupon_discount)

        total_cost, enrollment_fee = self.apply_enrollment_fee_if_any(total_cost)
        bill.update_enrollment_fee(enrollment_fee)

        return bill
        
class Bill:
    def __init__(self):
        self.sub_total_amount: float = 0
        self.coupon_applied: str = "NONE" 
        self.coupon_discount: float = 0
        self.total_pro_discount: float = 0
        self.pro_membership_fee: float = 0
        self.enrollment_fee_taken: float = 0

    def update_sub_total_amount(self, sub_total_amount):
        self.sub_total_amount = sub_total_amount

    def update_coupon_details(self, coupon_applied: str, coupon_discount: float):
        self.coupon_applied = coupon_applied
        self.coupon_discount = coupon_discount

    def update_pro_membership_details(self, pro_membership_fee: float, total_pro_discount: float):
        self.pro_membership_fee = pro_membership_fee
        self.total_pro_discount = total_pro_discount

    def update_enrollment_fee(self, enrollment_fee: float):
        self.enrollment_fee_taken = enrollment_fee

    def get_total_amount_paid(self):
        return self.sub_total_amount - self.coupon_discount 

    def print_receipt(self):
        print("SUB_TOTAL", self.sub_total_amount)
        print("COUPON_DISCOUNT", self.coupon_applied, self.coupon_discount)
        print("TOTAL_PRO_DISCOUNT", self.total_pro_discount)
        print("PRO_MEMBERSHIP_FEE", self.pro_membership_fee)
        print("ENROLLMENT_FEE", self.enrollment_fee_taken)
        print("TOTAL", self.get_total_amount_paid())