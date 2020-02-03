import flask
import datetime as dt
from events import EventHandler, Event;
from accounts.errors.error import ErrorType
from accounts.services.baseservice import BaseService
from accounts.databases.database import Database
from accounts.data.user import User
from accounts.data.userlevel import UserLevel, AdminLevelStatusType, AdminLevelType
from accounts.data.usercredential import UserCredential
from accounts.validators.uservalidator import UserValidator
from accounts.repositories.usercredentialrepository import UserCredentialRepository
from accounts.repositories.userrepository import UserRepository
from accounts.repositories.administrationlevelrepository import AdministratorLevelRepository


class UserCreatedEvent(Event):

    def __init__(self, user: User, credential: UserCredential):
        super().__init__('user.created.event')
        self.__User = user
        self.__Credential  = credential

    @property
    def Credential(self):
        return self.__Credential

    @property
    def User(self):
        return self.__User


class CredentialCreatedEvent(Event):

    def __init__(self, credential: UserCredential):
        super().__init__("user.credential.created.event")
        self.__Credential  =  credential

    @property
    def Credential(self):
        return self.__Credential


class UserRegistrationService(BaseService):

    def __init__(self, database):
        super().__init__("register_service", db=database)
        self.UserCreated        = EventHandler()
        self.CredentialCreated  = EventHandler()
        #   register events
        self.UserCreated        += self.OnUserCreate
        self.CredentialCreated  += self.OnCredentialCreated



    def OnCredentialCreated(self, event: CredentialCreatedEvent) -> None:
        '''
        :param event:
        :return:
        '''
        if isinstance(event, CredentialCreatedEvent) is not None:
            user_level_repo =  AdministratorLevelRepository(db=self.Database)
            if(user_level_repo.Exists(event.Credential.UserID)) is not True:
                expire_date  =  dt.datetime.now() + dt.timedelta(days=365)
                level  = UserLevel(user_uuid=event.Credential.UserID,
                                    status= AdminLevelStatusType.NORMAL,
                                    admin_level= AdminLevelType.SITE_USERS_LEVEL,
                                    expire_date=expire_date,
                                    assigned_date= dt.datetime.now())
                result  = user_level_repo.Create(event.Credential.UserID, level)
                if result is not None:
                    self.Status  = True


    def OnUserCreate(self, created_event: UserCreatedEvent) -> None:
        credential  = created_event.Credential
        user        = created_event.User

        if isinstance(credential, UserCredential) is not None:
            repo_credential = UserCredentialRepository(db= self.Database)
            if repo_credential.Exists(user.UUID) is not True:
                result_credential = repo_credential.Create(user.UUID, credential)
                if result_credential is not None:
                    user.Credential = result_credential
                    if self.CredentialCreated is not None:
                        self.CredentialCreated(CredentialCreatedEvent(credential))

    def Execute(self, request: flask.request) -> dict:
        """
         :param kwargs:
         :return:  dict
         """
        self.Status = False
        response = dict()
        response['success'] = False
        response['error_code'] = ErrorType.NORMAL

        email    = request.values.get("email", "").lower()
        password = request.values.get('password', 'admin')
        gender = request.values.get("gender", 'male')
        firstname = request.values.get('firstname', '')
        lastname = request.values.get('lastname', '')
        title = request.values.get('title')
        phone = request.values.get('phone')
        user = User(email=email, gender=gender, firstname=firstname, lastname=lastname, title=title, phone=phone)

        # validation of user inputs here
        validator = UserValidator()
        if (validator.Validate(user)) is True:
            # Validation passed  now user account verification to make sure the sure is not create multi-times.
            user_repo = UserRepository(db=self.Database)
            if user_repo.Exists(user.Email) is not True:
                result_user = user_repo.Create(user)
                if result_user is not None:
                    default_password    = self.GetHash(password)
                    credential          = UserCredential(user_uuid=result_user.UUID, password=default_password)

                    if self.UserCreated is not None :
                        event: UserCreatedEvent  = UserCreatedEvent(result_user, credential)
                        self.UserCreated(event)
                        response['success'] = True
                        response['user'] = dict()
                        response['user']['uuid'] = result_user.UUID
                        response['user']['create_date'] = result_user.DateRegistered
                else:
                    response['error_code'] = ErrorType.UNABLE_TO_CREATE_USER_ERROR
            else:
                response['error_code'] = ErrorType.USER_ALREADY_EXISTS_ERROR

        if response['success'] is True:
            # process successful response
            del response['error_code']
            pass;
        else:
            # process un-successful response
            pass;

        if self.Status is not True:
            self.Database.RollBack()
            response['success'] = False
        self.Database.Close()
        return flask.jsonify(response)


    def __del__(self):
        self.UserCreated -= self.OnUserCreate
        self.CredentialCreated -= self.OnCredentialCreated


if __name__ == "__main__":
    service  = UserRegistrationService(Database(name="dbtest.db"))
