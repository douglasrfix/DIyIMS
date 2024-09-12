class UnSupportedPlatformError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


class PreExistingInstallationError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)


class UnTestedPlatformError(Exception):
    # Constructor or Initializer
    def __init__(self, system, release, dict):
        self.system = system
        self.release = release
        self.dict = dict
        super().__init__(self.system)
        super().__init__(self.release)
        super().__init__(self.dict)

    # __str__ is to print() the value

    def __str__(self):
        return repr(self.system)


"""
try:
    raise (UnsupportedPlatformError('darwin'))

# Value of Exception is stored in error
except UnsupportedPlatformError as error:
    print(error.value, "is not a supported platform")
"""
