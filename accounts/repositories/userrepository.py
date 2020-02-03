import datetime as dt
from accounts.databases.database import Database
from accounts.databases.sqlresult import SQLResult
from accounts.data.user import User, GenderType
from accounts.repositories.repository import Repository


class UserRepository(Repository):

    def __init__(self, **kwargs):
        kwargs['name'] = 'tbl_users'
        super().__init__(**kwargs)
        if self.Database is not None:
            self.Database.Execute('''CREATE TABLE IF NOT EXISTS {0} 
                                        (user_uuid text PRIMARY KEY NOT NULL,
                                         lastname text NOT NULL,
                                         firstname text NOT NULL,
                                         email text NOT NULL,                                        
                                         gender text,
                                         phone_number text,
                                         date_registered text NOT NULL,
                                         last_update_date text NOT NULL)'''.format(self.Name))

            self.Database.Commit()
            self.__Users  = list()

    def Exists(self, user_uuid: str):
        status  = False
        if type(user_uuid) == str:
            stmt  =  self.Database.Execute("SELECT *FROM tbl_users WHERE (user_uuid=? OR email==?)", (user_uuid, user_uuid))
            if stmt.RowCount > 0:
                status   = True
        return status

    def Create(self, user: User) -> User:
        result  = None
        if isinstance(user, User):
            if self.Exists(user.Email) is not True:
                User.UUID  = self.NextUUID
                email = user.Email.lower().strip()
                sql  = "INSERT into tbl_users (user_uuid,lastname,firstname,email,gender,phone_number,date_registered, last_update_date) values(?,?,?,?,?,?,?,?)"
                date_created  = "{0}".format(dt.datetime.now().timestamp())
                date_updated =date_created
                stmt  = self.Database.Execute(sql, (user.UUID, user.Lastname, user.Firstname, email, user.Gender,user.PhoneNumber, date_created,date_updated))
                self.Database.Commit()
                result  = user
        return result

    def Get(self, user_uuid: str):
        result  = None;
        if type(user_uuid) == str:
            email = user_uuid.lower().strip()
            stmt  = self.Database.Execute("SELECT *FROM {0} WHERE user_uuid=? OR email=?".format(self.Name), (user_uuid, email));
            if stmt.RowCount > 0:
                record  = stmt.Next;
                if record is not None:
                    result  = self._ParseRecord(record);
        return result;

    def _ParseRecord(self, record: SQLResult):
        user = None;
        if(isinstance(record, SQLResult)):
            user_uid =  record.Get("user_uuid");
            user  =  User(last_update_date = record.Get("last_update_date"));
            user.UUID           = user_uid;
            user.Firstname      =  record.Get("firstname");
            user.Lastname       =  record.Get("lastname");
            user.Gender         =  record.Get("gender");
            user.Email          =  record.Get("email");
            user.PhoneNumber    =  record.Get('phone_number')
            user.DateRegistered =  dt.datetime.fromtimestamp(float(record.Get("date_registered")));

        return user;

    @property
    def Users(self):
        users  =  list();
        stmt  =  self.Database.Execute("Select *from tbl_users");
        if(stmt.RowCount > 0):
            record  =  stmt.Next;
            while(record != None):
                user =  self._ParseRecord(record);
                if(user != None):
                    users.append(user);
                record =  stmt.Next;
            stmt.Reset();
        return users;

    def Update(self,user:User):
        status  = False;
        if(isinstance(user, User)):
            if(self.Exists(user.UUID)):
                if(self.Database != None):
                    stmt  =  self.Database.Execute("UPDATE tbl_users SET email=?, firstname=?, gender=?, phone_number=?,lastname=?,last_update_date=? WHERE (user_uuid=?)",
                                                    (user.Email,user.Firstname, user.Gender, user.PhoneNumber, user.Lastname, dt.datetime.now().timestamp(), user.UUID));
                    status  = True;
                    self.Database.Commit();
        return status;

    def Delete(self, user_uid: str):
        status =  False;
        if(type(user_uid) == str):
            if(self.Exists(user_uid)):
                stmt = self.Database.Execute("Delete from tbl_users where (user_uuid=? OR  email=?)", (user_uid, user_uid));
                self.Database.Commit();
                status  =  True;
        return status;


    def Find(self, search_str: str):
        users =  list();
        if(type(search_str) == str):
            if(self.Database != None):
                search_str= '%'+search_str+'%';
                stmt =  self.Database.Execute('''SELECT *from tbl_users where (user_uuid LIKE ?
                                                                            OR email LIKE ?
                                                                            OR gender LIKE ?
                                                                            OR lastname LIKE ?
                                                                            OR firstname LIKE ?)''',(search_str, search_str, search_str,search_str,search_str));
                record =  stmt.Next;
                while(record != None):
                    user  =  self._ParseRecord(record);
                    if(user != None):
                        users.append(user);
                    record  =  stmt.Next;
        return users;




if(__name__ == "__main__"):
    account     = UserRepository(db =  Database(name  ='../server/dbtest.db'));
    account.Create(User(firstname= "Obaro", lastname ="Johnson", gender = GenderType.MALE, email="johnson.obaro"));
    account.Create(User(firstname= "Will", lastname ="Johnson", gender = GenderType.MALE, email="johnson.obaro@hotmail.com"));
    account.Create(User(firstname= "Obaro", lastname ="Johnson", gender = GenderType.MALE, email="johnson.obaro"));
    users  =  account.Users;
    for user in users:
        print("user ={0} ,email ={1}".format(user.UUID, user.Email));
    user  =  account.Get("johnson.obaro");
    user.Firstname  =  "Cathy";
    print("Delete Email = {0}".format(user.UUID));
    account.Update(user);
    users  =  account.Users;
    print("List");
    for user in users:
        print("user ={0} ,email ={1}".format(user.UUID, user.Email));


    users  =  account.Find("johnson");
    print(users);
    if(users != None):
       print(len(users));

    account.Clear();
    account.Drop();
    account.Database.Close();




