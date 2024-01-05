from typing import List, Union, Callable, Tuple

from .bill import Bill
from .program import Program
from .coupon import Coupon

from src.constants import CouponCode, ENROLLMENT_FEE_CHARGE, ENROLLMENT_FEE_RULE_AMOUNT, PRO_MEMBERSHIP_FEE_CHARGE, B4G1_coupon, DEAL_G20_coupon, DEAL_G5_coupon, DEAL_G20_COUPON_DISCOUNT_PERCENT, DEAL_G5_COUPON_DISCOUNT_PERCENT

class ProgramWebsite:
    def __init__(self):
        self.programs_in_cart: List[Program] = []
        self.user_applied_coupons: List[str] = []
        self.is_pro_membership_taken: bool = False

        self.available_coupons = {
            CouponCode.B4G1.value: B4G1_coupon,
            CouponCode.DEAL_G20.value: DEAL_G20_coupon,
            CouponCode.DEAL_G5.value: DEAL_G5_coupon
        }

    @property
    def total_programs_in_cart(self) -> int:
        return len(self.programs_in_cart)

    def add_program_to_cart(self, program: Program) -> None:
        self.programs_in_cart.append(program)
    
    def apply_coupon(self, coupon_code: str) -> None:
        if coupon_code not in self.available_coupons:
            raise Exception("Not a valid Coupon Code!")
        self.user_applied_coupons.append(coupon_code)

    def add_pro_membership(self) -> None:
        self.is_pro_membership_taken = True
    
    def find_program_cost_details(self, program: Program) -> (float, float):
        program_category = program.get_category()
        program_cost = program_category.get_cost()
        
        pro_discount: float = 0.0
        
        if self.is_pro_membership_taken:
            pro_discount = program_category.get_pro_discount()
        return program_cost, pro_discount

    def find_sub_total_cost_details(self) -> (float, float):
        sub_total_cost: float = 0.0
        total_pro_discount: float = 0.0

        for program in self.programs_in_cart:
            program_cost, pro_discount = self.find_program_cost_details(program)
            total_pro_discount += pro_discount
            sub_total_cost += program_cost 
            
        if self.is_pro_membership_taken:
            sub_total_cost += PRO_MEMBERSHIP_FEE_CHARGE

        sub_total_cost = sub_total_cost - total_pro_discount

        return sub_total_cost, total_pro_discount

    def apply_enrollment_fee_if_any(self, amount: float) -> (float, float):
        enrollment_fee: float = 0.0
        if amount < ENROLLMENT_FEE_RULE_AMOUNT:
            enrollment_fee = ENROLLMENT_FEE_CHARGE
        return amount + enrollment_fee, enrollment_fee

    def is_applicable_coupon(self, sub_total_cost: float, coupon: Coupon) -> bool:
        if coupon.is_explicitly_required() and coupon.name not in self.user_applied_coupons:
            return False
        if self.total_programs_in_cart < coupon.get_minimum_programs_count_for_applying():
            return False
        if sub_total_cost < coupon.get_minimum_amount_for_applying():
            return False
        return True
        
    def find_applicable_coupon(self, sub_total_cost: float) -> Union[Coupon, None]:
        applicable_coupon: Union[str, None] = None

        if self.is_applicable_coupon(sub_total_cost, B4G1_coupon):
            applicable_coupon = B4G1_coupon
        elif self.is_applicable_coupon(sub_total_cost, DEAL_G20_coupon):
            applicable_coupon = DEAL_G20_coupon
        elif self.is_applicable_coupon(sub_total_cost, DEAL_G5_coupon):
            applicable_coupon = DEAL_G5_coupon

        return applicable_coupon

    def find_lowest_valued_program(self, sub_total_cost) -> Program:
        program_details = []
        for program in self.programs_in_cart:
            program_category = program.get_category()
            program_cost = program_category.get_cost()
            program_details.append((program, program_cost))

        min_program_detail = min(program_details, key = lambda program_detail: program_detail[1])
        return min_program_detail[0]

    def apply_B4G1_coupon(self, sub_total_cost: float) -> (float, float):
        program = self.find_lowest_valued_program(sub_total_cost)
        program_category = program.get_category()
        program_cost = program_category.get_cost()
        if self.is_pro_membership_taken:
            program_cost = program_cost - program_category.get_pro_discount()
        discount = program_cost
        return sub_total_cost - discount, discount

    def apply_DEAL_G20_coupon(self, sub_total_cost: float) -> (float, float):
        discount_percent = DEAL_G20_COUPON_DISCOUNT_PERCENT
        discount = sub_total_cost * discount_percent
        return sub_total_cost - discount, discount

    def apply_DEAL_G5_coupon(self, sub_total_cost: float) -> (float, float):
        discount_percent = DEAL_G5_COUPON_DISCOUNT_PERCENT
        discount = sub_total_cost * discount_percent
        return sub_total_cost - discount , discount

    def apply_coupon_discount_if_any(self, sub_total_cost: float, applicable_coupon: Coupon) -> (float, float):
        if not applicable_coupon:
            return sub_total_cost, 0.0
        
        calculate_new_cost_details: Callable[[float], Tuple[float, float]] = None
        
        apply_coupon_functions_mapping = {
            CouponCode.B4G1.value: self.apply_B4G1_coupon,
            CouponCode.DEAL_G20.value: self.apply_DEAL_G20_coupon,
            CouponCode.DEAL_G5.value: self.apply_DEAL_G5_coupon
        }
        calculate_new_cost_details = apply_coupon_functions_mapping.get(applicable_coupon.name)

        return calculate_new_cost_details(sub_total_cost)

    def buy_programs_in_cart(self) -> Bill:
        bill = Bill()
        
        sub_total_cost, total_pro_discount = self.find_sub_total_cost_details()
        bill.update_sub_total_amount(sub_total_cost)

        if self.is_pro_membership_taken:
            bill.update_pro_membership_details(PRO_MEMBERSHIP_FEE_CHARGE, total_pro_discount)

        applicable_coupon = self.find_applicable_coupon(sub_total_cost)
        total_cost, coupon_discount = self.apply_coupon_discount_if_any(sub_total_cost, applicable_coupon)
        if applicable_coupon:
            bill.update_coupon_details(applicable_coupon.name, coupon_discount)

        total_cost, enrollment_fee = self.apply_enrollment_fee_if_any(total_cost)
        bill.update_enrollment_fee(enrollment_fee)

        return bill