from typing import List
from datetime import date, datetime

from .schemas import MetroCard, Station, StationCheckIn

AIRPORT_STATION_NAME = "AIRPORT"
CENTRAL_STATION_NAME = "CENTRAL"

class Solution(object):

    def __init__(self, input_lines: List[str]) -> None:
        self.input_lines = input_lines
        
        self.metro_cards_lookup = {}

        self.stations_lookup = {}
        self.stations_lookup[AIRPORT_STATION_NAME] = Station(name=AIRPORT_STATION_NAME)
        self.stations_lookup[CENTRAL_STATION_NAME] = Station(name=CENTRAL_STATION_NAME)

        self.station_check_ins = []

    def process_input(self) -> None:        
        for line in self.input_lines:
            if line.startswith("BALANCE"):
                _, metro_card_id, initial_balance = line.split(" ")
                metro_card = MetroCard(
                    id=metro_card_id, 
                    initial_balance=int(initial_balance)
                )
                self.metro_cards_lookup[metro_card_id] = metro_card

            elif line.startswith("CHECK_IN"):
                _, metro_card_id, passenger_type, from_station = line.strip().split(" ")
                self.station_check_ins.append((metro_card_id, passenger_type, from_station))
        
    def process_output(self) -> None:
        for check_in in self.station_check_ins:
            metro_card_id, passenger_type, from_station = check_in
            
            metro_card = self.metro_cards_lookup[metro_card_id]
            station = self.stations_lookup[from_station]
            
            station_check_in = StationCheckIn(
                station=station,
                metro_card=metro_card,
                passenger_type=passenger_type
            )
            station_check_in.apply_discount_if_any()
            station_check_in.pay_final_amount()

    def print_output(self) -> None:
        airport_station = self.stations_lookup[AIRPORT_STATION_NAME]
        central_station = self.stations_lookup[CENTRAL_STATION_NAME]

        central_station.display_station_collection_details()
        airport_station.display_station_collection_details()