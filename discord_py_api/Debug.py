import time


class Debug:
    INFO = "INFO"
    DEBUG = "DEBUG"

    def __init__(self, debug: bool):
        self.debug = debug
        self.start_time = time.time()

    def message(self, level: str, message: str):
        if self.debug is None:
            return

        elif level == self.INFO:
            print(f"[{(time.time() - self.start_time):.3f}] [{level}]: {message}")
            return

        elif not self.debug:
            return

        print(f"[{(time.time() - self.start_time):.3f}] [{level}]: {message}")
