import sqlite3
from threading import Lock
from accounts.databases.databasemanager import DatabaseManager
from accounts.databases.idatabase import IDatabase
from accounts.databases.sqlstatement import SQLStatement


class Database(IDatabase):
    __Manager = None
    __Locker  =  Lock()
    @staticmethod
    def GetManager():
        if Database.__Manager is None:
            Database.__Manager = DatabaseManager()
        return Database.__Manager

    def __init__(self, **kwargs):
        self.__Locker.acquire()
        self.__Manager = self.GetManager()
        databaseName = kwargs['name'] if ('name' in kwargs) else None
        if type(databaseName) != str:
            raise TypeError("Database: Expecting a database name but {0} type was provided".format(databaseName))
        self.__DatabaseName = databaseName
        self.__Conn = sqlite3.connect(databaseName)
        self.__Conn.row_factory = sqlite3.Row
        self.__Cursor = self.__Conn.cursor()
        if self.Manager.Exists(self.Name) is not True:
            self.Manager.Add(self)
        self.__Locker.release()

    @property
    def Name(self):
        return self.__DatabaseName

    @property
    def Manager(self):
        return self.__Manager

    def Execute(self, statement: str, parameters: tuple = ()):
        self.__Locker.acquire()
        result = None
        if type(statement) != str:
            raise TypeError("@Statement: must be a python string")
        if parameters is not None:
            if type(parameters) != tuple:
                raise TypeError("@expecting parameters to be tuple.")

        if self.__Conn is not None:
            if self.__Cursor is not None:
                self.__Cursor.execute(statement, parameters)
                result = SQLStatement(self.__Conn, self.__Cursor)
        self.__Locker.release()
        return result

    def Commit(self):
        self.__Locker.acquire()
        if self.__Conn is not None:
            self.__Conn.commit()
        self.__Locker.release()

    def RollBack(self):
        self.__Locker.acquire()
        if self.__Conn  is not None:
            self.__Conn.rollback()

        self.__Locker.release()

    def Close(self):
        self.__Locker.acquire()
        if self.__Conn is not None:
            self.Manager.Remove(self.Name)
            self.__Conn.close()
            del self.__Conn;
            self.__Conn  = None;
        self.__Locker.release()


if (__name__ == "__main__"):
    db = Database(name="dbtest.db")
    print(db)
    db = Database.GetManager().Get("dbtest.db")
    print(db)
    db2 = Database(name="dbtest2.db")
    nData = db.Manager.Count
    print(nData)
    print(db.Manager.Count)
    db.Execute("CREATE TABLE IF NOT EXISTS tbl_test (uuid text primary key not null)")
    db.Execute("DROP TABLE IF EXISTS tbl_test")
    db.Close()

    pass;
