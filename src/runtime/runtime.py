class FailureControl:
    def __init__(self, logger=None):
        if logger:
            self.logger = logger

    def report_failure(self, msg):
        self.logger.error("msg")