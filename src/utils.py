from math import pi, atan, floor

import pygame


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


def rot_center(image: pygame.Surface, angle: float):
    """Rotate an image on its center

    Args:
        image (pygame.Surface): The image to rotate
        angle ([type]): the angle at which to rotate the image

    Returns:
        pygame.Surface: The rotated image
    """
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def ConvertToHMS(secs: int):
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
