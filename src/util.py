# Ricky Galliani
# Hanna
# src/util.py

def dollar_str(amt):
    """
    Returns the given amount formatted as a dollar amount.
    """
    return "${:,.2f}".format(amt)

def pct_str(pct):
    """
    Returns the given string formatted as a percentage.
    """
    return "{:.1%}".format(pct)