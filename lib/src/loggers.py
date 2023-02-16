class NoLogger:
    def debug(self, message):
        pass

    def info(self, message):
        pass


class InfoLogger:
    def debug(self, message):
        pass

    def info(self, message):
        print("INF:", message)


class DebugLogger(InfoLogger):
    def debug(self, message):
        print("DBG:", message)
