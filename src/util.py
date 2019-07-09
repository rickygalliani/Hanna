# Ricky Galliani
# Hanna
# src/util.py


from datetime import datetime, timedelta

import os


def dollar_str(amt: float) -> str:
    """
    Returns the given amount formatted as a string dollar amount.
    """
    return "${:,.2f}".format(amt)


def pct_str(pct: float) -> str:
    """
    Returns the given percentage formatted as a string.
    """
    return "{:.1%}".format(pct)


def latency_str(start: datetime, end: datetime) -> str:
    """
    Returns the given latency in milliseconds
    """
    latency: float = difference_in_millis(start, end)
    return "{:g} ms".format(float("{:.3g}".format(latency)))


def difference_in_millis(start: datetime, end: datetime) -> float:
    """
    Returns the difference between start and end (datetime objects) in
    milliseconds.

    Original implementation found in this article:
    https://stackoverflow.com/
        questions/
        18426882/
        python-time-difference-in-milliseconds-not-working-for-me
    """
    diff: timedelta = end - start
    millis: float = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis


def latest_ds(base_path: str) -> str:
    """
    Returns the latest date partitioned string under the base path.
    """
    latest = str(max(os.listdir(base_path)))
    if ".json" in latest:
        return ""
    next_component = latest_ds(os.path.join(base_path, latest))
    if next_component != "":
        return os.path.join(latest, next_component)
    else:
        return latest
