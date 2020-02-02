import uuid;
from databases import Database;

class Respository(object):

    def __init__(self, **kwargs):
        database  = kwargs['db'] if('db' in kwargs) else None;
        name      = kwargs['name'] if('name' in kwargs) else None;
        if(type(name) != str):
            raise TypeError("Expecting a table name to be string {0}".format(name));
        if(isinstance(database, Database) != True):
            database  =  Database.GetManager().Get("Default");
            if(database != None):
                raise TypeError("@Repo: expecting a database object for the repo source of data");
        self.__Database   =  database;
        self.__Name       = name;

    @property
    def IsTable(self):
        status =  False;
        if(self.Database != None):
            stmt =  self.Database.Execute(''' SELECT * FROM sqlite_master WHERE type='table' AND name=? ''', (self.Name , ));
            
            if(stmt.RowCount > 0):
                status =  True;
        return status;

    @property
    def NextUUID(self):
        nextuid  =  0000;
        if(self.Database != None):
            if(self.IsTable):   
                stmt  = self.Database.Execute("Select * from {0}".format(self.Name));
                count =  stmt.RowCount;
                uuid_id = uuid.uuid4();
                nextuid  = "{0}{1}".format(uuid_id, count);
        return nextuid;

    @property
    def Name(self):
        return self.__Name;

    @property
    def Database(self):
        return self.__Database;

    def Drop(self):
        if(self.Database != None):
            self.Database.Execute("DROP table IF EXISTS {0} ".format(self.Name));
        return self;
    
    def Clear(self):
        if(self.Database != None):
            if(self.IsTable):
                stmt = self.Database.Execute("DELETE from {0} ".format(self.Name));
                self.Database.Commit();
        return self; 
        

    

if(__name__ =="__main__"):
    database  =  Database(name="test_db");
    database.Execute("Create table if not exists tbl_test (user_uuid text PRIMARY KEY NOT NULL, lastname text NOT NULL)");
    respo  =  Respository(db= database, name='tbl_test');
    print(respo.Database.Manager.Count);
    print(respo.Name);
    print(respo.NextUUID);
    respo.Clear();
    respo.Drop();
    database.Close();
    
    
