import logging


class ImageBank:
    """Represents a bank of images, to avoid loading images multiple times"""

    instance = None

    @staticmethod
    def getInstance():
        if ImageBank.instance is None:
            ImageBank()
        return ImageBank.instance

    def __init__(self):
        if ImageBank.instance is not None:
            raise RuntimeError("Trying to instanciate second object from singleton class")
        ImageBank.instance = self

        self.images: {str: any} = {}

    def __getitem__(self, name: str):
        return self.images[name]

    def exists(self, name: str):
        return name in self.images.keys()

    def set(self, name: str, value):
        logging.debug(f"BANK: Registering {name}")
        self.images[name] = value
