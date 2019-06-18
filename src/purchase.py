# Ricky Galliani
# Hanna
# src/purchase.py

from src.security import Security

from typing import Any, Dict

import json


class Purchase:
    def __init__(self, security: Security, num_shares: int) -> None:
        sec_price = security.get_price()
        if sec_price is None:
            raise Exception(
                "Purchase must be instantiated with a Security "
                "that has a non-None price"
            )
        if num_shares <= 0:
            raise Exception(
                "Purchase must be instantiated with num_shares >= 0"
            )
        self.__security: Security = security
        self.__num_shares: int = num_shares
        self.__cost: float = sec_price * self.__num_shares

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Purchase):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def get_security(self) -> Security:
        return self.__security

    def get_num_shares(self) -> int:
        return self.__num_shares

    def get_cost(self) -> float:
        return self.__cost

    def add_shares(self, num_shares: int) -> None:
        sec_price = self.get_security().get_price()
        if sec_price is None:
            raise Exception(
                "Cannot add shares to purchase for a security without"
                "a defined price"
            )
        self.__num_shares += num_shares
        self.__cost += num_shares * sec_price

    def to_dict(self) -> Dict[str, Any]:
        return {
            "security": self.get_security().to_dict(),
            "num_shares": self.get_num_shares(),
            "cost": self.get_cost(),
        }
