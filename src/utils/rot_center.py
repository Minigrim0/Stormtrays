import pygame as pg


def rotCenter(image: pg.Surface, angle: float) -> pg.Surface:
    """Rotate an image on its center

    Args:
        image (pg.Surface): The image to rotate
        angle ([type]): the angle at which to rotate the image

    Returns:
        pg.Surface: The rotated image
    """
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
