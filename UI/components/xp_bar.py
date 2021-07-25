from UI.components.loading_bar import LoadingBar


class XPBar(LoadingBar):
    def __init__(self, position: tuple, size: tuple):
        super.__init__(
            position,
            size,
            10
        )
