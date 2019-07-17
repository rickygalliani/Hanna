# Ricky Galliani
# Hanna
# src/portfolio.py

from src.asset_class import AssetClass
from src.deposit import Deposit
from src.holding import Holding
from src.api import (
    AccountProfile,
    DividendInfo,
    HoldingInfo,
    SecurityInfo,
    load_account_profile,
    load_dividends,
    load_holdings,
    load_securities,
)
from src.purchase import Purchase
from src.security import Security
from src.util import latency_str, dollar_str, pct_str

from datetime import datetime
from prettytable import PrettyTable
from typing import Any, Dict, KeysView, List, Optional, Tuple, ValuesView

import json
import logging


log = logging.getLogger(__name__)


class Portfolio:
    def __init__(self) -> None:
        """
        Initializes a portfolio using a user-specified configuration.
        """
        self.__asset_classes: Dict[str, AssetClass] = {}
        self.__cash: float = 0.0

    def load_configuration(
        self, portfolio_config: List[Dict[str, Any]]
    ) -> None:
        """
        Loads the target investment portfolio (weights for asset classes and
        the securities underlying those asset classes) from the given config
        file.
        """
        total_target_pct: float = 0.0
        for a in portfolio_config:
            # Sanity check for portfolio config format
            assert "name" in a
            assert "target_percentage" in a
            assert "securities" in a
            assert "buy_restrictions" in a

            ac_name: str = a["name"]
            ac_target_pct: float = float(a["target_percentage"])
            ac_securities: List[str] = a["securities"]
            ac_buy_restrictions: List[str] = a["buy_restrictions"]

            for sec_id in ac_buy_restrictions:
                assert sec_id in ac_securities

            ac: AssetClass = (
                self.get_asset_class(ac_name)
                if self.contains_asset_class(ac_name)
                else AssetClass(ac_name, ac_target_pct)
            )
            ac.set_target_percentage(ac_target_pct)

            total_target_pct += ac_target_pct
            for s_id in ac_securities:
                buy_restricted: int = int(s_id in ac_buy_restrictions)
                s: Security = Security(s_id, buy_restricted=buy_restricted)
                if not ac.contains_security(s_id):
                    ac.add_security(s)
                else:
                    sec: Security = ac.get_security(s_id)
                    # Potentially update buy restriction status
                    if buy_restricted:
                        sec.restrict_buy()
                    else:
                        sec.enable_buy()
            if not self.contains_asset_class(ac_name):
                self.add_asset_class(ac)

        self.add_asset_class(AssetClass("Other", 0.0))

        if abs(total_target_pct - 1.0) >= 1e-9:
            raise Exception(
                "load_configuration(): asset class target percentages do not "
                "add up to 1."
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Portfolio):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict())

    def get_asset_class_names(self) -> KeysView[str]:
        return self.__asset_classes.keys()

    def get_asset_classes(self) -> ValuesView[AssetClass]:
        return self.__asset_classes.values()

    def get_cash(self) -> float:
        return self.__cash

    def get_value(self) -> float:
        return self.get_cash() + sum(
            [ac.get_value() for ac in self.get_asset_classes()]
        )

    def get_num_shares(self) -> int:
        return sum([ac.get_num_shares() for ac in self.get_asset_classes()])

    def set_cash(self, amount: float) -> None:
        self.__cash = amount

    def add_asset_class(self, asset_class) -> None:
        self.__asset_classes[asset_class.get_name()] = asset_class

    def to_dict(self) -> Dict[str, Any]:
        acs: List[Dict[str, Any]] = sorted(
            [(ac.to_dict()) for ac in self.get_asset_classes()],
            key=lambda ac_dict: ac_dict["name"],
        )
        return {"asset_classes": acs, "cash": self.get_cash()}

    def for_display(self) -> str:
        ac_cols: List[str] = [
            "Asset Class",
            "Target Percentage",
            "Percentage",
            "Cost",
            "Value",
            "Dividends",
            "Return",
        ]
        sec_cols: List[str] = [
            "Asset Class",
            "Security",
            "Symbol",
            "Restricted",
            "Average Price",
            "Price",
            "Shares",
            "Dividends",
            "Value",
            "Percentage",
            "Return",
        ]
        p_ac: PrettyTable = PrettyTable(ac_cols)
        p_sec: PrettyTable = PrettyTable(sec_cols)
        p_ac.title = "Portfolio Asset Classes"
        p_sec.title = "Portfolio Securities"
        acs: List[Tuple[AssetClass, float]] = [
            (ac, ac.get_value()) for ac in self.get_asset_classes()
        ]
        for ac, ac_value in sorted(acs, key=lambda x: x[1], reverse=True):
            ac_name: str = ac.get_name()
            p_ac.add_row(
                [
                    ac_name,
                    pct_str(ac.get_target_percentage()),
                    pct_str(self.get_asset_class_percentage(ac_name)),
                    dollar_str(ac.get_cost()),
                    dollar_str(ac_value),
                    dollar_str(ac.get_dividends()),
                    pct_str(ac.get_return()),
                ]
            )
            hs: List[Tuple[Holding, float]] = [
                (h, self.get_security_value(h.get_security().get_id()))
                for h in ac.get_holdings()
            ]
            for hol, hol_val in sorted(hs, key=lambda h: h[1], reverse=True):
                s: Security = hol.get_security()
                price: Optional[float] = s.get_price()
                price_str: str = dollar_str(price) if price is not None else ""
                p_sec.add_row(
                    [
                        ac_name,
                        s.get_name(),
                        s.get_symbol(),
                        "Yes" if s.get_buy_restricted() else "No",
                        dollar_str(hol.get_average_buy_price()),
                        price_str,
                        hol.get_num_shares(),
                        dollar_str(hol.get_dividends()),
                        dollar_str(hol_val),
                        pct_str(self.get_security_percentage(s.get_id())),
                        pct_str(hol.get_return()),
                    ]
                )
        portfolio_cash = dollar_str(self.get_cash())
        p_ac.add_row(
            [
                "Cash",
                "-",
                pct_str(self.get_cash_percentage()),
                portfolio_cash,
                portfolio_cash,
                dollar_str(0.0),
                pct_str(0.0),
            ]
        )
        portfolio_return_str = pct_str(self.get_return())
        p_ac.add_row(
            [
                "Total",
                "100%",
                pct_str(1),
                dollar_str(self.get_cost()),
                dollar_str(self.get_value()),
                dollar_str(self.get_dividends()),
                portfolio_return_str,
            ]
        )
        cash_str = dollar_str(self.get_cash())
        p_sec.add_row(
            [
                "Cash",
                "-",
                "-",
                "-",
                "-",
                cash_str,
                "-",
                dollar_str(0.0),
                cash_str,
                pct_str(self.get_cash_percentage()),
                pct_str(0.0),
            ]
        )
        p_sec.add_row(
            [
                "Total",
                "-",
                "-",
                "-",
                "-",
                "-",
                self.get_num_shares(),
                dollar_str(self.get_dividends()),
                dollar_str(self.get_value()),
                pct_str(1),
                portfolio_return_str,
            ]
        )
        return "\n{}\n{}".format(p_ac, p_sec)

    def get_all_security_ids(self) -> List[str]:
        """
        Returns the ids of all securities in the portfolio as a list of
        strings.
        """
        ids: List[str] = []
        for ac in self.get_asset_classes():
            for hol in ac.get_holdings():
                ids.append(hol.get_security().get_id())
        return ids

    def get_all_security_symbols(self) -> List[str]:
        """
        Returns the symbols of all securities in the portfolio as a list of
        strings.
        """
        symbols: List[str] = []
        for ac in self.get_asset_classes():
            for hol in ac.get_holdings():
                symbols.append(hol.get_security().get_symbol())
        return symbols

    def get_cost(self) -> float:
        """
        Computes and returns the cumulative cost of all investments in this
        portfolio.
        """
        return self.get_cash() + sum(
            [ac.get_cost() for ac in self.get_asset_classes()]
        )

    def get_dividends(self) -> float:
        """
        Returns the amount of dividends paid out for holdings in this
        portfolio.
        """
        return sum([ac.get_dividends() for ac in self.get_asset_classes()])

    def get_return(self) -> float:
        """
        Computes and returns the percent change of the investments in this
        portfolio.
        """
        value: float = self.get_value()
        cost: float = self.get_cost()
        dividends: float = self.get_dividends()
        return (value - cost + dividends) / cost

    def contains_asset_class(self, asset_class_name: str) -> bool:
        """
        Returns True if this portfolio contains an asset class with the given
        name.
        """
        return asset_class_name in self.get_asset_class_names()

    def contains_security(self, security_id: str) -> bool:
        """
        Returns whether the portfolio contains the given security.
        """
        return any(
            [
                a.contains_security(security_id)
                for a in self.get_asset_classes()
            ]
        )

    def get_asset_class(self, asset_class_name: str) -> AssetClass:
        """
        Retrieves the asset class instance with the given name.
        """
        if self.contains_asset_class(asset_class_name):
            return self.__asset_classes[asset_class_name]
        raise Exception(
            "Portfolio does not contain a '{}' asset class.".format(
                asset_class_name
            )
        )

    def get_asset_class_for_security(self, security_id: str) -> AssetClass:
        """
        Returns the asset class object containing the given security.
        """
        for ac in self.get_asset_classes():
            if ac.contains_security(security_id):
                return ac
        return self.get_asset_class("Other")

    def get_asset_class_value(self, asset_class_name: str) -> float:
        """
        Returns the value invested in the given asset class.
        """
        return self.get_asset_class(asset_class_name).get_value()

    def get_cash_percentage(self) -> float:
        """
        Returns the percentage of the portfolio value in cash.
        """
        total_value: float = self.get_value()
        if abs(total_value - 0 < 10e-9):
            return 0.0
        else:
            return 1.0 * self.get_cash() / total_value

    def get_asset_class_percentage(self, asset_class_name: str) -> float:
        """
        Returns the percentage of the portfolio invested in the given asset
        class.
        """
        total_value: float = self.get_value()
        if abs(total_value - 0 < 10e-9):
            return 0.0
        else:
            ac_value: float = self.get_asset_class_value(asset_class_name)
            return 1.0 * ac_value / total_value

    def get_security_value(self, security_id: str) -> float:
        """
        Returns the value invested in the given security.
        """
        ac: AssetClass = self.get_asset_class_for_security(security_id)
        return ac.get_holding(security_id).get_value()

    def get_security_percentage(self, security_id: str) -> float:
        """
        Returns the percentage of this portfolio invested in the given
        security.
        """
        return self.get_security_value(security_id) / self.get_value()

    def get_asset_class_target_value(
        self, asset_class_name: str, portfolio_value: float
    ) -> float:
        """
        Returns the amount that should be invested in the given asset class.
        """
        ac: AssetClass = self.get_asset_class(asset_class_name)
        return portfolio_value * ac.get_target_percentage()

    def get_asset_class_target_deviation(
        self, asset_class_name: str, portfolio_value: float
    ) -> float:
        """
        Returns the deviation between the target and the achieved amount
        invested in the given asset class.
        """
        ac: AssetClass = self.get_asset_class(asset_class_name)
        target: float = self.get_asset_class_target_value(
            asset_class_name, portfolio_value
        )
        return ac.get_value() - target

    def get_asset_class_budgets(
        self, deposit_amount: float
    ) -> Dict[str, float]:
        """
        Returns the spending budgets for the asset classes in the portfolio
        for a given deposit.
        """
        remaining_value: float = deposit_amount
        ac_budgets: Dict[str, float] = dict(
            [(ac.get_name(), 0.0) for ac in self.get_asset_classes()]
        )
        ac_devs: List[Tuple[str, float]] = []
        for ac in self.get_asset_classes():
            ac_name = ac.get_name()
            ac_dev = self.get_asset_class_target_deviation(
                ac.get_name(), self.get_value() + deposit_amount
            )
            ac_devs.append((ac_name, ac_dev))
        ac_devs.sort(key=lambda x: x[1])
        for (nm, ac_dev) in ac_devs:
            ac_budget: float = max(0, -1.0 * ac_dev)
            if ac_budget > remaining_value:
                ac_budget = remaining_value
            ac_budgets[nm] = ac_budget
            remaining_value -= ac_budget
        return ac_budgets

    def refresh(self, online: bool, logging: bool) -> None:
        """
        Hits the Robinhood API to pull fresh holding data for this portfolio.
        The internal state is changed by the in update() function.
        """
        s: datetime = datetime.now()
        account_profile: AccountProfile = load_account_profile(
            s, online, logging
        )
        holdings: Dict[str, HoldingInfo] = load_holdings(s, online, logging)
        security_ids: List[str] = list(holdings.keys())
        securities: Dict[str, SecurityInfo] = load_securities(
            security_ids, s, online, logging
        )
        dividends: Dict[str, DividendInfo] = load_dividends(
            security_ids, s, online, logging
        )
        e: datetime = datetime.now()
        self.update(account_profile, securities, holdings, dividends)
        log.info("Refreshed portfolio data. ({})".format(latency_str(s, e)))
        log.info("Portfolio:{}".format(self.for_display()))

    def update(
        self,
        account_profile: AccountProfile,
        securities: Dict[str, SecurityInfo],
        holdings: Dict[str, HoldingInfo],
        dividends: Dict[str, DividendInfo],
    ) -> None:
        """
        Updates this portfolio (and its underlying asset classes and
        securities).
        """
        cash: float = account_profile.get_buying_power()
        self.set_cash(cash)
        # Group securities that aren't defined in portfolio configuration in
        # "Other" asset class
        for sec_id in holdings.keys():
            # Extract refreshed data for this security
            hol_info: HoldingInfo = holdings[sec_id]
            sec_info: SecurityInfo = securities[sec_id]
            div_info: DividendInfo = dividends[sec_id]
            updated_shares: int = hol_info.get_quantity()
            updated_average_buy_price: float = (
                hol_info.get_average_buy_price()
            )
            updated_name: str = sec_info.get_name()
            updated_symbol: str = sec_info.get_symbol()
            updated_price: float = sec_info.get_price()
            updated_dividends: float = div_info.get_amount()

            # Update the state for this security
            ac: AssetClass = self.get_asset_class_for_security(sec_id)
            if not ac.contains_security(sec_id):
                ac.add_security(Security(sec_id))
            ac.update_security(
                sec_id, updated_symbol, updated_name, updated_price
            )
            ac.update_holding(
                sec_id,
                updated_shares,
                updated_average_buy_price,
                updated_dividends,
            )

    def plan_deposit(self, amount: float) -> Deposit:
        """
        Returns the optimal purchases to make with deposit added to this
        portfolio.
        """
        portfolio_cash = self.get_cash()
        deposit_budget = amount if portfolio_cash >= amount else portfolio_cash
        s: datetime = datetime.now()
        # Compute purchases necessary to rebalance portfolio
        deposit: Deposit = Deposit()
        budgets: List[Tuple[str, float]] = sorted(
            self.get_asset_class_budgets(deposit_budget).items(),
            key=lambda x: x[1],
            reverse=True,
        )
        # Rollover allocations not spent in previous classes
        rollover: float = 0.0
        for (ac_name, budget) in budgets:
            ac: AssetClass = self.get_asset_class(ac_name)
            final_budget: float = budget + rollover
            if (ac_name, budget) == budgets[-1]:
                final_budget -= ac.get_purchase_buffer()
            ac_purchases: Dict[str, Purchase] = ac.plan_purchases(final_budget)
            ac_total: float = 0.0
            for purchase in ac_purchases.values():
                deposit.add_purchase(ac_name, purchase)
                ac_total += purchase.get_cost()
            rollover = final_budget - ac_total
        e: datetime = datetime.now()
        log.info("Planned deposit. ({})".format(latency_str(s, e)))
        return deposit

    def make_deposit(self, deposit: Deposit, online: bool) -> None:
        """
        Makes all the purchases in the given deposit, updating the state of
        this portfolio.
        """
        if deposit.get_total() > self.get_cash():
            raise Exception("Deposit total is more than cash in portfolio.")
        log.info("Deposit:{}".format(deposit.for_display()))
        acs: List[Tuple[str, float]] = [
            (ac, deposit.get_asset_class_expenditures(ac))
            for ac in deposit.get_involved_asset_classes()
        ]
        sorted_acs: List[Tuple[str, float]] = sorted(
            acs, key=lambda x: x[1], reverse=True
        )
        for ac_name, _ in sorted_acs:
            ac: AssetClass = self.get_asset_class(ac_name)
            ps: List[Purchase] = deposit.get_purchases_for_asset_class(ac_name)
            purchases: List[Purchase] = sorted(
                ps, key=lambda x: x.get_cost(), reverse=True
            )
            for p in purchases:
                state: str = ac.buy(
                    p.get_security(), p.get_num_shares(), online
                )
                if state != "failed":
                    m: str = "\t- Trade Status: {}\n".format(
                        state.capitalize()
                    )
                    log.info(m)
                    self.set_cash(self.get_cash() - p.get_cost())
                else:
                    em: str = "\t- Trade Status: {}\n".format(
                        state.capitalize()
                    )
                    log.error(em)
