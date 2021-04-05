from reporter.config import config

class ReporterDatabase:
    def __init__(self, location: str = None):
        if location is None:
            location = config.data['postgresql']
