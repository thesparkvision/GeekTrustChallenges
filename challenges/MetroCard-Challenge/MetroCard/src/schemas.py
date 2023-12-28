from typing import List, Dict, Tuple
from datetime import date, datetime

TRAVEL_CHARGES_TYPE = {
    "ADULT": 200,
    "SENIOR_CITIZEN": 100,
    "KID": 50
}
RECHARGE_SERVICE_TAX_PERCENT = 0.02
RETURN_JOURNEY_DISCOUNT_PERCENT = 0.5
TRANSACTION_TYPES = {
    "DEBIT",
    "CREDIT"
}

class MetroCard:
    def __init__(self, id: str, initial_balance: int = 0):
        self.id: str = id
        self.__balance: int = initial_balance
        self.log_entries: List[Tuple(str, int)] = []

    def has_discount_available(self) -> bool:
        log_entry_count = len(self.log_entries)
        
        if log_entry_count > 0 and log_entry_count % 2 != 0:
            return True
        return False

    def find_discount_percent(self) -> int:
        discount_percent = 0
        if self.has_discount_available():
            discount_percent = RETURN_JOURNEY_DISCOUNT_PERCENT
        return discount_percent

    def add_log_entry(self, from_station: str, collected_amount: int) -> None:
        log_entry = (from_station, collected_amount)
        self.log_entries.append(log_entry)

    def get_balance_amount(self) -> int:
        return self.__balance
    
    def add_balance_amount(self, amount) -> int:
        self.__balance += amount
        return self.__balance
    
    def deduct_balance_amount(self, amount) -> int:
        if amount > self.__balance:
            raise Exception("Not enough amount to deduct!")
        self.__balance -= amount
        return self.__balance

class Station:
    def __init__(self, name: str):
        self.name = name
        self.collected_amount: int = 0
        self.discount_given: int = 0
        self.passenger_count_details: Dict[str, int] = {}

    def get_station_name(self):
        return self.name

    def update_station_collection(self, amount: int, passenger_type: str, discount_amount: int = 0):
        passenger_count = self.passenger_count_details.get(passenger_type, 0)
        self.passenger_count_details[passenger_type] = passenger_count + 1
        self.discount_given += discount_amount
        self.collected_amount += amount
    
    def display_station_collection_details(self):
        print("TOTAL_COLLECTION", self.name, self.collected_amount, self.discount_given)
        print("PASSENGER_TYPE_SUMMARY")
        
        passenger_count_details = list(self.passenger_count_details.items())
        passenger_count_details.sort(key = lambda x: (-x[1], x[0]))
        for passenger_type, passenger_count in passenger_count_details:
            print(passenger_type, passenger_count)

class StationCheckIn:
    def __init__(
        self,
        station: Station,
        metro_card: MetroCard,
        passenger_type: str
    ):
        self.station = station
        self.metro_card = metro_card
        self.passenger_type = passenger_type
        self.total_amount_charged = TRAVEL_CHARGES_TYPE[passenger_type]
        self.discount_amount = 0

    def apply_discount_if_any(self):
        discount_percent = self.metro_card.find_discount_percent()
        self.discount_amount = int(self.total_amount_charged * discount_percent)
        self.total_amount_charged = self.total_amount_charged - self.discount_amount

    def pay_final_amount(self):
        recharge_service_charge = 0
        balance_amount = self.metro_card.get_balance_amount()
        if balance_amount - self.total_amount_charged < 0:
            extra_balance_required = self.total_amount_charged - balance_amount
            recharge_service_charge = int(extra_balance_required * RECHARGE_SERVICE_TAX_PERCENT)
            self.metro_card.add_balance_amount(extra_balance_required)
            
        self.metro_card.deduct_balance_amount(self.total_amount_charged)
        self.total_amount_charged = self.total_amount_charged + recharge_service_charge

        self.station.update_station_collection(
            amount=self.total_amount_charged,
            passenger_type=self.passenger_type,
            discount_amount=self.discount_amount
        )
        station_name = self.station.get_station_name()
        self.metro_card.add_log_entry(station_name, self.total_amount_charged)