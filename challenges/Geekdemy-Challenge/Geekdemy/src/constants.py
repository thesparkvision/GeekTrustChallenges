from enum import Enum
from src.schemas.coupon import Coupon

ENROLLMENT_FEE_RULE_AMOUNT = 6666
ENROLLMENT_FEE_CHARGE = 500
PRO_MEMBERSHIP_FEE_CHARGE = 200

class CouponCode(Enum):
    B4G1 = "B4G1"
    DEAL_G20 = "DEAL_G20"
    DEAL_G5 = "DEAL_G5"

B4G1_coupon = Coupon(
    name=CouponCode.B4G1.value, 
    min_programs_count=4
) 
DEAL_G20_coupon = Coupon(
    name=CouponCode.DEAL_G20.value, 
    is_explicitly_required=True, 
    min_amount=10000.0
)
DEAL_G5_coupon = Coupon(
    name=CouponCode.DEAL_G5.value, 
    is_explicitly_required=True, 
    min_programs_count=2
)

DEAL_G20_COUPON_DISCOUNT_PERCENT = 0.20
DEAL_G5_COUPON_DISCOUNT_PERCENT = 0.05
