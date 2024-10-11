class UnSupportedPlatformError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    # def __str__(self):
    #     return repr(self.value)


class PreExistingInstallationError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    # def __str__(self):
    #     return repr(self.value)


class UnTestedPlatformError(Exception):
    # Constructor or Initializer
    def __init__(self, system, release):
        self.system = system
        self.release = release
        super().__init__(self.system)
        super().__init__(self.release)

    # __str__ is to print() the value

    # def __str__(self):
    #     return repr(self.system)


class InvalidDriveLetterError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    # def __str__(self):
    #    return repr(self.value)


class CreateSchemaError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    # def __str__(self):
    #    return repr(self.value)


class UnSupportedIPFSVersionError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    # def __str__(self):
    #    return repr(self.value)


class ApplicationNotInstalledError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
        super().__init__(self.value)

    # __str__ is to print() the value
    # def __str__(self):
    #    return repr(self.value)
