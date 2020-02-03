import datetime as dt


class AdminLevelType(str):
    SITE_USERS_LEVEL = "site.user.level"
    SITE_ADMINISTRATION_LEVEL = 'site.administrator.user.level'
    DEVELOPER_ADMINISTRATOR_LEVEL = 'developer.administrator.user.level'


class AdminLevelStatusType(int):
    NORMAL: int = 0x4000
    PRIVILEGED_REVOKED: int = 0x4001





class UserLevel(object):

    def __init__(self, **kwargs):
        self.__UserUUID = kwargs['user_uuid'] if ('user_uuid' in kwargs) else None
        self.__AdminLevel = kwargs['admin_level'] if ('admin_level' in kwargs) else None
        self.__Status = kwargs['status'] if ('status' in kwargs) else None
        self.__ExpiredDate = kwargs['expired_date'] if ('expired_date' in kwargs) else dt.datetime.now()
        self.__AssignDate = kwargs['assigned_date'] if ('expired_date' in kwargs) else dt.datetime.now()
        self.__DateCreated = kwargs['date_created'] if ('date_created' in kwargs) else dt.datetime.now()

    @property
    def DateCreated(self):
        return self.__DateCreated

    @DateCreated.setter
    def DateCreated(self, date_created):
        if isinstance(date_created, dt.datetime):
            self.__DateCreated = date_created
        return self

    @property
    def Expired(self):
        return self.__ExpiredDate

    @Expired.setter
    def Expired(self, expired_date: dt.datetime):
        if isinstance(expired_date, dt.datetime) is True:
            self.__ExpiredDate = expired_date

    @property
    def Assigned(self):
        return self.__AssignDate

    @Assigned.setter
    def Assigned(self, assign_date: dt.datetime):
        if isinstance(assign_date, dt.datetime):
            self.__AssignDate = assign_date

    @property
    def Status(self):
        return self.__Status

    @Status.setter
    def Status(self, status):
        if type(status) == bool:
            self.__Status = status

    @property
    def UserID(self):
        return self.__UserUUID

    @UserID.setter
    def UserID(self, user_uuid: str):
        if type(user_uuid) == str:
            self.__UserUUID = user_uuid

    @property
    def Level(self) -> AdminLevelType:
        return self.__AdminLevel

    @Level.setter
    def Level(self, level: AdminLevelType):
        if  type(level) == str:
            self.__AdminLevel = level

    def __str__(self):
        return "UserLevel(uuid={0},date_created={1})".format(self.UserID, self.DateCreated)
