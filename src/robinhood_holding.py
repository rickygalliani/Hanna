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
        self.__id = holding_id
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__average_buy_price = average_buy_price
        self.__equity = equity
        self.__percentage = percentage
        self.__percent_change = percent_change
        self.__equity_change = equity_change
        self.__type = holding_type

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def get_average_buy_price(self):
        return self.__average_buy_price

    def get_equity(self):
        return self.__equity

    def get_percentage(self):
        return self.__percentage

    def get_percent_change(self):
        return self.__percent_change

    def get_equity_change(self):
        return self.__equity_change

    def get_type(self):
        return self.__type

    def __repr__(self):
        return json.__dumps({
            'id': self.get_id(),
            'name': self.get_name(),
            'price': self.get_price(),
            'quantity': self.get_quantity(),
            'average_buy_price': self.get_average_buy_price(),
            'equity': self.get_equity(),
            'percentage': self.get_percentage(),
            'percent_change': self.get_percent_change(),
            'equity_change': self.get_equity_change(),
            'type': self.get_type()
        })
