def fit(v, oldmin, oldmax, newmin=0.0, newmax=1.0):
    """
    Just a standard math fit/remap function
    Example:
    >>> fit(50, 0, 100, 0.0, 1.0)
    0.5
    """
    return (v - oldmin) * (newmax - newmin) / (oldmax - oldmin) + newmin
