class Runnable:
    """A runnable class, with a hidden loop, callable"""

    def __init__(self):
        self.running: bool = False

    def __call__(self):
        self.run()

    def run(self):
        """Starts the loop"""
        self.running = True
        while self.running:
            self.loop()

    def loop(self):
        """Loop must be overriden in child class"""
        raise NotImplementedError()
