class Logger:
    """message -> earliest timestamp at which it may print again.
    One dict lookup + one comparison per call; the timer only resets
    when the message actually prints."""

    def __init__(self):
        self.next_ok = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if timestamp < self.next_ok.get(message, 0):
            return False
        self.next_ok[message] = timestamp + 10
        return True
