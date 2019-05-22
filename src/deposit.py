# Ricky Galliani
# Hanna
# src/deposit.py

from src.util import dollar_str, pct_str

from prettytable import PrettyTable

import json


class Deposit:

    def __init__(self):
        self.__total = 0.0  # Total spent on all purchases
        self.__num_shares = 0  # Total shares bought on all purchases
        self.__purchases = {}

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_total(self):
        return self.__total

    def get_num_shares(self):
        return self.__num_shares

    def get_purchases(self):
        return self.__purchases

    def get_involved_asset_classes(self):
        return self.get_purchases().keys()

    def to_dict(self):
        return {
            'total': self.get_total(),
            'num_shares': self.get_num_shares(),
            'purchases': self.get_purchases()
        }

    def for_display(self):
        p_ac = PrettyTable(['Asset Class', 'Expenditures'])
        p_sec = PrettyTable([
            'Asset Class',
            'Security',
            'Symbol',
            'Shares',
            'Price',
            'Cost'
        ])
        p_ac.title = 'Expenditures per Asset Class'
        p_sec.title = 'Purchases'
        sec_tot_value = 0.0
        sec_tot_shares = 0
        acs = [
            (ac, self.get_asset_class_expenditures(ac))
            for ac in self.get_involved_asset_classes()
        ]
        sorted_acs = sorted(acs, key=lambda x: x[1], reverse=True)
        for ac_name, ac_exp in sorted_acs:
            p_ac.add_row([ac_name, dollar_str(ac_exp)])
            ps = [
                (p, p.get_cost())
                for p in self.get_purchases_for_asset_class(ac_name)
            ]
            sorted_ps = sorted(ps, key=lambda x: x[1], reverse=True)
            for p, p_cost in sorted_ps:
                sec = p.get_security()
                name = sec.get_name()
                sym = sec.get_symbol()
                shares = p.get_num_shares()
                price = dollar_str(sec.get_price())
                cost = dollar_str(p_cost)
                p_sec.add_row([ac_name, name, sym, shares, price, cost])
        p_ac.add_row(['Total', dollar_str(self.get_total())])
        tot_shares = self.get_num_shares()
        tot_cost = self.get_total()
        p_sec.add_row(
            ['Total', '-', '-', tot_shares, '-', dollar_str(tot_cost)]
        )
        return "\n{}\n{}".format(p_ac, p_sec)

    def add_purchase(self, asset_class_name, purchase):
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

    def involves_asset_class(self, asset_class_name):
        """
        Returns whether this deposit involves purchases made in the given
        asset class.
        """
        return asset_class_name in self.get_involved_asset_classes()

    def get_purchases_for_asset_class(self, asset_class_name):
        """
        Returns the purchases to be made for the given asset class for this
        deposit.
        """
        if self.involves_asset_class(asset_class_name):
            return self.get_purchases()[asset_class_name]
        raise Exception(
            "Deposit does not involve asset class {}.".format(asset_class_name)
        )

    def get_asset_class_expenditures(self, asset_class_name):
        """
        Returns the total expenditures in the given asset class.
        """
        ps = self.get_purchases_for_asset_class(asset_class_name)
        return sum(p.get_cost() for p in ps)
