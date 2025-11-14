#[#IO Provider Errors]
class BaseIOProviderError(Exception):
    """Base for all IO provider-related errors."""
    def __init__(self, message, *, cause=None):
        self.cause = cause
        super().__init__(message)

    def __str__(self):
        s = "IOProviderError raised: An error occurred in the IO provider and data could not be read.\n"
        s += super().__str__()
        return s

class IOProviderReadError(BaseIOProviderError, IOError):
    """
    Exception raised for errors in reading data from an IO provider.
    """
    def __init__(self, message: str):
        message += " IOProviderReadError: An error occurred while reading data from the IO provider."
        super().__init__(message)


#[Filter Errors]
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
        message += " FilterDesignError: An error occurred during the filter design process."
        super().__init__(message)

class FilterInitializerError(BaseFilterError, ValueError):
    """
    Exception raised for errors in the filter design process.
    """
    def __init__(self, message: str):
        message += " FilterInitializerError: An error occurred during filter initialization."
        super().__init__(message)

class FilterNotDesignedError(BaseFilterError, ValueError):
    """
    Exception raised when attempting to apply a filter that has not been designed yet.
    """
    def __init__(self, message: str):
        message += " FilterNotDesignedError: The filter has not been designed yet."
        super().__init__(message)

class FilterApplyModeError(BaseFilterError, ValueError):
    """
    Exception raised when an invalid mode is specified for filter application.
    """
    def __init__(self, message: str):
        message += " FilterApplyModeError: An invalid mode was specified for filter application."
        super().__init__(message)