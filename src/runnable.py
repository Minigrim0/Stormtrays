class Runnable:
    """A runnable class, with a hidden loop, callable"""

    def __init__(self):
        self.running: bool = False

    def __call__(self):
        self.run()

    def _end(self):
        pass

    def run(self):
        """Starts the loop"""
        self.running = True
        while self.running:
            self.loop()
        self._end()

    def loop(self):
        """Loop must be overriden in child class"""
        raise NotImplementedError()
