# Ricky Galliani
# Hanna
# src/holdingclass Security:

from src.security import Security

from typing import Any, Dict, Optional

import json


class Holding:
    def __init__(
        self, security: Security, num_shares: int, average_buy_price: float
    ) -> None:
        if not isinstance(security, Security):
            raise Exception(
                "Holding must be instantiated with a Security instance"
            )
        if num_shares <= 0:
            raise Exception(
                "Holding must be instantiated with a positive number of shares"
            )
        self.__security: Security = security
        self.__num_shares: int = num_shares
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

    def get_average_buy_price(self) -> float:
        return self.__average_buy_price

    def get_value(self) -> float:
        price = self.get_security().get_price()
        if price is None:
            raise Exception(
                "Can't compute holding value, underlying "
                "security has undefined price"
            )
        return self.get_num_shares() * price

    def get_return(self) -> float:
        sec_price: Optional[float] = self.get_security().get_price()
        if sec_price is None:
            raise Exception(
                "Can't compute holding return, underlying "
                "security has undefined price"
            )
        num_shares: int = self.get_num_shares()
        value = sec_price * num_shares
        cost: float = self.get_average_buy_price() * num_shares
        return (value - cost) / cost

    def set_num_shares(self, num_shares: int) -> None:
        self.__num_shares = num_shares

    def set_average_buy_price(self, average_buy_price: float) -> None:
        self.__average_buy_price = average_buy_price

    def to_dict(self) -> Dict[str, Any]:
        return {
            "security": self.get_security().to_dict(),
            "num_shares": self.get_num_shares(),
            "average_buy_price": self.get_average_buy_price(),
        }
