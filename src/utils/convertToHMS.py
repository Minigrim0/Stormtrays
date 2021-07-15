from math import floor


def convertToHMS(secs: int):
    """Converts a timestamps in hour minutes and seconds

    Args:
        secs (int): [description]

    Returns:
        [type]: [description]
    """
    M = floor(secs / 60)
    S = floor(secs % 60)
    H = floor(M / 60)
    M = floor(M % 60)

    tab = [H, M, S]

    return tab
