class IOProviderError(Exception):
    """
    Exception raised for errors in the IO provider from external libraries.
    """
    def __init__(self, message: str):
        print("IOProverderError raised: An error occurred in the IO provider and data could not be read.")
        super().__init__(message)
