class UnsupportedPlatformError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


class PreexistingInstallationError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


"""
try:
    raise (UnsupportedPlatformError('darwin'))

# Value of Exception is stored in error
except UnsupportedPlatformError as error:
    print(error.value, "is not a supported platform")
"""
