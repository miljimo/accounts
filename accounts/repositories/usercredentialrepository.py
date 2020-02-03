import copy
import datetime as dt
import random
import time
from accounts.data.usercredential import UserCredential
from accounts.databases.database import Database
from accounts.databases.sqlresult import SQLResult
from accounts.repositories.repository import Repository


class UserCredentialRepository(Repository):

    def __init__(self, **kwargs):
        kwargs["name"] = "tbl_user_credential";
        super().__init__(**kwargs);
        if (self.Database != None):
            self.Database.Execute('''CREATE TABLE IF NOT EXISTS {0} (user_uuid text primary key,
                                                                     password text not null,
                                                                     session_uuid varchar(50) not null,
                                                                     activate_code varchar(20) not null,                                                                     
                                                                     status integer not null,
                                                                     last_date varchar(50) not null)'''.format(
                self.Name))

    def Create(self, user_uuid: str, credential: UserCredential):
        result = None;
        if type(user_uuid) == str:
            if isinstance(credential, UserCredential):
                if self.IsTable:
                    credential = copy.copy(credential)
                    credential.LastDate = dt.datetime.now()
                    credential.UserID = user_uuid
                    timestamp = str(credential.LastDate.timestamp())
                    credential.SessionID = self.NextUUID
                    code  = self.GenerateNumber()
                    stmt = self.Database.Execute('''INSERT into {0} (user_uuid, password,session_uuid,activate_code, status, last_date)
                                                                      values(?,?,?,?,?,?)'''.format(self.Name),
                                                 (user_uuid, credential.Password, credential.SessionID,code,
                                                  credential.Status, timestamp))
                    self.Database.Commit()
                    result = credential

                pass;
        return result

    def GenerateNumber(self, start=100000, end =999999):
        random.seed(time.time())
        numbers = random.randrange(start,end)

        return numbers

    def Exists(self, user_uuid: str, session_uid: str = None):
        return self.Get(user_uuid, session_uid) is not None

    def _ParseCredential(self, record: SQLResult):
        credential = None
        if record is not None:
            credential = UserCredential(user_uuid=record.Get("user_uuid"));
            credential.Password = record.Get("password");
            credential.SessionID = record.Get("session_uuid");
            credential.Status = record.Get("status");
            credential.ActivateCode = record.Get('activate_code')
            credential.LastDate = dt.datetime.fromtimestamp(float(record.Get("last_date")));

        return credential;

    def Get(self, user_uuid: str, session_uuid: str = None) -> UserCredential:
        """
        :param user_uuid:
        :param session_uuid:
        :return: UserCredential
        """
        result = None;
        if (type(user_uuid) == str):
            stmt = None;
            if (session_uuid == None):
                stmt = self.Database.Execute("SELECT *from {0} where (user_uuid=?) ".format(self.Name), (user_uuid,));
            else:
                stmt = self.Database.Execute(
                    "SELECT *from {0} where (user_uuid=? AND session_uuid = ?) ".format(self.Name),
                    (user_uuid, session_uuid));
            if (stmt != None):
                if (stmt.RowCount > 0):
                    record = stmt.Next;
                    result = self._ParseCredential(record);
        return result;

    @property
    def Credentials(self):
        credentials = list();
        if (self.Database != None):
            stmt = self.Database.Execute("SELECT *from {0}".format(self.Name));
            if (stmt.RowCount > 0):
                record = stmt.Next;
                while (record != None):
                    credential = self._ParseCredential(record);
                    if (credential != None):
                        credentials.append(credential);
                    record = stmt.Next;
        return credentials;

    def Update(self, user_uuid: str, credential: UserCredential):
        status = False;
        if (type(user_uuid) == str):
            if (isinstance(credential, UserCredential)):
                last_update = dt.datetime.now();
                last_update_timestamp = last_update.timestamp();

                stmt = self.Database.Execute(
                    "UPDATE {0} SET session_uuid=?, activate_code=?,status=?, password=?, last_date=? where (user_uuid=?)".format(
                        self.Name),
                    (credential.SessionID, credential.ActivateCode, credential.Status, credential.Password, last_update_timestamp, user_uuid));
                self.Database.Commit();
                status = True;

        return status;

    def Delete(self, user_uuid: str):
        status = False;
        if (type(user_uuid) == str):
            stmt = self.Database.Execute("DELETE FROM {0} WHERE (user_uuid=?)".format(self.Name), (user_uuid,));
            self.Database.Commit();
            status = True;
        return status;


if (__name__ == "__main__"):
    database = Database(name="../server/dbtest.db");
    respo = UserCredentialRepository(db=database);

    credential = UserCredential(user_uuid="001", password="johnsone", status=0);
    result1 = respo.Create("001", credential);
    result2 = respo.Create("00123", credential);
    result2 = respo.Create("001234", credential);
    print(respo.Credentials);
    print((result1.SessionID, result1.UserID));
    if (respo.Exists("001", result1.SessionID)):
        print("Exist");
    record = respo.Get("001", result1.SessionID);
    print(result1.SessionID);
    print(record);
    print("Updating testing");
    print(result1.Password);
    print(result1.Status);
    result1.Password = "CathyPassword";
    result1.Status = 2;
    respo.Update(result1.UserID, result1);
    record = respo.Get(result1.UserID);
    print(record.Password);
    print(record.Status);
    print("__update testing done");

    print("Test Delete");
    r = respo.Get("001");
    print(r);
    respo.Delete("001");
    r = respo.Get("001");
    print(r);
    respo.Drop();
    database.Close();
