from typing import List, Dict
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

class CheckIn:
    def __init__(
        self, 
        metro_card_id: str, 
        passenger_type: str, 
        from_station: str, 
        initial_travel_charge: int,
        total_charge_collected: int,
        recharge_service_charge: int = 0,
        discount_amount: int = 0,
    ) -> None:
        self.metro_card_id = metro_card_id
        self.passenger_type = passenger_type
        self.from_station = from_station
        self.initial_travel_charge = initial_travel_charge
        self.total_charge_collected = total_charge_collected
        self.recharge_service_charge = recharge_service_charge
        self.discount_amount = discount_amount

class Transaction:
    def __init__(self, amount: int, transaction_type: str):
        self.amount = amount
        self.flow_type = transaction_type

class MetroCard:
    def __init__(self, id: str, initial_balance: int = 0):
        self.id: str = id
        self.__balance: int = initial_balance
        self.check_in_logs: Dict[date, List[CheckIn]] = {}
        self.transactions = []

        if initial_balance > 0:
            self.transactions.append(Transaction(initial_balance, "CREDIT"))

    @property
    def current_check_in_logs_count(self) -> CheckIn:
        current_date = datetime.now().date()
        todays_log = self.check_in_logs.get(current_date, [])
        return len(todays_log)
    
    def add_check_in_log(self, check_in: CheckIn):
        current_date = datetime.now().date()
        todays_log = self.check_in_logs.get(current_date)
        if not todays_log:
            self.check_in_logs[current_date] = [check_in]
        else:
            todays_log.append(check_in)

    def get_balance_amount(self) -> int:
        return self.__balance
    
    def add_balance_amount(self, amount) -> int:
        self.__balance += amount
        self.transactions.append(Transaction(amount, "CREDIT"))
        return self.__balance
    
    def deduct_balance_amount(self, amount) -> int:
        if amount > self.__balance:
            raise Exception("Not enough amount to deduct!")
        self.__balance -= amount
        self.transactions.append(Transaction(amount, "DEBIT"))
        return self.__balance
        
class MetroCardRepository:
    def __init__(self):
        self.metro_cards: Dict[str, MetroCard] = {}
        
    def create_metro_card(self, id: str, initial_balance: int = 0) -> None:
        if not id:
            raise Exception("Metro Card need to have an ID!")
        
        if id in self.metro_cards:
            raise Exception("Metro Card need to have unique ID. This ID is in assigned to somebody else!")
        
        metro_card = MetroCard(id, initial_balance)
        self.metro_cards[metro_card.id] = metro_card  

    def get_metro_card(self, id: str) -> MetroCard:
        return self.metro_cards.get(id)

class StationDailyRecordBook:
    def __init__(self):
        self.collected_amount: int = 0
        self.given_discount: int = 0
        self.passenger_counts: Dict[str, int] = {}

    def add_entry(self, amount: int, passenger_type: str, discount_amount: int = 0):
        passenger_count = self.passenger_counts.get(passenger_type, 0)
        self.passenger_counts[passenger_type] = passenger_count + 1
        self.given_discount += discount_amount
        self.collected_amount += amount
    
class Station:
    def __init__(self, name: str) -> None:
        self.name = name
        self.daily_records: Dict[date, StationDailyRecordBook] = {}
    
    def update_daily_record(self, amount, passenger_type, discount_amount):
        current_date = datetime.now().date()
        todays_record = self.daily_records.get(current_date) 
        if not todays_record:
            todays_record = StationDailyRecordBook()
            todays_record.add_entry(amount, passenger_type, discount_amount)
            self.daily_records[current_date] = todays_record 
        else:
            todays_record.add_entry(amount, passenger_type, discount_amount)
         
    def get_record_entry(self, entry_date: date) -> StationDailyRecordBook:
        record_entry = self.daily_records.get(entry_date)
        if not record_entry:
            raise Exception(f"Record Entry in Station {self.name} for {entry_date} not found!")
        return record_entry
    
    def print_record_entry(self, entry_date: date) -> None:
        record_entry = self.get_record_entry(entry_date)
        print("TOTAL_COLLECTION", self.name, record_entry.collected_amount, record_entry.given_discount)
        print("PASSENGER_TYPE_SUMMARY")
        for passenger_type, passenger_count in record_entry.passenger_counts.items():
            print(passenger_type, passenger_count)

class StationRepository:
    def __init__(self):
        self.stations: Dict[str, Station] = {}

    def create_station(self, name: str) -> Station:
        if name in self.stations:
            raise Exception(f"Station with name {name} already present!")
        
        new_station = Station(name)
        self.stations[name] = new_station
    
    def get_station(self, name: str) -> Station:
        station = self.stations.get(name)
        if not station:
            raise Exception(f"Station {name} not found")
        return station
    
    def user_check_in(self, metro_card: MetroCard, passenger_type: str, from_station: str):
        user_station = self.get_station(from_station)

        travel_charge = TRAVEL_CHARGES_TYPE[passenger_type]
        total_amount = travel_charge
        recharge_service_charge = 0

        discount_amount = 0
        check_in_count = metro_card.current_check_in_logs_count
        if check_in_count > 0 and check_in_count % 2 != 0:
            #print(user_station.name, passenger_type, metro_card.id, "ink")
            discount_amount = int(total_amount * RETURN_JOURNEY_DISCOUNT_PERCENT)
        total_amount = total_amount - discount_amount

        extra_balance_required = 0
        balance_amount = metro_card.get_balance_amount()
        if balance_amount - total_amount < 0:
            extra_balance_required = total_amount - balance_amount
            recharge_service_charge = int(extra_balance_required * RECHARGE_SERVICE_TAX_PERCENT)
            metro_card.add_balance_amount(extra_balance_required)
            metro_card.deduct_balance_amount(total_amount)
        else:
            metro_card.deduct_balance_amount(total_amount)
        
        total_amount_collected = total_amount + recharge_service_charge

        user_station.update_daily_record(
            amount=total_amount_collected,
            passenger_type=passenger_type,
            discount_amount=discount_amount
        )
        print(
            user_station.name, 
            metro_card.id,
            travel_charge,
            extra_balance_required, 
            total_amount_collected, 
            passenger_type, 
            discount_amount,
            metro_card.get_balance_amount()
        )

        check_in = CheckIn(
            metro_card_id = metro_card.id, 
            passenger_type = passenger_type, 
            from_station = from_station, 
            initial_travel_charge = travel_charge,
            total_charge_collected = total_amount_collected,
            recharge_service_charge = recharge_service_charge,
            discount_amount = discount_amount,
        )

        metro_card.add_check_in_log(check_in)