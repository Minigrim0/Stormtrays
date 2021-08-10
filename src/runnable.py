import logging


class Runnable:
    """A runnable class, with a hidden loop, callable"""

    def __init__(self):
        self.running: bool = False

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)

    @staticmethod
    def _start(*args, **kwargs):
        """The method called before the runnable loop is launched"""
        logging.warning("Calling not implemented method _start")

    @staticmethod
    def _end():
        """The method called before the runnable loop ends"""
        logging.warning("Calling not implemented method _end")

    def run(self, *args, **kwargs):
        """Starts the loop"""
        self.running = True
        self._start(*args, **kwargs)
        while self.running:
            self.loop()
        self._end()

    @staticmethod
    def loop():
        """Loop must be overriden in child class"""
        raise NotImplementedError()
