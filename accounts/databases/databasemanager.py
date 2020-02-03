from accounts.databases.idatabase import IDatabase


class DatabaseManager(object):
    __INSTANCE__    = None
    __CLASS__       = None
    __DATABASES__   = dict()

    def __new__(cls, *args, **kwargs):
        if (cls is not None) and (cls.__INSTANCE__ is None):
            cls.__INSTANCE__ = super().__new__(cls, *args, **kwargs)
            cls.__CLASS__ = cls
        return cls.__INSTANCE__

    def Exists(self, databaseName: str) -> bool:
        status = False
        if type(databaseName) == str:
            status = (databaseName in self.__DATABASES__)
        return status

    def Add(self, database: IDatabase):
        index = -1

        if isinstance(database, IDatabase) is not True:
            raise TypeError("@Expecting a database object")
        if self.Exists(database.Name) is not True:
            self.__DATABASES__[database.Name] = database
            index = len(self.__DATABASES__) - 1
        return index

    def Remove(self, databaseName: str):
        result = None
        if type(databaseName) == str:
            if databaseName in self.__DATABASES__:
                result = self.__DATABASES__[databaseName]
                del self.__DATABASES__[databaseName]
        return result

    def Get(self, name):
        database = None
        if name in self.__DATABASES__:
            database = self.__DATABASES__[name]
        return database

    @property
    def Count(self):
        return len(self.__DATABASES__);
