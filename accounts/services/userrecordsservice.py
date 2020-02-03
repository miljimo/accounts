from flask import jsonify, request as Request
from accounts.data.user import User
from accounts.errors.error import ErrorType
from accounts.repositories.userrepository import UserRepository
from accounts.databases.database import Database
from accounts.repositories.usercredentialrepository import UserCredentialRepository
from accounts.services.baseservice import BaseService
from accounts.data.usercredential import CredentialStatusType, UserCredential
from accounts.repositories.administrationlevelrepository import AdministratorLevelRepository,AdminLevelType,AdminLevelStatusType
from accounts.loggers.logger import BaseLogger


class UserRecordsService(BaseService):

    def __init__(self, database: Database, **kwargs):
        super().__init__("user.record.service",db=database)
        self.Logger  = kwargs['logger'] if('logger' in kwargs) else None

    def Execute(self, request: Request) -> dict:
        self.Logger.Info("Request to get all users details")
        """
        :rtype: object
        """
        response            = dict()
        response['success'] = False
        user_uid            = request.values.get("user_id", "").lower()
        status              = False

        if type(user_uid) == str:
            user_repo = UserRepository(db=self.Database)
            user:User = user_repo.Get(user_uid)

            if user is not None:
                # verify if the user credential are not blocked.
                user_credential_repo = UserCredentialRepository(db=self.Database)
                credential:UserCredential = user_credential_repo.Get(user.UUID)

                if credential is not None:
                    if (credential.Status == CredentialStatusType.ACTIVATED) or \
                            (credential.Status == CredentialStatusType.SUCCESS):

                        # verify if the current user credential have access to this users list.
                        admin_level_repo = AdministratorLevelRepository(db=self.Database)

                        if admin_level_repo.IsAdmin(credential.UserID):

                            users = user_repo.Users
                            users_result = list()

                            for user in users:

                                dict_user = dict()
                                dict_user['user_uuid']      = user.UUID
                                dict_user['lastname']       = user.Lastname
                                dict_user['firstname']      = user.Firstname
                                dict_user['gender']         = user.Gender
                                dict_user['phone']          = user.PhoneNumber
                                dict_user['email']          = user.Email

                                users_result.append(dict_user)
                            response['users'] = users_result
                            status = True
                    else:
                        response['error_code'] = ErrorType.ACCOUNT_NOT_ACTIVATED
            user_repo.Database.Close()

        if status is not True:
            if 'error_code' not in response:
                response['error_code'] = ErrorType.NOT_ACCESS_ERROR
        return jsonify(response)





