# Ricky Galliani
# Hanna
# src/deposit.py

from prettytable import PrettyTable

import json


class Deposit:

    def __init__(self):
        self.__total = 0.0  # Total spent on all purchases in deposit
        self.__purchases = {}

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_total(self):
        return self.__total

    def get_purchases(self):
        return self.__purchases

    def get_involved_asset_classes(self):
        return self.get_purchases().keys()

    def to_dict(self):
        return {'total': self.get_total(), 'purchases': self.get_purchases()}

    def for_display(self):
        p_ac = PrettyTable(['Asset Class', 'Expenditures'])
        p_sec = PrettyTable([
            'Asset Class',
            'Security',
            'Shares',
            'Price',
            'Cost'
        ])
        p_ac.title = 'Expenditures per Asset Class'
        p_sec.title = 'Purchases'
        sec_total = 0.0
        acs = [
            (ac, self.get_asset_class_expenditures(ac))
            for ac in self.get_involved_asset_classes()
        ]
        sorted_acs = sorted(acs, key=lambda x: x[1], reverse=True)
        for ac_name, ac_exp in sorted_acs:
            exp = "${:,.2f}".format(ac_exp)
            p_ac.add_row([ac_name, exp])
            ps = self.get_purchases_for_asset_class(ac_name)
            sorted_ps = sorted(ps, key=lambda x: x.get_cost(), reverse=True)
            for purchase in sorted_ps:
                p_cost = purchase.get_cost()
                sec_total += p_cost
                name = purchase.get_security_name()
                shares = purchase.get_num_shares()
                price = "${:,.2f}".format(purchase.get_price())
                cost = "${:,.2f}".format(p_cost)
                p_sec.add_row([ac_name, name, shares, price, cost])
        p_ac.add_row(['Total', "${:,.2f}".format(self.get_total())])
        p_sec.add_row(['Total', '-', '-', '-', "${:,.2f}".format(sec_total)])
        return "\n{}\n{}".format(p_ac, p_sec)

    def add_purchase(self, asset_class_name, purchase):
        if self.involves_asset_class(asset_class_name):
            self.__purchases[asset_class_name] += [purchase]
        else:
            self.__purchases[asset_class_name] = [purchase]
        self.__total += purchase.get_cost()

    def involves_asset_class(self, asset_class_name):
        return asset_class_name in self.get_involved_asset_classes()

    def get_purchases_for_asset_class(self, asset_class_name):
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
