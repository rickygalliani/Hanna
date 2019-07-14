# Ricky Galliani
# Hanna
# src/security.py

from typing import Any, Dict, Optional

import json


class Security:
    def __init__(
        self,
        security_id: str,
        symbol: Optional[str] = None,
        name: Optional[str] = None,
        price: Optional[float] = None,
        buy_restricted: int = 1,
    ) -> None:
        if price and price <= 0:
            raise Exception(
                "Must pass positive price (or None) to instantiate a Security"
            )
        self.__id: str = security_id
        self.__symbol: Optional[str] = symbol
        self.__name: Optional[str] = name
        self.__price: Optional[float] = price
        self.__buy_restricted: int = buy_restricted
        if price:
            self.__purchase_buffer: float = 0.15 * price
        else:
            self.__purchase_buffer: float = 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Security):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def get_id(self) -> str:
        return self.__id

    def get_symbol(self) -> Optional[str]:
        return self.__symbol

    def get_name(self) -> Optional[str]:
        return self.__name

    def get_price(self) -> Optional[float]:
        return self.__price

    def get_purchase_buffer(self) -> float:
        return self.__purchase_buffer

    def get_buy_restricted(self) -> int:
        return self.__buy_restricted

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_symbol(self, symbol: str) -> None:
        self.__symbol = symbol

    def set_price(self, price: float) -> None:
        if price <= 0:
            raise Exception("Security price must be positive")
        self.__price = price
        self.__purchase_buffer = 0.15 * price

    def restrict_buy(self) -> None:
        self.__buy_restricted = 1

    def enable_buy(self) -> None:
        self.__buy_restricted = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.get_id(),
            "symbol": self.get_symbol(),
            "name": self.get_name(),
            "price": self.get_price(),
            "purchase_buffer": self.get_purchase_buffer(),
            "buy_restricted": self.get_buy_restricted(),
        }

    def with_cents(self) -> "Security":
        """
        Returns this security but with monetary amounts represented in cents,
        not dollars.
        """
        price = self.get_price()
        if price is None:
            raise Exception(
                "Security can't be converted to cents without a price"
            )
            return self
        return Security(
            self.get_id(),
            self.get_symbol(),
            self.get_name(),
            price * 100,
            self.get_buy_restricted(),
        )
