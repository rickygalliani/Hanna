# Ricky Galliani
# Hanna
# src/robinhood_holding.py

import json

class RobinhoodHolding:

    def __init__(self,
                 holding_id,
                 name,
                 price,
                 quantity,
                 average_buy_price,
                 equity,
                 percentage,
                 percent_change,
                 equity_change,
                 holding_type):
        self.id = holding_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.average_buy_price = average_buy_price
        self.equity = equity
        self.percentage = percentage
        self.percent_change = percent_change
        self.equity_change = equity_change
        self.type = holding_type

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'average_buy_price': self.average_buy_price,
            'equity': self.equity,
            'percentage': self.percentage,
            'percent_change': self.percent_change,
            'equity_change': self.equity_change,
            'type': self.type
        })