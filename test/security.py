# Ricky Galliani
# Hanna
# test/security.py

from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.security

class SecurityTest(unittest.TestCase):

    def test_with_cents(self):
        sec1 = Security('sec1', price=167).with_cents()
        self.assertEqual(sec1.price, 16700)

    def test_update(self):
        pass

if __name__ == '__main__':
    unittest.main()