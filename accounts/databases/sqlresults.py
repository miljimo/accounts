from accounts.databases.sqlresult import SQLResult


class SQLResults(object):
    def __init__(self, conn, cursor):
        self.__conn = conn
        self.__cursor = cursor
        self.__rows = cursor.fetchall()
        self.__rowcount = len(self.__rows)
        self.__RowIndex = 0

    @property
    def Next(self):
        row = None
        if self.__RowIndex < self.RowCount:
            row = SQLResult(self.__cursor, self.__rows[self.__RowIndex])
            self.__RowIndex += 1
        return row

    @property
    def CurrentIndex(self):
        return self.__RowIndex

    def Reset(self):
        self.__RowIndex = 0

    @property
    def RowCount(self):
        return self.__rowcount

    def Clear(self):
        self.Reset()
        self.__rows = self.fetchall()
        self.__rowcount = len(self.__rows)