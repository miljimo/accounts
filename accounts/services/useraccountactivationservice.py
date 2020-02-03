from flask import request as Request, jsonify
from events import Event, EventHandler
from accounts.services.baseservice import BaseService
from accounts.databases.database import Database
from accounts.repositories.usercredentialrepository import UserCredentialRepository
from accounts.repositories.addressrepository import AddressRepository
from accounts.data.usercredential import UserCredential, CredentialStatusType
from accounts.errors.error import ErrorType
from accounts.repositories.userrepository import UserRepository, User


class ActivatedEvent(Event):
    def __init__(self, credential: UserCredential, activate_code: str):
        super().__init__("activate.data")
        if(isinstance(credential, UserCredential)) is not True:
            raise TypeError("@ActivateEvent: expecting parameter 1 to be a credential object.")
        self.__Credential  = credential
        self.__activatedCode  =  activate_code

    @property
    def ActivatedCode(self):
        return self.__activatedCode

    @property
    def Credential(self):
        return self.__Credential


class UserAccountActivationService(BaseService):

    def __init__(self, database: Database):
        super().__init__("user.account.activation.service", db=database)
        self.__Activated = EventHandler()

    @property
    def Activated(self):
        return self.__Activated

    @Activated.setter
    def Activated(self, handler):
        if handler == self.__Activated:
            self.__Activated = handler
        return self

    def Execute(self, request: Request) -> dict:
        response  = dict()
        response['success'] = False

        code                        = request.values.get('code','')
        user_uuid                   = request.values.get('user_id','')

        user_repo  = UserRepository(db=self.Database)
        user:User = user_repo.Get(user_uuid)

        if user is not None:
            credential_repo             = UserCredentialRepository(db= self.Database)
            credential                  = credential_repo.Get(user.UUID)

            if (credential is None) or (credential.ActivateCode != code):
                response['error_code'] = ErrorType.NOT_FOUND
            else:
                # make sure the user has not already activate the account.
                if credential.Status == CredentialStatusType.NORMAL:
                    # activate the account
                    credential.Status  = CredentialStatusType.ACTIVATED

                    status  = credential_repo.Update(credential.UserID, credential)

                    if status is True:
                        response['success'] = True
                        # raise and event to tell other part of the application.
                        if self.Activated is not None:
                            self.Activated(ActivatedEvent(credential, code))
                    else:
                        response['error_code'] = ErrorType.UPDATE_FAIL
                else:
                    errorcode = ErrorType.ACTIVATED_ALREADY if(credential.Status is not CredentialStatusType.BLOCKED) else ErrorType.USER_ACCOUNT_BLOCKED
                    response['error_code'] = errorcode
        else:
            response['error_code'] = ErrorType.NOT_FOUND

        self.Database.Close()
        return jsonify(response)

