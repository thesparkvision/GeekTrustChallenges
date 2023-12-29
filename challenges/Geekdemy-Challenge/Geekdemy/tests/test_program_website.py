from unittest import TestCase
from unittest.mock import patch

from src.schemas.program_category import ProgramCategory
from src.schemas.program import Program
from src.schemas.program_website import ProgramWebsite
from src.schemas.bill import Bill

class TestProgramWebsite(TestCase):

    def setUp(self):
        self.program_category = ProgramCategory(name="DIPLOMA", cost=100.0, discount=10.0)
        self.program = Program(category=self.program_category, quantity=3)
        self.program_website = ProgramWebsite()

    def test_add_program_to_cart(self):
        self.program_website.add_program_to_cart(self.program)
        self.assertEqual(len(self.program_website.programs_in_cart), 1)

    def test_apply_coupon_valid(self):
        self.program_website.apply_coupon("DEAL_G20")
        self.assertEqual(len(self.program_website.user_applied_coupons), 1)

    def test_apply_coupon_invalid(self):
        with self.assertRaises(Exception):
            self.program_website.apply_coupon("INVALID_COUPON")

    @patch('src.schemas.program_website.ProgramWebsite.find_lowest_valued_program')
    def test_apply_B4G1_coupon(self, mock_find_lowest_valued_program):
        mock_find_lowest_valued_program.return_value = self.program
        sub_total_cost = 300.0
        result = self.program_website.apply_B4G1_coupon(sub_total_cost)
        self.assertEqual(result, (200.0, 100.0))

    @patch('src.schemas.program_website.ProgramWebsite.find_lowest_valued_program')
    def test_apply_DEAL_G20_coupon(self, mock_find_lowest_valued_program):
        mock_find_lowest_valued_program.return_value = self.program
        sub_total_cost = 1000.0
        result = self.program_website.apply_DEAL_G20_coupon(sub_total_cost)
        self.assertEqual(result, (800.0, 200.0))

    @patch('src.schemas.program_website.ProgramWebsite.find_lowest_valued_program')
    def test_apply_DEAL_G5_coupon(self, mock_find_lowest_valued_program):
        mock_find_lowest_valued_program.return_value = self.program
        sub_total_cost = 300.0
        result = self.program_website.apply_DEAL_G5_coupon(sub_total_cost)
        self.assertEqual(result, (285.0, 15.0))

    def test_apply_enrollment_fee_if_any_with_fee(self):
        amount = 5000.0
        result = self.program_website.apply_enrollment_fee_if_any(amount)
        self.assertEqual(result, (5500.0, 500.0))

    def test_apply_enrollment_fee_if_any_without_fee(self):
        amount = 7000.0
        result = self.program_website.apply_enrollment_fee_if_any(amount)
        self.assertEqual(result, (7000.0, 0.0))

    def test_add_pro_membership(self):
        self.assertFalse(self.program_website.is_pro_membership_taken)
        self.program_website.add_pro_membership()
        self.assertTrue(self.program_website.is_pro_membership_taken)

    def test_find_applicable_coupon_B4G1(self):
        # If the total_programs_count is greater than or equal to 4, "B4G1" should be applicable
        self.program_website.user_applied_coupons = {"DEAL_G20", "DEAL_G5"}
        self.program_website.total_programs_count = 5
        result = self.program_website.find_applicable_coupon(sub_total_cost=500.0)
        self.assertEqual(result, "B4G1")

    def test_find_applicable_coupon_DEAL_G20(self):
        # If total_programs_count is less than 4 but sub_total_cost is >= 10000 and "DEAL_G20" applied, "DEAL_G20" should be applicable
        self.program_website.user_applied_coupons = {"DEAL_G20", "DEAL_G5"}
        self.program_website.total_programs_count = 3
        result = self.program_website.find_applicable_coupon(sub_total_cost=12000.0)
        self.assertEqual(result, "DEAL_G20")

    def test_find_applicable_coupon_DEAL_G5(self):
        # If total_programs_count is less than 4, sub_total_cost is < 10000, and "DEAL_G5" applied, "DEAL_G5" should be applicable
        self.program_website.user_applied_coupons = {"DEAL_G20", "DEAL_G5"}
        self.program_website.total_programs_count = 3
        result = self.program_website.find_applicable_coupon(sub_total_cost=8000.0)
        self.assertEqual(result, "DEAL_G5")

    def test_find_applicable_coupon_none(self):
        # If none of the conditions are met, no coupon should be applicable
        self.program_website.total_programs_count = 3
        result = self.program_website.find_applicable_coupon(sub_total_cost=5000.0)
        self.assertIsNone(result)
    
    def test_find_program_cost_details_without_pro_membership(self):
        program_category = ProgramCategory("CERTIFICATION", 3000, 0.2)
        program = Program(program_category, 1)

        cost, discount = self.program_website.find_program_cost_details(program)

        self.assertEqual(cost, 3000)
        self.assertEqual(discount, 0.0)

    def test_find_program_cost_details_with_pro_membership(self):
        program_website = ProgramWebsite()
        program_website.add_pro_membership()
        program_category = ProgramCategory("CERTIFICATION", 3000, 0.2)
        program = Program(program_category, 1)

        cost, discount = program_website.find_program_cost_details(program)

        self.assertEqual(cost, 2400)
        self.assertEqual(discount, 600) 

    def test_find_lowest_valued_program(self):
        program2 = Program(category=self.program_category, quantity=1)
        program3 = Program(category=self.program_category, quantity=2)
        self.program_website.programs_in_cart = [self.program, program2, program3]
        result = self.program_website.find_lowest_valued_program(sub_total_cost=500.0)
        self.assertEqual(result.get_category().get_name(), program2.get_category().get_name())

    @patch('src.schemas.program_website.ProgramWebsite.apply_B4G1_coupon')
    def test_apply_coupon_discount_if_any_B4G1(self, mock_apply_B4G1_coupon):
        sub_total_cost = 500.0
        self.program_website.find_applicable_coupon = lambda x: "B4G1"
        result = self.program_website.apply_coupon_discount_if_any(sub_total_cost, applicable_coupon="B4G1")
        mock_apply_B4G1_coupon.assert_called_with(sub_total_cost)
        self.assertEqual(result, mock_apply_B4G1_coupon.return_value)

    @patch('src.schemas.program_website.ProgramWebsite.apply_DEAL_G20_coupon')
    def test_apply_coupon_discount_if_any_DEAL_G20(self, mock_apply_DEAL_G20_coupon):
        sub_total_cost = 1000.0
        self.program_website.find_applicable_coupon = lambda x: "DEAL_G20"
        result = self.program_website.apply_coupon_discount_if_any(sub_total_cost, applicable_coupon="DEAL_G20")
        mock_apply_DEAL_G20_coupon.assert_called_with(sub_total_cost)
        self.assertEqual(result, mock_apply_DEAL_G20_coupon.return_value)

    @patch('src.schemas.program_website.ProgramWebsite.apply_DEAL_G5_coupon')
    def test_apply_coupon_discount_if_any_DEAL_G5(self, mock_apply_DEAL_G5_coupon):
        sub_total_cost = 300.0
        self.program_website.find_applicable_coupon = lambda x: "DEAL_G5"
        result = self.program_website.apply_coupon_discount_if_any(sub_total_cost, applicable_coupon="DEAL_G5")
        mock_apply_DEAL_G5_coupon.assert_called_with(sub_total_cost)
        self.assertEqual(result, mock_apply_DEAL_G5_coupon.return_value)

    def test_apply_coupon_discount_if_any_no_coupon(self):
        sub_total_cost = 500.0
        expected_result = (sub_total_cost, 0.0)
        self.program_website.find_applicable_coupon = lambda x: None
        result = self.program_website.apply_coupon_discount_if_any(sub_total_cost, applicable_coupon=None)
        self.assertEqual(result, expected_result)

    def test_buy_programs_in_cart(self):
        self.program_website.add_program_to_cart(self.program)
        self.program_website.add_pro_membership()
        self.program_website.apply_coupon("DEAL_G5")
        result = self.program_website.buy_programs_in_cart()
        self.assertIsInstance(result, Bill)