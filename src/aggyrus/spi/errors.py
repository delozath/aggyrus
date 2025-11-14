class IOProviderError(Exception):
    """
    Exception raised for errors in the IO provider from external libraries.
    """
    def __init__(self, message: str):
        print("IOProverderError raised: An error occurred in the IO provider and data could not be read.")
        super().__init__(message)


class BaseFilterError(Exception):
    """Base for all filtering-related errors."""

    def __init__(self, message, *, cause=None):
        self.cause = cause
        super().__init__(message)

    def __str__(self):
        s = "FilterDesignError raised: An error occurred during the filter design process.\n"
        s += super().__str__()
        return s



class FilterDesignError(BaseFilterError, ValueError):
    """
    Exception raised for errors in the filter design process.
    """
    def __init__(self, message: str):
        super().__init__(message)

class FilterInitializerError(BaseFilterError, ValueError):
    """
    Exception raised for errors in the filter design process.
    """
    def __init__(self, message: str):
        super().__init__(message)