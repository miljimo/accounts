
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