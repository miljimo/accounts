import datetime as dt;
import uuid;


class CredentialStatusType(int):
    NORMAL: int = 0x00
    SUCCESS: int = 0x01
    BLOCKED: int = 0x02
    ACTIVATED: int = 0x03


class UserCredential(object):

    def __init__(self, **kwargs):
        self.__UserUID = kwargs['user_uuid'] if ('user_uuid' in kwargs) else "";
        self.__Password = kwargs['password'] if ('password' in kwargs) else "";
        self.__SessionID = kwargs['session_uuid'] if ('session_uuid' in kwargs) else "__session__";
        self.__Status = kwargs['status'] if ('status' in kwargs) else CredentialStatusType.NORMAL;
        self.__LastDate = kwargs['last_date'] if ('last_date' in kwargs) else dt.datetime.now();
        self.__ActivatedCode  =  None

    @property
    def ActivateCode(self):
        return self.__ActivatedCode

    @ActivateCode.setter
    def ActivateCode(self, code):
        self.__ActivatedCode = code

    @property
    def LastDate(self):
        return self.__LastDate;

    @LastDate.setter
    def LastDate(self, lastdate: dt.datetime):
        if (isinstance(lastdate, dt.datetime) != True):
            raise TypeError("@LastDate: expecting a datetime object.");
        self.__LastDate = lastdate;
        return self;

    @property
    def Status(self):
        return self.__Status;

    @Status.setter
    def Status(self, status: CredentialStatusType):
        if type(status) == int:
            if((status == CredentialStatusType.NORMAL) or
                    (status == CredentialStatusType.SUCCESS) or
                    (status == CredentialStatusType.ACTIVATED) or
                    (status == CredentialStatusType.BLOCKED)):
                self.__Status = status;
        return self;

    @property
    def UserID(self):
        return self.__UserUID;

    @UserID.setter
    def UserID(self, value: str):
        if type(value) == str:
            self.__UserUID = value;
        return self;

    @property
    def Password(self):
        return self.__Password;

    @Password.setter
    def Password(self, password: str):
        if (type(password) == str):
            self.__Password = password;
        return self;

    @property
    def SessionID(self):
        return self.__SessionID;

    @SessionID.setter
    def SessionID(self, session: str):
        if (type(session) == str):
            self.__SessionID = session;

        return self;

    def __repr__(self):
        return "UserCredential(user_uuid={0},session={1})".format(self.UserID, self.SessionID);


if (__name__ == "__main__"):
    credential = UserCredential();
    credential.SessionID = uuid.uuid4();
    print(credential);
