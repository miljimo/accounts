from flask import request as Request, jsonify
import hashlib
from accounts.databases.database import Database
from accounts.services.baseservice import BaseService
from accounts.repositories.userrepository import UserRepository
from accounts.repositories.usercredentialrepository import UserCredentialRepository
from accounts.data.usercredential import UserCredential, CredentialStatusType
from accounts.errors.error import  ErrorType


class UserAuthService(BaseService):

    def __init__(self, database: Database):
        super().__init__('user.authentication', db=database)

    def Execute(self, request: Request) -> dict:
        response = dict()
        username = request.values.get('username')
        password = request.values.get('password')

        user_repo = UserRepository(db=self.Database)
        user = user_repo.Get(username)

        if user is not None:
            user_uuid = user.UUID
            credential_repo = UserCredentialRepository(db=self.Database)
            credential = credential_repo.Get(user_uuid)

            if credential is not None:
                hash_password = self.GetHash(password)

                if (credential.Status == CredentialStatusType.ACTIVATED) and (credential.Password == hash_password):
                    response['success'] = True
                else:
                    response['error_code'] = ErrorType.ACCOUNT_BLOCK_ACTIVATED
            else:
                response['error_code'] = ErrorType.INVALID_CREDENTIAL_PROVIDED
        else:
            response['error_code'] = ErrorType.INVALID_CREDENTIAL_PROVIDED

        self.Database.Close()
        return jsonify(response)
