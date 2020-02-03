
class SQLResult(object):

    def __init__(self, cursor, row):
        self.__Cursor = cursor
        self.__Row = row
        self.__Keys = self.__Row.keys()

    @property
    def Keys(self):
        return self.__Keys

    def Get(self, key):
        value = None
        if key in self.Keys:
            value = self.__Row[key]
        return value