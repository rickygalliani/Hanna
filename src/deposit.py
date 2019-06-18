# Ricky Galliani
# Hanna
# src/deposit.py

from src.purchase import Purchase
from src.security import Security
from src.util import dollar_str

from prettytable import PrettyTable
from typing import Any, Dict, List, KeysView, Optional, Tuple

import json


class Deposit:
    def __init__(self):
        self.__total: float = 0.0  # Total spent on all purchases
        self.__num_shares: int = 0  # Total shares bought on all purchases
        self.__purchases: Dict[str, List[Purchase]] = {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Deposit):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def get_total(self) -> float:
        return self.__total

    def get_num_shares(self) -> int:
        return self.__num_shares

    def get_purchases(self) -> Dict[str, List[Purchase]]:
        return self.__purchases

    def get_involved_asset_classes(self) -> KeysView:
        return self.get_purchases().keys()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.get_total(),
            "num_shares": self.get_num_shares(),
            "purchases": self.get_purchases(),
        }

    def for_display(self) -> str:
        p_ac: PrettyTable = PrettyTable(["Asset Class", "Expenditures"])
        p_sec: PrettyTable = PrettyTable(
            ["Asset Class", "Security", "Symbol", "Shares", "Price", "Cost"]
        )
        p_ac.title = "Expenditures For Each Asset Class"
        p_sec.title = "Purchases"
        acs: List[Tuple[str, float]] = [
            (ac, self.get_asset_class_expenditures(ac))
            for ac in self.get_involved_asset_classes()
        ]
        sorted_acs: List[Tuple[str, float]] = sorted(
            acs, key=lambda x: x[1], reverse=True
        )
        for ac_name, ac_exp in sorted_acs:
            p_ac.add_row([ac_name, dollar_str(ac_exp)])
            ps: List[Tuple[Purchase, float]] = [
                (p, p.get_cost())
                for p in self.get_purchases_for_asset_class(ac_name)
            ]
            sorted_ps: List[Tuple[Purchase, float]] = sorted(
                ps, key=lambda x: x[1], reverse=True
            )
            for p, p_cost in sorted_ps:
                sec: Security = p.get_security()
                name: Optional[str] = sec.get_name()
                sym: str = sec.get_symbol()
                shares: int = p.get_num_shares()
                price: Optional[float] = sec.get_price()
                price_str: str = dollar_str(price) if price is not None else ""
                cost: str = dollar_str(p_cost)
                p_sec.add_row([ac_name, name, sym, shares, price_str, cost])
        p_ac.add_row(["Total", dollar_str(self.get_total())])
        tot_shares: int = self.get_num_shares()
        tot_cost: float = self.get_total()
        p_sec.add_row(
            ["Total", "-", "-", tot_shares, "-", dollar_str(tot_cost)]
        )
        return "\n{}\n{}".format(p_ac, p_sec)

    def add_purchase(self, asset_class_name: str, purchase: Purchase) -> None:
        """
        Adds the given purchase to the list of purchases to be made for the
        given asset class.
        """
        if self.involves_asset_class(asset_class_name):
            self.__purchases[asset_class_name] += [purchase]
        else:
            self.__purchases[asset_class_name] = [purchase]
        self.__total += purchase.get_cost()
        self.__num_shares += purchase.get_num_shares()

    def involves_asset_class(self, asset_class_name: str) -> bool:
        """
        Returns whether this deposit involves purchases made in the given
        asset class.
        """
        return asset_class_name in self.get_involved_asset_classes()

    def get_purchases_for_asset_class(
        self, asset_class_name: str
    ) -> List[Purchase]:
        """
        Returns the purchases to be made for the given asset class for this
        deposit.
        """
        if self.involves_asset_class(asset_class_name):
            return self.get_purchases()[asset_class_name]
        raise Exception(
            "Deposit does not involve asset class {}.".format(asset_class_name)
        )

    def get_asset_class_expenditures(self, asset_class_name: str) -> float:
        """
        Returns the total expenditures in the given asset class.
        """
        ps: List[Purchase] = self.get_purchases_for_asset_class(
            asset_class_name
        )
        return sum(p.get_cost() for p in ps)
