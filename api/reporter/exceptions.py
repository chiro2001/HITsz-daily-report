class ReporterBaseError(Exception):
    def __init__(self, data):
        self.data = data


class ReporterPermissionError(ReporterBaseError):
    pass
