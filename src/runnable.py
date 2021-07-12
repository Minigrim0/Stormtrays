class Runnable:
    def __init__(self):
        self.running: bool = False

    def __call__(self):
        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.loop()

    def loop(self):
        raise NotImplementedError()
