from math import pi, atan


def findAngle(delta_x: int, delta_y: int):
    """Returns the angle from the right-angle
    triangle formed by side of the given sizes

    Args:
        delta_x (int): the size of the x side
        delta_y (int): the size of the y side

    Returns:
        float: the angle in degrees of the trangle's corner
    """

    if delta_x != 0:
        angle = atan(delta_y / delta_x)
    elif delta_y < 0:
        angle = -pi / 2
    else:
        angle = pi / 2

    if delta_x < 0:
        angle = angle + pi

    return angle
