from models.screen import Screen


class LoadingBar:
    """A loading bar"""

    def __init__(self, pos: tuple, size: tuple):
        self.position = pos
        self.size = size
        self.advancement = 0

    def set_advancement(self, advancement: int):
        """Sets the advancement of the loading"""
        self.advancement = advancement

    def update(self, timeElapsed: int):
        """Updates the bar according to its advancement"""
        pass

    def draw(self, screen: Screen):
        """Draws the bar on the screen"""
        pass
