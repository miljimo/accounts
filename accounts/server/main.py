from flask import Flask, request, jsonify
import copy
from accounts.errors.error import ErrorType
from accounts.loggers.logger import BaseLogger
from accounts.repositories.userrepository import UserRepository
from accounts.services.useraccountactivationservice import UserAccountActivationService
from accounts.services.userrecordsservice import UserRecordsService
from accounts.services.userregistrationservice import UserRegistrationService
from accounts.databases.database import Database
from accounts.services.userauthservice import UserAuthService
from accounts.repositories.usercredentialrepository import UserCredentialRepository
from accounts.data.usercredential import CredentialStatusType, UserCredential
from accounts.repositories.administrationlevelrepository import AdministratorLevelRepository, AdminLevelStatusType, AdminLevelType
from events import Event, EventHandler
from accounts.services.administrationassignmentservice import AdministrationAssignmentService

DATABASE_URL = 'dbtest.db'


class UserAdminLevelUpdatedEvent(Event):

    def __init__(self, old_user_level, new_user_level):
        super().__init__("user.admin.level.updated")
        self.__OldUserLevel = old_user_level
        self.__NewUserLevel = new_user_level

    @property
    def OldValue(self):
        return self.__OldUserLevel

    @property
    def NewValue(self):
        return self.__NewUserLevel


FILE_LOGGER_LOCATION = "../../logs/account.log"


class WebRouting(object):

    def Attach(self, app):
        app.add_url_rule('/api/{0}/user/account'.format(self.Version),
                          view_func=self.CreateUserAccount,
                          methods=['POST', 'GET']);
        
        app.add_url_rule("/api/{0}/user/account/activate".format(self.Version), methods=['GET', 'POST'],
                          view_func=self.ActivateUserAccount)
        
        app.add_url_rule('/api/{0}/user/account/login'.format(self.Version), methods=['Get', 'POST'],
                          view_func=self.AuthenticateUserCredential)
        app.add_url_rule("/api/{0}/user/accounts".format(self.Version), methods=['GET', 'POST'],
                          view_func=self.GetAllUsers)

        app.add_url_rule("/api/{0}/admin/level".format(self.Version), methods=['post', 'get'],
                          view_func=self.AssignAdministrationLevel)
        
        pass;
        
class UserAccountServer(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__Version = "v1"
        self.config["DEBUG"]= True
        self.__Logger = BaseLogger(filename  = FILE_LOGGER_LOCATION)
        self.Logger.Info("Application server started.")
        self.Logger.Info("Start registering url rules")
        

        # errors
        self.register_error_handler(404, self.PageNotFound)
        self.Logger.Info("Application started.")


    @property
    def Logger(self):
        return self.__Logger

    def AssignAdministrationLevel(self):
        service  = AdministrationAssignmentService(database=Database(DATABASE_URL), logger=self.Logger)
        return service.Execute(request)

    def GetAllUsers(self) -> object:
        service  =  UserRecordsService(Database(name=DATABASE_URL),logger=self.Logger)
        return service.Execute(request)

    def AuthenticateUserCredential(self):
        service = UserAuthService(Database(name=DATABASE_URL))
        return service.Execute(request)

    @property
    def Version(self):
        return self.__Version

    def PageNotFound(self, error):
        response = dict()
        response['success'] = False
        response['error'] = "unknown request , please read the api documentations"
        return jsonify(response)
        pass;

    def ActivateUserAccount(self) -> object:
        service = UserAccountActivationService(Database(name=DATABASE_URL))
        return service.Execute(request)

    def CreateUserAccount(self) -> object:
        service = UserRegistrationService(Database(name=DATABASE_URL))
        return service.Execute(request)


if __name__ == "__main__":
    app = UserAccountServer(__name__)
    app.run()
