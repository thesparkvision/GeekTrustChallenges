class Bill:
    def __init__(self):
        self.sub_total_amount: float = 0
        self.coupon_applied: str = "NONE" 
        self.coupon_discount: float = 0
        self.total_pro_discount: float = 0
        self.pro_membership_fee: float = 0
        self.enrollment_fee_taken: float = 0

    def update_sub_total_amount(self, sub_total_amount: float) -> None:
        self.sub_total_amount = sub_total_amount

    def update_coupon_details(self, coupon_applied: str, coupon_discount: float) -> None:
        self.coupon_applied = coupon_applied
        self.coupon_discount = coupon_discount

    def update_pro_membership_details(self, pro_membership_fee: float, total_pro_discount: float) -> None:
        self.pro_membership_fee = pro_membership_fee
        self.total_pro_discount = total_pro_discount

    def update_enrollment_fee(self, enrollment_fee: float) -> None:
        self.enrollment_fee_taken = enrollment_fee

    def get_total_amount_paid(self) -> float:
        return self.sub_total_amount + self.enrollment_fee_taken - self.coupon_discount 

    def print_receipt(self) -> None:
        print(f"SUB_TOTAL {self.sub_total_amount:.2f}")
        print(f"COUPON_DISCOUNT {self.coupon_applied} {self.coupon_discount:.2f}")
        print(f"TOTAL_PRO_DISCOUNT {self.total_pro_discount:.2f}")
        print(f"PRO_MEMBERSHIP_FEE {self.pro_membership_fee:.2f}")
        print(f"ENROLLMENT_FEE {self.enrollment_fee_taken:.2f}")
        print(f"TOTAL {self.get_total_amount_paid():.2f}")