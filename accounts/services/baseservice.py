from flask import request as Request
import hashlib
from accounts.databases.database import Database
from accounts.loggers.logger import  BaseLogger


class BaseService(object):

    def __init__(self, name, **kwargs):
        self.__database  = kwargs['db'] if('db' in kwargs) else None
        self.__name  = name if(type(name) == str) else 'base_service'
        self.__Logger  = kwargs['logger'] if('logger' in kwargs) else None
        if isinstance(self.__database, Database) is not True:
            raise TypeError("Expecting a database object")
        self.__Status = False

    @property
    def Logger(self) -> BaseLogger:
        return self.__Logger

    @property
    def Status(self)->bool:
        return self.__Status

    @Status.setter
    def Status(self, status: bool):
        if type(status) == bool:
            self.__Status = status

    @property
    def Database(self) -> Database:
        return self.__database

    def GetHash(self, plain_test):
        s = hashlib.sha1()
        s.update(plain_test.encode('utf-8'))
        return s.hexdigest()


    def Execute(self, request: Request) -> dict:
        raise NotImplementedError('Execute: method must be implement before use.')





