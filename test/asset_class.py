# Ricky Galliani
# Hanna
# test/asset_class.py

from src.asset_class import AssetClass
from src.robinhood_holding import RobinhoodHolding
from src.security import Security

import unittest

# Usage: python -m unittest --verbose test.asset_class

class AssetClassTest(unittest.TestCase):

    def test_add_security(self):
        ac = AssetClass('ac', target_percentage=1.0)

        # Add security without specified holdings
        sec1 = Security('sec1')
        ac.add_security(sec1)
        self.assertEqual(ac.securities[sec1.id], sec1)
        self.assertEqual(ac.holdings, 0.0)
        
        # Add security with specified holdings
        sec2 = Security('sec2', price=10.0, quantity=3, holdings=30.0)
        ac.add_security(sec2)
        self.assertEqual(ac.securities[sec2.id], sec2)
        self.assertEqual(ac.holdings, 30.0)

    def test_update_1(self):
        rh = RobinhoodHolding(
            holding_id='sec1',
            name='sec1_name',
            price=40.0,
            quantity=1,
            average_buy_price=40.0,
            equity=40.0,
            percentage=40.0,
            percent_change=0.0,
            equity_change=0.0,
            holding_type='etp'
        )
        ac = AssetClass('ac1', target_percentage=0.5)
        sec1 = Security('sec1')     
        ac.add_security(sec1)
        ac.update(rh)
        self.assertEqual(ac.holdings, rh.equity)
        self.assertEqual(ac.securities['sec1'], sec1)

    def test_update(self):
        pass

if __name__ == '__main__':
    unittest.main()