import os
import sys
import glob
import math
import json
import pygame as pg


def best_geometry(size: int) -> tuple[int, int]:
    x = round(math.sqrt(size))
    y = x
    if x ** 2 < size:
        x += 1
    return x, y


def get_geom(size) -> tuple[int, int]:
    geom_x, geom_y = best_geometry(len(file_paths))

    print(f"Is {geom_x}x{geom_y} a correct geometry for the new tileset ?")
    ok = not input("(Y/n) > ").lower() == "n"
    if ok:
        return geom_x, geom_y

    while not ok:
        print("Please enter the new geometry as '<X value>x<Y value>'")
        new_value = input("> ")
        if "x" not in new_value or new_value.count("x") > 1:
            continue
        geom_x, geom_y = new_value.split("x")
        if geom_x.isdigit() and geom_y.isdigit():
            ok = not input(f"Confirm the new geometry {geom_x}x{geom_y} ? (Y/n) > ").lower() == "n"
        else:
            ok = False
            print("The value you have entered is incorrect !")

    return int(geom_x), int(geom_y)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {__file__} <path to tile folder>")
    path = sys.argv[1]

    file_paths = glob.glob(os.path.join(path, "*.png"))
    print(f"Found {len(file_paths)} file(s)")

    geom_x, geom_y = get_geom(len(file_paths))
    reference_size: tuple[int, int] = None
    final_image: pg.Surface = None

    pg.init()
    pg.display.set_mode((10, 10))

    meta = {}

    for index, image_path in enumerate(file_paths):
        image_name = os.path.split(image_path)[1]
        current_image = pg.image.load(image_path).convert_alpha()
        if reference_size is None:
            reference_size = current_image.get_size()
            final_image = pg.Surface(
                (geom_x * reference_size[0], geom_y * reference_size[1]),
                pg.SRCALPHA
            )
            print(f"Created final image with reference size: {final_image.get_size()}")
        elif current_image.get_size() != reference_size:
            raise RuntimeError(
                f"Image sizes differ ! (ref={reference_size}, current={current_image.get_size()})"
            )

        x_pos = (index % geom_x) * reference_size[0]
        y_pos = (index // geom_x) * reference_size[1]
        print(x_pos, y_pos)
        meta[image_name] = [x_pos, y_pos]

        final_image.blit(current_image, (x_pos, y_pos))

    pg.image.save(final_image, os.path.join(path, "tileset.png"))
    with open(os.path.join(path, "tileset.json"), "w+") as f:
        json.dump(meta, f)
