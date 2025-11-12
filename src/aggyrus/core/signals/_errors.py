
class NoSegmentsDefinedError(ValueError):
    """
    Raised when no segments are defined in a time series record.
    """
    def __init__(self, message: str):
        print("At least one segment must be defined in the time series record.")
        super().__init__(message)