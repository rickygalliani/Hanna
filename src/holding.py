# Ricky Galliani
# Hanna
# src/holdingclass Security:

from src.security import Security

from typing import Any, Dict

import json


class Holding:
    def __init__(
        self,
        security: Security,
        num_shares: int,
        value: float,
        average_buy_price: float,
    ) -> None:
        if num_shares <= 0:
            raise Exception(
                "Holding must be instantiated with a positive number of shares"
            )
        if value <= 0:
            raise Exception(
                "Holding must be instantiated with a positive value"
            )
        self.__security: Security = security
        self.__num_shares: int = num_shares
        self.__value: float = value
        self.__average_buy_price: float = average_buy_price

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Holding):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def get_security(self) -> Security:
        return self.__security

    def get_num_shares(self) -> int:
        return self.__num_shares

    def get_value(self) -> float:
        return self.__value

    def get_average_buy_price(self) -> float:
        return self.__average_buy_price

    def get_return(self) -> float:
        value_per_share: float = self.get_value() / self.get_num_shares()
        abp: float = self.get_average_buy_price()
        return (value_per_share - abp) / abp

    def set_num_shares(self, num_shares: int) -> None:
        self.__num_shares = num_shares

    def set_value(self, value: float) -> None:
        self.__value = value

    def set_average_buy_price(self, average_buy_price: float) -> None:
        self.__average_buy_price = average_buy_price

    def to_dict(self) -> Dict[str, Any]:
        return {
            "security": self.get_security().to_dict(),
            "num_shares": self.get_num_shares(),
            "value": self.get_value(),
            "average_buy_price": self.get_average_buy_price(),
        }

    def add(self, other_holding: "Holding") -> None:
        """
        Adds the given holding to this holding by aggregating the holding data. 
        """
        if self.get_security() != other_holding.get_security():
            raise Exception(
                "Can only add holding of {} to this holding.".format(
                    self.get_security().get_id()
                )
            )
        cur_num_shares: int = self.get_num_shares()
        other_num_shares: int = other_holding.get_num_shares()
        cur_value: float = self.get_value()
        other_value: float = other_holding.get_value()
        cur_average_buy_price: float = self.get_average_buy_price()
        other_average_buy_price: float = other_holding.get_average_buy_price()
        avg_average_buy_price: float = (
            (
                cur_num_shares * cur_average_buy_price
                + other_num_shares * other_average_buy_price
            )
            / (cur_num_shares + other_num_shares)
        )
        self.set_num_shares(cur_num_shares + other_num_shares)
        self.set_value(cur_value + other_value)
        self.set_average_buy_price(avg_average_buy_price)
