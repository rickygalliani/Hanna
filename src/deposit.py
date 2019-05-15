# Ricky Galliani
# Hanna
# src/deposit.py

from prettytable import PrettyTable

import json


class Deposit:

    def __init__(self):
        self.total = 0.0  # Total spent on all purchases in deposit
        self.purchases = {}

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'purchases': dict(
                [(ac, [p.to_dict() for p in ps])
                 for (ac, ps) in self.purchases.items()]
            )
        }

    def for_display(self):
        p_ac = PrettyTable(['Asset Class', 'Expenditures'])
        p_sec = PrettyTable([
            'Asset Class',
            'Security',
            'Shares',
            'Price',
            'Cost'
        ])
        sorted_acs = sorted(
            self.purchases.items(),
            key=lambda x: self.get_asset_class_expenditures(x[0]),
            reverse=True
        )
        for ac_name, purchases in sorted_acs:
            exp = "${:,.2f}".format(self.get_asset_class_expenditures(ac_name))
            p_ac.add_row([ac_name, exp])
            sorted_ps = sorted(purchases, key=lambda x: x.cost, reverse=True)
            for purchase in sorted_ps:
                name = purchase.security_name
                shares = purchase.num_shares
                price = "${:,.2f}".format(purchase.price)
                cost = "${:,.2f}".format(purchase.num_shares * purchase.price)
                p_sec.add_row([ac_name, name, shares, price, cost])
        return "\n{}\n{}".format(p_ac, p_sec)

    def add_purchase(self, asset_class_name, purchase):
        """
        Adds purchases related to an asset class to this deposit.
        """
        if asset_class_name in self.purchases:
            self.purchases[asset_class_name] += [purchase]
        else:
            self.purchases[asset_class_name] = [purchase]
        self.total += purchase.cost

    def get_asset_class_expenditures(self, asset_class_name):
        """
        Returns the total expenditures in the given asset class.
        """
        ps = self.purchases[asset_class_name]
        return sum(p.cost for p in ps)
