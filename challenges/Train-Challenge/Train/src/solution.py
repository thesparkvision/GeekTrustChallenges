from typing import List
from src.schemas import Bogie, BogieChain, Train
from src.constants import TRAIN_STATION_DETAILS

class Solution(object):

    def __init__(self, input_lines: List[str]) -> None:
        if len(input_lines) != 2:
            raise Exception("Needed 2 train inputs for the solution class to work")

        self.input_lines = input_lines
        self.trains_to_merge = []
        self.merged_train = None
        self.merging_station = "HYB"
        self.departure_station = "BPL"

        self.preprocessing()

    def preprocessing(self):
        STATIONS_BEFORE_HYB = dict()
        TRAIN_A_STATION = TRAIN_STATION_DETAILS["TRAIN_A"]
        TRAIN_A_STATION_HYB_DISTANCE = TRAIN_A_STATION.get("HYB")
        for key, value in TRAIN_STATION_DETAILS["TRAIN_A"].items():
            if value < TRAIN_A_STATION_HYB_DISTANCE:
                STATIONS_BEFORE_HYB[key] = value

        TRAIN_B_STATION = TRAIN_STATION_DETAILS["TRAIN_B"]
        TRAIN_B_STATION_HYB_DISTANCE = TRAIN_B_STATION.get("HYB")
        for key, value in TRAIN_STATION_DETAILS["TRAIN_B"].items():
            if value < TRAIN_B_STATION_HYB_DISTANCE:
                STATIONS_BEFORE_HYB[key]=value

        STATION_A_DISTANCES_AFTER_HYB = dict()
        for key, value in TRAIN_STATION_DETAILS["TRAIN_A"].items():
            if key not in STATIONS_BEFORE_HYB:
                STATION_A_DISTANCES_AFTER_HYB[key] = value - TRAIN_A_STATION_HYB_DISTANCE

        STATION_B_DISTANCES_AFTER_HYB = dict()
        for key, value in TRAIN_STATION_DETAILS["TRAIN_B"].items():
            if key not in STATIONS_BEFORE_HYB:
                STATION_B_DISTANCES_AFTER_HYB[key] = value - TRAIN_B_STATION_HYB_DISTANCE
        
        STATION_DIST = STATION_A_DISTANCES_AFTER_HYB.update(STATION_B_DISTANCES_AFTER_HYB)
        self.STATION_DISTANCES_AFTER_HYB = STATION_DIST
        self.STATIONS_BEFORE_HYB = STATIONS_BEFORE_HYB

    def process_input(self) -> None:
        for line in self.input_lines:
            train_name, _, *bogie_destinations = line.strip().split(" ")
            train_station_details = TRAIN_STATION_DETAILS.get(train_name, {})
            bogies = [
                Bogie(
                    destination=bogie_destination,
                    distance_remaining=train_station_details.get(bogie_destination, -1) 
                ) for bogie_destination in bogie_destinations if bogie_destination not in self.STATIONS_BEFORE_HYB
            ]
            #print(bogies, len(bogies), len(bogie_destinations))
            bogies.sort(key = lambda bogie: bogie.distance_remaining, reverse=True)
            print(bogies,"debug", end="\n\n")
            # train = Train(
            #     name=train_name, 
            #     bogies=bogies
            # )
            # self.trains_to_merge.append(train)

    def process_output(self) -> None:
        # trainA, trainB = self.trains_to_merge

        # # while trainA.des
        # trainAB = Train.merge(trainA, trainB)
        # self.merged_train = trainAB
        pass


    def print_output(self) -> None:
        pass