# Ricky Galliani
# Hanna
# src/asset_class.py

from src.holding import Holding
from src.purchase import Purchase
from src.security import Security
from src.util import dollar_str

from typing import Any, Dict, List, ValuesView

import robin_stocks as r

import json
import logging

log = logging.getLogger(__name__)


class AssetClass:
    def __init__(self, name: str, target_percentage: float) -> None:
        self.__name: str = name
        self.__target_percentage: float = target_percentage
        self.__securities: Dict[str, Security] = {}
        self.__holdings: Dict[str, Holding] = {}
        self.__purchase_buffer: float = 0.0
        self.__value: float = 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AssetClass):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def get_name(self) -> str:
        return self.__name

    def get_target_percentage(self) -> float:
        return self.__target_percentage

    def get_securities(self) -> ValuesView:
        return self.__securities.values()

    def get_holdings(self) -> ValuesView:
        return self.__holdings.values()

    def get_purchase_buffer(self) -> float:
        secs = self.get_securities()
        if len(secs) == 0:
            return 0.0
        else:
            return max([s.get_purchase_buffer() for s in secs])

    def get_value(self) -> float:
        return self.__value

    def set_target_percentage(self, target_percentage: float) -> None:
        self.__target_percentage = target_percentage

    def to_dict(self) -> Dict[str, Any]:
        secs: List[Dict[str, Any]] = sorted(
            [s.to_dict() for s in self.get_securities()],
            key=lambda sec: sec["id"],
        )
        hols: List[Dict[str, Any]] = sorted(
            [h.to_dict() for h in self.get_holdings()],
            key=lambda hol: hol["security"]["id"],
        )
        ac = {
            "name": self.get_name(),
            "target_percentage": self.get_target_percentage(),
            "securities": secs,
            "holdings": hols,
            "purchase_buffer": self.get_purchase_buffer(),
            "value": self.get_value(),
        }
        return ac

    def get_security(self, security_id: str) -> Security:
        """
        Returns the security for the given security id.
        """
        if self.contains_security(security_id):
            return self.__securities[security_id]
        else:
            raise Exception(
                "get_security(): {} is not in the '{}' asset "
                "class's securities.".format(security_id, self.get_name())
            )

    def get_holding(self, security_id: str) -> Holding:
        """
        Returns this asset class's holdings of the given security.
        """
        if self.contains_holding(security_id):
            return self.__holdings[security_id]
        else:
            m = "get_holding(): {} is not in the '{}' asset class's holdings."
            raise Exception(m.format(security_id, self.get_name()))

    def contains_security(self, security_id: str) -> bool:
        """
        Returns True if this asset class contains the given security.
        """
        return security_id in self.__securities

    def contains_holding(self, security_id: str) -> bool:
        """
        Returns True if this asset class contains a holding of the given
        security.
        """
        return security_id in self.__holdings

    def add_value(self, amount: float) -> None:
        """
        Adds the given value to this asset class.
        """
        if self.__value:
            self.__value += amount
        else:
            self.__value = amount

    def add_security(self, security: Security) -> None:
        """
        Adds the given security to this asset class.
        """
        sec_id: str = security.get_id()
        if not self.contains_security(sec_id):
            self.__securities[sec_id] = security
        else:
            raise Exception(
                "add_security(): {} was already added to the '{}'"
                "asset class.".format(sec_id, self.get_name())
            )

    def add_holding(self, holding: Holding) -> None:
        """
        Adds the given holding to this asset class.

        Possible cases (HS: has security, HH: has holding):
        1) HS, HH: user already added holding and security, raise error
        2) !HS, HH: impossible in theory, raise error
        3) HS, !HH: good use case
        4) !HS, !HH: user needs to add security first, raise error
        """
        sec_id: str = holding.get_security().get_id()
        has_security: bool = self.contains_security(sec_id)
        has_holding: bool = self.contains_holding(sec_id)
        if has_security and not has_holding:
            self.__holdings[sec_id] = holding
            self.add_value(holding.get_value())
        elif not has_security:
            raise Exception(
                "add_holding(): Must add {} to '{}' before adding"
                " it as a holding.".format(sec_id, self.get_name())
            )
        else:
            raise Exception(
                "add_holding(): A holding for {} was already added"
                " to the '{}' asset class.".format(sec_id, self.get_name())
            )

    def update_security(
        self, security_id: str, name: str, price: float
    ) -> None:
        """
        Updates the given security with name and latest price data.
        """
        sec = self.get_security(security_id)
        sec.set_name(name)
        sec.set_price(price)

    def update_holding(
        self, security_id: str, num_shares: int, value: float
    ) -> None:
        """
        Updates the given holding with new holding data.
        """
        if self.contains_holding(security_id):
            # Already have a holding for this security -> update state
            hol: Holding = self.get_holding(security_id)
            old_hol_val: float = hol.get_value()
            hol.set_num_shares(num_shares)
            hol.set_value(value)
            self.add_value(-old_hol_val + value)
        elif self.contains_security(security_id):
            # Don't have holding for this security yet -> add as a new holding
            sec: Security = self.get_security(security_id)
            self.add_holding(Holding(sec, num_shares, value))
        else:
            raise Exception(
                "update_holding(): {} is not in the '{}' asset "
                "class's securities.".format(security_id, self.get_name())
            )

    def buy(self, security: Security, num_shares: int, dry_run: bool):
        """
        Adds num_shares of the given security to the holdings of this asset
        class. Returns the state of the buy transaction.
        """
        value: float = num_shares * security.get_price()
        self.add_value(value)
        sec_id: str = security.get_id()
        buy_holding: Holding = Holding(security, num_shares, value)
        if not self.contains_holding(sec_id):
            self.__holdings[sec_id] = buy_holding
        else:
            self.__holdings[sec_id].add(buy_holding)

        log.info(
            "Buy {n} {s} of {c} at {p} for a total of {t}? (Y/n) ".format(
                n=num_shares,
                s="shares" if num_shares > 1 else "share",
                c=security.get_symbol(),
                p=dollar_str(security.get_price()),
                t=dollar_str(value),
            )
        )
        if not dry_run:
            # Actually buy the ETFs
            user_choice: str = input("").lower()
            if user_choice in ["", "y"]:
                resp: Dict[str, Any] = r.order_buy_limit(
                    security.get_symbol(), num_shares, security.get_price()
                )
                if resp is None:
                    return "failed"
                else:
                    return resp["state"]
        else:
            return "confirmed"

    def plan_purchases(self, budget: float) -> Dict[str, Purchase]:
        """
        Uses a Dynamic Program to determine how to optimally spend the budget
        on the asset class's securities. This is the well known Unbounded
        Knapsack problem.
        """
        budget_cents: int = int(budget * 100)
        if budget_cents < 0:
            return {}

        securities_cents: Dict[str, Security] = dict(
            [
                (s.get_id(), s.with_cents())
                for s in self.get_securities()
                if not s.get_buy_restricted()
            ]
        )

        # Purchase at T[i] maximizes expenditure with budget i
        T: List[int] = [0 for x in range(budget_cents + 1)]
        for b_cents in range(budget_cents + 1):
            for j, (j_id, s_cents) in enumerate(securities_cents.items()):
                j_price_cents: int = s_cents.get_price()
                # Check if budget of b allows for a purchase of j
                if j_price_cents <= b_cents:
                    # Check if buying it increases expenditures
                    cur_exp: int = T[b_cents]
                    new_exp: int = T[b_cents - j_price_cents] + j_price_cents
                    if new_exp > cur_exp:
                        # Optimal purchases at budget i now includes buying j
                        T[b_cents] = new_exp

        # Backtrack thru T to construct set of optimal purchases
        purchases: Dict[str, Purchase] = {}
        i: int = len(T) - 1
        while T[i]:
            exp_i: int = T[i]  # Optimal amount spent at budget i
            # Find last security purchased
            for j, (j_id, sec_cents) in enumerate(securities_cents.items()):
                price_cents: int = sec_cents.get_price()
                # If buying security j brought us to optimal expenditures at
                # budget i
                if T[exp_i - price_cents] + price_cents == exp_i:
                    if j_id in purchases:
                        purchases[j_id].add_shares(1)
                    else:
                        purchases[j_id] = Purchase(self.get_security(j_id), 1)
                    break
            i = exp_i - securities_cents[j_id].get_price() + 1
        # Prune purchases of no shares from return value
        return dict(
            [(s, p) for (s, p) in purchases.items() if p.get_num_shares() != 0]
        )
