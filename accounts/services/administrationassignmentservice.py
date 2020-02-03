import copy
import datetime as dt
from flask import jsonify, request as Request
from accounts.data.usercredential import CredentialStatusType, UserCredential
from accounts.data.userlevel import UserLevel, AdminLevelType
from accounts.databases.database import Database
from accounts.errors.error import ErrorType
from accounts.repositories.administrationlevelrepository import AdministratorLevelRepository
from accounts.repositories.usercredentialrepository import UserCredentialRepository
from accounts.repositories.userrepository import UserRepository
from accounts.server.main import UserAdminLevelUpdatedEvent
from accounts.services.baseservice import BaseService


class AdministrationAssignmentService(BaseService):

    def __init__(self, database:Database, **kwargs):
        super().__init__("administration.assignment.service", db=database, **kwargs)


    def Execute(self, request: Request) -> dict:
        self.Logger.Info("Assigning new administration levels")
        response = dict()
        response['success'] = False
        user_uid = request.values.get('user_id', '').lower()
        level = request.values.get("level", None)
        assigned_timestamp = request.values.get('assigned_timestamp', 0.0)
        expired_timestamp = request.values.get('expired_timestamp', 0.0)
        try:
            status  = self.Validate(user_id = user_uid, assigned_timestamp=assigned_timestamp, expired_timestamp=expired_timestamp, level=level)
            if status == ErrorType.NORMAL:
                status = self.UpdateAdministratorLevel(user_uid=user_uid,
                                                       assigned_timestamp=assigned_timestamp,
                                                       expired_timestamp=expired_timestamp,
                                                       level=level)

                if status is ErrorType.NORMAL:
                    del response['error_code']
                    response['success'] = True

        except Exception as err:
            self.Database.RollBack()
            self.Logger.Error(err)
        finally:
            self.Logger.Info("Administration assignment service completed.")

        if response['success'] is not True:
            response['error_code'] = 'Error found'
        return jsonify(response)


    def Validate(self, **kwargs):
        status_code                  = ErrorType.VALIDATION_ERROR
        user_uid :str                = kwargs['user_id'] if('user_id' in kwargs) else ''
        assigned_timestamp:float     = kwargs['assigned_timestamp'] if('assigned_timestamp' in kwargs) else 0.0
        expired_timestamp: float     = kwargs['expired_timestamp'] if ('expired_timestamp' in kwargs) else 0.0
        level :AdminLevelType        = kwargs['level'] if ('level' in kwargs) else 0.0

        if type(user_uid) == str:
            now             = dt.datetime.now()
            assigned_date   = dt.datetime.fromtimestamp(float(assigned_timestamp))
            expired_date    = dt.datetime.fromtimestamp(float(expired_timestamp))

            if now < assigned_date:
                if assigned_date < expired_date:
                   if AdminLevelType.IsValid(level):
                       status_code  = ErrorType.NORMAL
        return status_code

    def UpdateAdministrationLevel(self,**kwargs):
        status_code  = ErrorType.UNABLE_ASSIGNED_ADMINISTRATOR_ERROR
        user_uid:str = kwargs['user_id'] if('user_id' in kwargs) else None
        user_repo = UserRepository(db=self.Database)
        user = user_repo.Get(user_uid)
        if user is not None:
            credential: UserCredential  = self.GetAdminCredential(user_uid=user.UUID)
            if credential is not None:
                status_code  = self.UpdateLevel()
        return status_code

    def GetAdminCredential(self, user_uid: str) -> UserCredential:
        credential : UserCredential = None
        credential_repo = UserCredentialRepository(db=self.Database, logger=self.Logger)
        tem_credential = credential_repo.Get(user_uid)

        if tem_credential is not None:
            if (credential.Status == CredentialStatusType.SUCCESS) or (
                    credential.Status == CredentialStatusType.ACTIVATED):
                credential = tem_credential
        return credential

    def UpdateLevel(self, **kwargs):
        status_code  = ErrorType.UNABLE_TO_UPDATE_RECORD
        user_level:UserLevel  =  kwargs['user_level'] if ('user_level' in kwargs) else 0.0
        level = kwargs['level'] if ('level' in kwargs) else None
        assigned_date:float = kwargs['assigned_date'] if('assigned_date' in kwargs) else 0.0
        expired_date:float  = kwargs['expired_date'] if('assigned_date' in kwargs) else 0.0
        user_id : str = kwargs['user_id'] if('assigned_date' in kwargs) else ''

        if user_level is not None:
            temp_user_level     = copy.deepcopy(user_level)
            user_level.Level    = level if (level is not None) else user_level.Level
            user_level.Assigned = assigned_date if (assigned_date is not None) else user_level.Assigned
            user_level.Expired  = expired_date if (expired_date is not None) else user_level.Expired

            admin_repo = AdministratorLevelRepository(db=self.Database, logger=self.Logger)
            result = admin_repo.Update(user_id, user_level)

            if result is True:
                if self.UserAdminLevelUpdated is not None:
                    self.UserAdminLevelUpdated(UserAdminLevelUpdatedEvent(temp_user_level, user_level))
                    status_code = ErrorType.NORMAL
        return status_code

