import sqlite3;

class IDatabase(object):
    

    @property
    def Name(self):
        raise NotImplementedError("@Name : property must be implemented");

    @property
    def Manager(self):
        raise NotImplementedError("@Manager : property must be implemented");

    def Execute(self, sqlstatement: str, parameter: tuple = ()):
        raise NotImplementedError("@Execute : method must be implemented");

    def Commit(self):
        raise NotImplementedError("@Commit : method must be implemented");

    def Close(self):
        raise NotImplementedError("@Close : method must be implemented");


class SQLResult(object):

    def __init__(self, cursor , row):
        self.__Cursor  =  cursor;
        self.__Row     =  row;
        self.__Keys    =  self.__Row.keys();

    @property
    def Keys(self):
       return self.__Keys;
    
    def Get(self, key):
        value = None;
        if(key in self.Keys):
            value   = self.__Row[key];
        return value;


class SQLResults(object):

    def __init__(self, conn, cursor):
        self.__conn    =  conn;
        self.__cursor  =  cursor;
        self.__rows    =  cursor.fetchall();
        self.__rowcount  =  len(self.__rows);
        self.__RowIndex  = 0;

    @property
    def Next(self):
        row  =  None;
        if(self.__RowIndex < self.RowCount):
            row =  SQLResult(self.__cursor, self.__rows[self.__RowIndex]);
            self.__RowIndex += 1;
        return row;
    
    @property
    def CurrentIndex(self):
        return self.__RowIndex;

    def Reset(self):
        self.__RowIndex  = 0;
            

    @property
    def RowCount(self):
        return self.__rowcount;

    def Clear(self):
        self.Reset();
        self.__rows      =  self.fetchall();
        self.__rowcount  =  len(self.__rows);


class SQLStatement(object):

    def __init__(self, conn , cursor):
        self.__RowCount   = 0;
        if(isinstance(conn, sqlite3.Connection) != True):
            raise ValueError("Expecting a sqlite3.Connection object in parameter 1");
        if(isinstance(cursor, sqlite3.Cursor) != True):
            raise ValueError("@Expecting a cursor object as the sqlite3.Cursor");
        self.__Conn       = conn;
        self.__Cursor     = cursor;
        self.__Result     = SQLResults(self.__Conn, self.__Cursor);
        
    @property
    def RowCount(self):
        rowcount  =  0;
        if(self.__Result != None):
            rowcount  =  self.__Result.RowCount;
        return rowcount;

    @property
    def Next(self):
        row  =  None;
        if( self.__Result != None):
            row  =   self.__Result.Next;
        return row;

    def Reset(self):
        if(self.__Result != None):          
            self.__Result.Reset();
    
"""
 Database manager;
"""
class DatabaseManager(object):

    __INSTANCE__    =  None;
    __CLASS__       =  None;
    __DATABASES__   =  dict();
    

    def __new__(cls , *args, **kwargs):
        if ( (cls != None) and (cls.__INSTANCE__ == None)):  
            cls.__INSTANCE__ =  super().__new__(cls, *args, **kwargs);
            cls.__CLASS__ =  cls;
        return cls.__INSTANCE__;


    def Exists(self, databaseName):
        status  =  False;
        if(type(databaseName) == str):
            status  =  (databaseName in self.__DATABASES__);
        return status;

    def Add(self, database: IDatabase):
        index  =  -1;
        
        if(isinstance(database, IDatabase) != True):
            raise TypeError("@Expecting a database object");
        if(self.Exists(database.Name) != True):
            self.__DATABASES__[database.Name]  =  database;
            index  =  len(self.__DATABASES__) - 1;
        return index;

    def Remove(self, databaseName:str):
        result   = None;
        if(type(databaseName) == str):
            if(databaseName in self.__DATABASES__):
                result  =  self.__DATABASES__[databaseName];
                del self.__DATABASES__[databaseName];
        return result;

    def Get(self, name):
        database =  None;
        if(name in self.__DATABASES__):
            database = self.__DATABASES__[name];
        return database;

    @property
    def Count(self):
        return len(self.__DATABASES__);
    
"""
 The database object for manipulating the sql 
"""
class Database(IDatabase):
    __Manager  =  None;

    @staticmethod
    def GetManager():
        if(Database.__Manager == None):
           Database.__Manager = DatabaseManager();
        return Database.__Manager;
    

    def __init__(self,**kwargs):
        self.__Manager = self.GetManager();
        databaseName  =  kwargs['name'] if('name' in kwargs) else None;
        if(type(databaseName) != str):
            raise TypeError("Database: Expecting a database name but {0} type was provided".format(databaseName)); 
        self.__DatabaseName     = databaseName;
        if(self.Manager.Exists(self.Name)):
            raise ValueError("@Database: already opened and created, use manager.Get to get the instance");
        
        self.__Conn             = sqlite3.connect(databaseName);
        self.__Conn.row_factory = sqlite3.Row;
        self.__Cursor           = None;
        self.Manager.Add(self);
        

    @property
    def Name(self):
        return self.__DatabaseName;
    

    @property
    def Manager(self):
        return self.__Manager;

    def Execute(self, statement: str, parameters : tuple = ()):
        result  =  None;        
        if(type(statement) != str):
            raise TypeError("@Statement: must be a python string");
        if(parameters != None):
            if(type(parameters) != tuple):
                raise TypeError("@expecting parameters to be tuple.");

        if(self.__Conn != None):
            if(self.__Cursor == None):
                self.__Cursor =  self.__Conn.cursor();
            self.__Cursor.execute(statement, parameters);
            result  =  SQLStatement(self.__Conn, self.__Cursor);           
        return result;
    

    def Commit(self):
        if(self.__Conn != None):
            self.__Conn.commit();            


    def Close(self):
        if(self.__Conn != None):
            self.__Conn.close();
            self.Manager.Remove(self.Name);
            self.__Conn == None;
            



if(__name__ == "__main__"):
    db =  Database(name   =  "dbtest.db");
    print(db);
    db =  Database.GetManager().Get("dbtest.db");
    print(db);
    db2 =  Database(name   =  "dbtest2.db");
    nData  = db.Manager.Count;
    print(nData);
    db2.Close();
    print(db.Manager.Count);
    pass;

