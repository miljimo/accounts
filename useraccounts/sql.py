import sqlite3;
import uuid;
import datetime as dt;
from databases import Database, SQLResults, SQLStatement, SQLResult;



class AddressType(int):
    HOME_ADDRESS    =  0x01;
    OFFICE_ADDRESS  =  0x02;

class GenderType(int):
    MALE    = 0x00;
    FEMALE  = 0x01;

    def __init__(self, value):
        self.__Value   = value;

    @property
    def Value(self):
        return self.__Value;
        
    
    

class Address(object):

    def __init__(self, **kwargs):
        self.__Number       = None;
        self.__Street       = None;
        self.__County       = None;
        self.__Country      = None;
        self.__LocalGovt    =  None;
        self.__AddressType  =  AddressType.HOME_ADDRESS;
     

    
class User(object):
    def __init__(self, **kwargs):
        self.__UUID          = kwargs['uuid'] if('uuid' in kwargs) else None;
        self.__Lastname      = kwargs['lastname'] if('lastname' in kwargs) else "";
        self.__Firstname     = kwargs['firstname'] if('firstname' in kwargs) else "";
        
        self.__EmailAddress  = kwargs['email'] if('email' in kwargs) else "";
        self.__Gender        = kwargs['gender'] if('gender' in kwargs) else GenderType.MALE;
        self.__Credential    = None;
        self.__Addresses     = dict();
        self.__DateRegistered  =  kwargs['registered_date'] if('registered_date' in kwargs) else dt.datetime.now();
        self.__LastDateUpdated    =  kwargs['last_update_date'] if('last_update_date' in kwargs) else dt.datetime.now();  
        
    @property
    def LastDateUpdated(self):
        return self.__LastDateUpdated;

    @LastDateUpdated.setter
    def LastDateUpdated(self, value):
        if(isinstance(value, dt.datetime) != True):
            raise TypeError("@LastDateUpdated : expecting a datetime object");
        self.__LastDateUpdated  =  value;
        return self;
    
    @property
    def DateRegistered(self):
        return self.__DateRegistered;

    @DateRegistered.setter
    def DateRegistered(self, value):
        if(isinstance(value, dt.datetime) != True):
            raise TypeError("@DateRegistered : expecting a datetime object");
        self.__DateRegistered  =  value;
        return self;
    
    @property
    def UUID(self):
        return self.__UUID;

    @UUID.setter
    def UUID(self, value):
        if(type(value) == str):
            self.__UUID  = value;
        return self;
    
    @property
    def Firstname(self):
        return self.__Firstname;

    @Firstname.setter
    def Firstname(self, value):
        if(type(value) == str):
            self.__Firstname  =  value;
        return self;
    
    @property
    def Gender(self):
        return self.__Gender;
    
    @Gender.setter
    def Gender(self, value):
        if(type(value) == int):
            self.__Gender  =  value;
        return self;

    @property
    def Email(self):
        return self.__EmailAddress;

    @Email.setter
    def Email(self, value):
        if(type(value) == str):
            self.__EmailAddress  =  value;
        return self;
    
    @property
    def Lastname(self):
        return self.__Lastname;

    @Lastname.setter
    def Lastname(self, value):
        if(type(value) == str):
            self.__Lastname = value;
        return self;            
    
    @property
    def Addresses(self):
        return self.__Addresses;





class Respository(object):

    def __init__(self, **kwargs):
        database  = kwargs['db'] if('db' in kwargs) else None;
        if(isinstance(database, Database) != True):
            database  =  Database.GetManager().Get("Default");
            if(database != None):
                raise TypeError("@Repo: expecting a database object for the repo source of data");
        self.__Database  =  database;

    @property
    def Database(self):
        return self.__Database;

    


class UserAccount(Respository):

    def __init__(self, **kwargs):
        super().__init__(**kwargs);
        if(self.Database != None):
            self.Database.Execute('''CREATE TABLE IF NOT EXISTS tbl_users
                                        (user_uuid text PRIMARY KEY NOT NULL,
                                         lastname text NOT NULL,
                                         firstname text NOT NULL,
                                         email text NOT NULL,                                        
                                         gender text,
                                         date_registered text NOT NULL,
                                         last_update_date text NOT NULL)''');
            self.__Users  =  None;

    def Exists(self, user_uuid: str):
        status  =  False;
        if(type(user_uuid) == str):
            stmt  =  self.Database.Execute("SELECT *FROM tbl_users WHERE (user_uuid=? OR email==?)", (user_uuid, user_uuid));
            if(stmt.RowCount > 0):
                status   =  True;
        return status;

    def Create(self, user: User):
        result  = None;
        if(isinstance(user, User)):
            User.UUID  =  self.NextUUID;
            sql  =  "INSERT into tbl_users values(?,?,?,?,?,?,?)";
            date  =  "{0}".format(dt.datetime.now().timestamp());
            stmt  =  self.Database.Execute(sql, (user.UUID, user.Lastname, user.Firstname, user.Email, user.Gender,date,date ));            
            self.Database.Commit();
            result  =  user;
        return result;


    def Get(self, user_uuid: str):        
        result  =  None;
        if(type(user_uuid) == str):
            
            stmt  =  self.Database.Execute("SELECT *FROM tbl_users WHERE (user_uuid=? OR email==?)", (user_uuid, user_uuid));
            if(stmt.RowCount > 0):
                record  =  stmt.Next;
                if(record != None):
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
            user.DateRegistered =  dt.datetime.fromtimestamp(float(record.Get("date_registered")));           
            
        return user;    

    @property
    def NextUUID(self):
        nextuid  =  0000;
        if(self.Database != None):
            stmt  = self.Database.Execute("Select *from tbl_users");
            count =  stmt.RowCount;
            uuid_id = uuid.uuid4();
            nextuid  = "{0}{1}".format(uuid_id, count);
        return nextuid;

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
                    stmt  =  self.Database.Execute("UPDATE tbl_users SET email=?, firstname=?, gender=?,lastname=?,last_update_date=? WHERE (user_uuid=?)",
                                                    (user.Email,user.Firstname, user.Gender, user.Lastname, dt.datetime.now().timestamp(), user.UUID));
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

    def Clear(self):
        if(self.Database != None):
            stmt = self.Database.Execute("Delete from tbl_users");
            self.Database.Commit();
        return self;    

    def Drop(self):
        if(self.Database != None):
            self.Database.Execute("DROP table tbl_users");
        return self;
    
        
    

if(__name__ == "__main__"):
    account     =  UserAccount(db =  Database(name  =  'rgb.db'));
   
    account.Create(User(firstname= "Obaro", lastname ="Johnson", gender = GenderType.MALE, email="johnson.obaro"));
    account.Create(User(firstname= "Will", lastname ="Johnson", gender = GenderType.MALE, email="johnson.obaro@hotmail.com"));

    print("List Of Users");
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

    
   
    
