from unittest import TestCase, mock
from datetime import date
import io

from src.schemas import MetroCard, Station, StationCheckIn, TRANSACTION_TYPES, TRAVEL_CHARGES_TYPE, RECHARGE_SERVICE_TAX_PERCENT, RETURN_JOURNEY_DISCOUNT_PERCENT

class TestMetroCard(TestCase):
    def test_initial_balance(self):
        metro_card = MetroCard("MC1")
        self.assertEqual(metro_card.get_balance_amount(), 0)

    def test_add_balance_amount(self):
        metro_card = MetroCard("MC1")
        metro_card.add_balance_amount(100)
        self.assertEqual(metro_card.get_balance_amount(), 100)

    def test_deduct_balance_amount(self):
        metro_card = MetroCard("MC1", initial_balance=100)
        metro_card.deduct_balance_amount(50)
        self.assertEqual(metro_card.get_balance_amount(), 50)

    def test_deduct_balance_amount_insufficient_funds(self):
        metro_card = MetroCard("MC1", initial_balance=20)
        with self.assertRaises(Exception):
            metro_card.deduct_balance_amount(100)

    def test_has_discount_available_no_log_entries(self):
        metro_card = MetroCard("MC1", initial_balance=300)
        self.assertFalse(metro_card.has_discount_available())

    def test_has_discount_available_odd_log_entries(self):
        metro_card = MetroCard("MC1", initial_balance=300)
        metro_card.add_log_entry("CENTRAL", 200)
        metro_card.add_log_entry("AIRPORT", 100)
        self.assertFalse(metro_card.has_discount_available())

    def test_has_discount_available_even_log_entries(self):
        metro_card = MetroCard("MC1", initial_balance=600)
        metro_card.add_log_entry("CENTRAL", 200)
        metro_card.add_log_entry("AIRPORT", 100)
        metro_card.add_log_entry("CENTRAL", 200)
        self.assertTrue(metro_card.has_discount_available())

    def test_find_discount_percent_with_discount(self):
        metro_card = MetroCard("MC1", initial_balance=200)
        metro_card.add_log_entry("CENTRAL", 100)
        self.assertEqual(metro_card.find_discount_percent(), RETURN_JOURNEY_DISCOUNT_PERCENT)

    def test_find_discount_percent_without_discount(self):
        metro_card = MetroCard("MC1")
        self.assertEqual(metro_card.find_discount_percent(), 0)

class TestStation(TestCase):

    def setUp(self):
        self.station = Station("CENTRAL")

    def test_initial_values(self):
        self.assertEqual(self.station.collected_amount, 0)
        self.assertEqual(self.station.discount_given, 0)
        self.assertEqual(self.station.passenger_count_details, {})

    def test_get_station_name(self):
        self.assertEqual(self.station.get_station_name(), "CENTRAL")

    def test_update_station_collection(self):
        self.station.update_station_collection(200, "ADULT", 10)
        self.assertEqual(self.station.collected_amount, 200)
        self.assertEqual(self.station.discount_given, 10)
        self.assertEqual(self.station.passenger_count_details, {"ADULT": 1})

        # Test with different passenger types
        self.station.update_station_collection(50, "SENIOR_CITIZEN", 5)
        self.station.update_station_collection(50, "KID", 0)
        self.station.update_station_collection(25, "KID", 8)

        self.assertEqual(self.station.collected_amount, 325)
        self.assertEqual(self.station.discount_given, 23)
        self.assertEqual(
            self.station.passenger_count_details,
            {"ADULT": 1, "SENIOR_CITIZEN": 1, "KID": 2},
        )

    def test_display_station_collection_details(self):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.station.display_station_collection_details()

        expected_output = "TOTAL_COLLECTION CENTRAL 0 0\nPASSENGER_TYPE_SUMMARY"
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

        self.station.update_station_collection(100, "ADULT", 10)
        self.station.update_station_collection(50, "SENIOR_CITIZEN", 5)

        with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            self.station.display_station_collection_details()

        expected_output = (
            "TOTAL_COLLECTION CENTRAL 150 15\n"
            "PASSENGER_TYPE_SUMMARY\n"
            "ADULT 1\nSENIOR_CITIZEN 1"
        )
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

class TestStationCheckIn(TestCase):

    def setUp(self):
        self.station = Station("CENTRAL")
        self.metro_card = MetroCard("123", initial_balance=300)

    def test_apply_discount_if_any_with_discount(self):
        self.metro_card.add_log_entry("CENTRAL", 100)

        station_check_in = StationCheckIn(self.station, self.metro_card, "ADULT")
        station_check_in.apply_discount_if_any()
        self.assertEqual(station_check_in.discount_amount, 100)

    def test_apply_discount_if_any_without_discount(self):
        station_checkin = StationCheckIn(self.station, self.metro_card, "ADULT")
        station_checkin.apply_discount_if_any()
        self.assertEqual(station_checkin.discount_amount, 0)

    def test_pay_final_amount_with_balance(self):
        station_checkin = StationCheckIn(self.station, self.metro_card, "ADULT")
        station_checkin.pay_final_amount()
        expected_balance = 100
        self.assertEqual(self.metro_card.get_balance_amount(), expected_balance)

    def test_pay_final_amount_insufficient_balance(self):
        self.metro_card.deduct_balance_amount(200)
        station_checkin = StationCheckIn(self.station, self.metro_card, "ADULT")
        station_checkin.pay_final_amount()
        expected_balance = 0
        self.assertEqual(self.metro_card.get_balance_amount(), expected_balance)

    def test_check_station_collection(self):
        station_checkin = StationCheckIn(self.station, self.metro_card, "ADULT")
        station_checkin.pay_final_amount()
        self.assertEqual(self.station.collected_amount, TRAVEL_CHARGES_TYPE["ADULT"])
        self.assertEqual(self.station.discount_given, 0)
        self.assertEqual(self.station.passenger_count_details, {"ADULT": 1})