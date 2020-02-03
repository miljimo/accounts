
from accounts.validators.valuevalidator import ValueValidator
from accounts.validators.validator import EmailValidator, PhoneValidator, NamingValidator;
from accounts.data.user import User


class UserValidator(ValueValidator):

    def __init__(self):
        super().__init__("");
        self.__Validators = dict();
        self.Validators['email'] = EmailValidator();
        self.Validators['phone'] = PhoneValidator();
        namingValidator = NamingValidator();
        self.Validators['firstname'] = namingValidator;
        self.Validators['lastname'] = namingValidator;
        self.__Errors = None;

    @property
    def Errors(self):
        return self.__Errors;

    @property
    def Validators(self):
        return self.__Validators

    def Validate(self, user: User) ->bool:
        """
        :type user :User
        :param user:
        :return:
        """
        error = dict();
        for field in self.Validators:
            if field == 'email':
                if (self.Validators[field].Validate(user.Email)) is not True:
                    error[field] = False;
            elif field == 'firstname' :
                if (self.Validators[field].Validate(user.Firstname)) is not True:
                    error[field] = False;
            elif field == 'lastname':
                if (self.Validators[field].Validate(user.Lastname)) is not True:
                    error[field] = False;
            elif field == 'phone':
                if (self.Validators['phone'].Validate(user.PhoneNumber)) is not True:
                    error[field] = False;
        success  = (len(error) == 0);
        if success is not True:
            self.__Errors = error if (len(error) > 0) else None;
        return success;


if __name__ == "__main__":

    user = User(phone="07501348124", firstname='Obaro', lastname="Johnson", gender='mr',email='obaro.johnson@hotmail.com');
    validator = UserValidator();
    if (validator.Validate(user)) is not True:
        print(validator.Errors);
        print("Not validated")
    else:
        print("Validated : successful")
    print(user)
