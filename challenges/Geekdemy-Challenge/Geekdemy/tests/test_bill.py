from unittest import TestCase, mock
from src.schemas.bill import Bill

class TestBill(TestCase):

    def setUp(self):
        self.bill = Bill()

    def test_update_sub_total_amount(self):
        self.bill.update_sub_total_amount(1000.0)
        self.assertEqual(self.bill.sub_total_amount, 1000.0)

    def test_update_coupon_details(self):
        self.bill.update_coupon_details("DEAL_G20", 10.0)
        self.assertEqual(self.bill.coupon_applied, "DEAL_G20")
        self.assertEqual(self.bill.coupon_discount, 10.0)

    def test_update_pro_membership_details(self):
        self.bill.update_pro_membership_details(200.0, 500.0)
        self.assertEqual(self.bill.pro_membership_fee, 200.0)
        self.assertEqual(self.bill.total_pro_discount, 500.0)

    def test_update_enrollment_fee(self):
        self.bill.update_enrollment_fee(500.0)
        self.assertEqual(self.bill.enrollment_fee_taken, 500.0)

    def test_get_total_amount_paid_without_coupon(self):
        self.bill.update_sub_total_amount(1000.0)
        self.assertEqual(self.bill.get_total_amount_paid(), 1000.0)

    def test_get_total_amount_paid_with_coupon(self):
        self.bill.update_sub_total_amount(1000.0)
        self.bill.update_coupon_details("DEAL_G20", 10.0)
        self.assertEqual(self.bill.get_total_amount_paid(), 990.0)

    @mock.patch('builtins.print')
    def test_print_receipt(self, mock_print):
        self.bill.update_sub_total_amount(1000.0)
        self.bill.update_coupon_details("DEAL_G20", 10.0)
        self.bill.update_pro_membership_details(200.0, 40.0)
        self.bill.update_enrollment_fee(500.0)

        self.bill.print_receipt()

        mock_print.assert_any_call("SUB_TOTAL 1000.00")
        mock_print.assert_any_call("COUPON_DISCOUNT DEAL_G20 10.00")
        mock_print.assert_any_call("TOTAL_PRO_DISCOUNT 40.00")
        mock_print.assert_any_call("PRO_MEMBERSHIP_FEE 200.00")
        mock_print.assert_any_call("ENROLLMENT_FEE 500.00")
        mock_print.assert_any_call("TOTAL 990.00")