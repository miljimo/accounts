import re


class IValueValidator(object):
    def Validate(self, value):
        raise NotImplementedError("@Validate: method must be implemented before used.")


class ValueValidator(IValueValidator):
    def __init__(self, pattern: str):
        if type(pattern) != str:
            raise TypeError("Expecting a string of reg pattern")
        self.__Pattern = pattern

    @property
    def Pattern(self):
        return self.__Pattern

    def Validate(self, value: str, **kwargs):
        status = False
        if type(value) == str:
            program = re.compile(self.Pattern, re.UNICODE)
            result = program.match(value)
            if result is not None:
                group = result.group(0)
                if group == value:
                    status = True
        return status


if __name__ == "__main__":
    validator = ValueValidator("^([a-zA-Z0-9]+)")
    if (validator.Validate("Johnson")) is True:
        print("Hello World")
