import math


def distance_between(p1: tuple, p2: tuple):
    """Returns the distance between two 2D points"""
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
