from typing import Dict, List, Tuple
from ERC1155Token import ERC1155EnergyToken
import datetime
from time import time
from datas import *

frequency_time_unit = 1  # seconds

class Pool():
    def __init__(self, standard: str, carbon_type: str, issuance_year: int):
        self.standard = standard
        self.carbon_type = carbon_type
        self.issuance_year = issuance_year
        self.ownerToTokens: Dict[int, List[Tuple[time, ERC1155EnergyToken]]] = {}
        self.investments: List[Tuple[time, ERC1155EnergyToken]] = []
        self.prices: List[int] = []
        # there's another property for the pool that scales the frequency of minting based on the type of the accepted ERC1155 Energy tokens
        self.inherent_value = weights["standard"] * standards[self.standard] + weights["carbon_type"] * \
                              carbon_type_values[self.carbon_type] + weights["issuance_year"] * (
                                      self.issuance_year - 1980)
        self.current_frequency = 0
        self.raw_frequency = 0
        self.last_withdrawals_calculate: time = datetime.datetime.now()
        self.owners_withdrawals: Dict[int, int] = {}

    def __str__(self) -> str:
        return f"Pool: Standard: {self.standard}, Carbon Type: {self.carbon_type}, Issuance Year: {self.issuance_year}"

    def invest(self, token: ERC1155EnergyToken):
        if token.standard == self.standard and token.carbon_type == self.carbon_type and token.issuance_year == self.issuance_year:
            self.ownerToTokens[token.owner].append((datetime.datetime.now(), token))
            self.investments.append((datetime.datetime.now(), token))
            self.calculate_current_frequency()
            self.owners_withdrawals[token.owner] = 0
        else:
            raise Exception("The token is not valid for this pool")

    def get_current_price(self):
        # This is an API call
        price = 100
        self.prices.append(price)

        return price

    def calculate_current_frequency(self):
        # calculate the current frequency of minting based on the current price and the current frequency of minting and also current frequency of investment
        raw_frequency = self.get_raw_frequency()
        self.current_frequency = raw_frequency * self.inherent_value
        self.update_withdrawals_amounts()
        return self.current_frequency

    def update_withdrawals_amounts(self):
        current_frequency = self.current_frequency
        current_amount_for_each_value = current_frequency * (
                    datetime.datetime.now() - self.last_withdrawals_calculate) / frequency_time_unit
        for owner in self.ownerToTokens.keys():
            self.owners_withdrawals[owner] += current_amount_for_each_value * self.calculate_amount_of_erc1155_tokens(
                owner)
        self.last_withdrawals_calculate = datetime.datetime.now()

    def get_raw_frequency(self) -> int:
        return self.raw_frequency

    def calculate_amount_of_erc1155_tokens(self, owner: int) -> int:
        sum = 0
        for _, token in self.ownerToTokens[owner]:
            sum += token.carbon_value
        return sum

    def withdraw_benefit(self, owner: int):
        amount = self.owners_withdrawals[owner]
        self.owners_withdrawals[owner] = 0
        return amount