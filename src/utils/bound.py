def bound(low: int, high: int, value: int) -> int:
    """Bounds a value between given limits"""
    return max(low, min(value, high))
