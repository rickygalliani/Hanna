# Ricky Galliani
# Hanna
# src/util.py


def dollar_str(amt):
    """
    Returns the given amount formatted as a string dollar amount.
    """
    return "${:,.2f}".format(amt)


def pct_str(pct):
    """
    Returns the given percentage formatted as a string.
    """
    return "{:.1%}".format(pct)


def latency_str(start, end):
    """
    Returns the given latency in milliseconds
    """
    latency = difference_in_millis(start, end)
    return "{:g} ms".format(float('{:.3g}'.format(latency)))


def difference_in_millis(start, end):
    """
    Returns the difference between start and end (datetime objects) in
    milliseconds.

    Original implementation found in this article:
    https://stackoverflow.com/
        questions/
        18426882/
        python-time-difference-in-milliseconds-not-working-for-me
    """
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis
