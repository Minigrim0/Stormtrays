class TowerUI:
    """Represents the small UI appearing when a tower is selected"""

    instance = None

    @staticmethod
    def getInstance():
        if TowerUI.instance is None:
            TowerUI()
        return TowerUI.instance

    def __init__(self):
        pass
