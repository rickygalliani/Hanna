# Ricky Galliani
# Hanna
# src/deposit.py

from src.purchase import Purchase

import json

class Deposit:

    def __init__(self):
        self.total = 0.0  # Total spent on all purchases in deposit
        self.purchases = {}

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
        out = ["\n\nRecommended Purchases:"]
        for asset_class_name, purchases in self.purchases.items():
            out.append("\n\n{}".format(asset_class_name))
            ac_total = 0.0
            for purchase in purchases:
                out.append(purchase.for_display())
                ac_total += purchase.total
            out.append(
                "\n\tAsset Class Expenditures: ${:,.2f}".format(ac_total)
            )
        out.append("\n\nTotal Expenditures: {}".format(round(self.total, 2)))
        return ''.join(out)

    def add_purchase(self, asset_class_name, purchase):
        """
        Adds purchases related to an asset class to this deposit.
        """
        if asset_class_name in self.purchases:
            self.purchases[asset_class_name] += [purchase]
        else:
            self.purchases[asset_class_name] = [purchase]
        self.total += purchase.total