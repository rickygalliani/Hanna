#!/usr/bin/env bash

python3 -m unittest --verbose test.security;
python3 -m unittest --verbose test.holding;
python3 -m unittest --verbose test.asset_class;
python3 -m unittest --verbose test.portfolio;
python3 -m unittest --verbose test.purchase;
python3 -m unittest --verbose test.deposit;
python3 -m unittest --verbose test.util;