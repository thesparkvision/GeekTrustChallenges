from typing import List
from datetime import date, datetime

from .schemas import MetroCardRepository, StationRepository

class Solution(object):

    def __init__(self, input_lines: List[str]) -> None:
        self.input_lines = input_lines
        self.metro_card_repository = MetroCardRepository()
        
        station_repository = StationRepository()
        station_repository.create_station(name="AIRPORT")
        station_repository.create_station(name="CENTRAL")
        self.station_repository = station_repository

        self.user_check_ins = []

    def process_input(self) -> None:        
        for line in self.input_lines:
            if line.startswith("BALANCE"):
                _, metro_card_id, initial_balance = line.split(" ")
                self.metro_card_repository.create_metro_card(metro_card_id, int(initial_balance))
            elif line.startswith("CHECK_IN"):
                _, metro_card_id, passenger_type, from_station = line.strip().split(" ")
                self.user_check_ins.append((metro_card_id, passenger_type, from_station))
        
    def process_output(self) -> None:
        for check_in in self.user_check_ins:
            metro_card_id, passenger_type, from_station = check_in
            metro_card = self.metro_card_repository.get_metro_card(metro_card_id)
            
            self.station_repository.user_check_in(
                metro_card=metro_card,
                passenger_type=passenger_type,
                from_station=from_station
            )

    def print_output(self) -> None:
        current_date = datetime.now().date()
        
        airport_station = self.station_repository.get_station("AIRPORT")
        central_station = self.station_repository.get_station("CENTRAL")

        central_station.print_record_entry(current_date)
        airport_station.print_record_entry(current_date)