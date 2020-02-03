import re;
from accounts.validators.valuevalidator import ValueValidator;


class EmailValidator(ValueValidator):
    def __init__(self):
        super().__init__("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)");


class UKPostcodeValidator(ValueValidator):
    def __init__(self):
        super().__init__(
            "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})");


class ZipCodeValidator(ValueValidator):
    def __init__(self):
        super().__init__("^\d{5}(?:[-\s]\d{4})?$");


class PhoneValidator(ValueValidator):

    def __init__(self):
        super().__init__("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$");


class NamingValidator(ValueValidator):

    def __init__(self):
        super().__init__("^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$");


class NumberValidator(ValueValidator):
    def __init__(self):
        super().__init__("^([0-9]+)(([\.]{1})([09]{1,})$");


if __name__ == "__main__":
    email = EmailValidator();
    print(email.Validate("obaro_90.johnson@hotmail.com"));
    phone = PhoneValidator();
    print(phone.Validate("+447501358124"));
    ukpostcode = UKPostcodeValidator();
    print(ukpostcode.Validate("TW7 3JL"));
    naming = NamingValidator();
    print(naming.Validate("Obaro Johnson", number_of_match=1));
