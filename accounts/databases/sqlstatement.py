import sqlite3
from accounts.databases.sqlresults import SQLResults


class SQLStatement(object):

    def __init__(self, conn, cursor):
        self.__RowCount = 0
        if isinstance(conn, sqlite3.Connection) is not True:
            raise ValueError("Expecting a sqlite3.Connection object in parameter 1")
        if isinstance(cursor, sqlite3.Cursor) is not True:
            raise ValueError("@Expecting a cursor object as the sqlite3.Cursor")
        self.__Conn     = conn
        self.__Cursor   = cursor
        self.__Result   = SQLResults(self.__Conn, self.__Cursor)

    @property
    def RowCount(self):
        rowcount = 0
        if self.__Result is not None:
            rowcount = self.__Result.RowCount
        return rowcount

    @property
    def Next(self):
        row = None;
        if self.__Result is not None:
            row = self.__Result.Next
        return row;

    def Reset(self):
        if self.__Result is not None:
            self.__Result.Reset()