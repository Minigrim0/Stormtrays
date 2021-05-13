from math import pi, atan


def findAngle(delta_x, delta_y):
    if delta_x != 0:
        angle = atan(delta_y / delta_x)
    elif delta_y < 0:
        angle = -pi / 2
    else:
        angle = pi / 2

    if delta_x < 0:
        angle = angle + pi

    return angle
