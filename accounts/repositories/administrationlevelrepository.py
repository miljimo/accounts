import datetime as dt
import copy
from accounts.data.userlevel            import UserLevel
from accounts.data.userlevel            import AdminLevelType
from accounts.data.userlevel            import AdminLevelStatusType
from accounts.databases.database        import Database
from accounts.repositories.repository   import Repository
from accounts.databases.sqlresult       import SQLResult


class AdministratorLevelRepository(Repository):
    def __init__(self, **kwargs):
        kwargs["name"] = 'tbl_administration_level'
        super().__init__(**kwargs)
        if self.Database is not None:
            self.Database.Execute(
                "CREATE TABLE IF NOT EXISTS {0} (user_uuid text primary key, admin_level text, status int, expired_date text,"
                " date_assigned text, date_created text(20))".format(self.Name))
            self.Database.Commit()

    def Create(self, user_uuid: str, level: UserLevel) -> UserLevel:
        result = None
        if self.Exists(user_uuid) is not True:
            level.DateCreated = dt.datetime.now()
            expired = str(level.Expired.timestamp())
            assigned_date = str(level.Assigned.timestamp())
            date_created = str(level.DateCreated.timestamp())
            stmt = self.Database.Execute(
                "INSERT INTO {0} (user_uuid, admin_level,status,expired_date,date_assigned,date_created) "
                "VALUES (?,?,?,?,?,?)".format(self.Name),
                (user_uuid, level.Level, level.Status, expired, assigned_date, date_created))
            result = copy.deepcopy(level)
            self.Database.Commit()
        return result

    def ParseRecord(self, record:SQLResult):
        level:UserLevel  = None
        if record is not None:
            level:UserLevel = UserLevel(user_uuid= record.Get('user_uuid'), status= record.Get('status'))
            level.DateCreated = record.Get('date_created')
            level.Assigned    = record.Get('assigned_date')
            level.Expired     = record.Get('expired_date')
            level.Level       = record.Get('admin_level')
        return level


    def IsAdmin(self, user_uid: str) -> bool:
        status  = False
        if type(user_uid) == str:
            user_level:UserLevel = self.Get(user_uid)
            if user_level is not None:
                if(user_level.Level == AdminLevelType.SITE_ADMINISTRATION_LEVEL) or\
                            (user_level.Level == AdminLevelType.DEVELOPER_ADMINISTRATOR_LEVEL):
                    status  = True
        return status

    def Get(self, user_uuid:str) -> UserLevel:
        level: UserLevel = None

        if type(user_uuid) == str:
            stmt = self.Database.Execute("SELECT *FROM {0} WHERE (user_uuid =?)".format(self.Name), (user_uuid,))
            if stmt.RowCount > 0:
                record = stmt.Next
                level: UserLevel = self.ParseRecord(record)
        return level

    def Update(self,user_uuid:str,  user_level: UserLevel) -> bool:
        status  = False
        if (isinstance(user_level, UserLevel) is True) and (self.Exists(user_uuid) is True):

            self.Database.Execute("UPDATE {0} set (admin_level=?, assigned_date=?, status=?, expired_date=?) where (user_uuid=?)".format(self.Name),
                                  (user_level.Level, str(user_level.Assigned.timestamp()), status, str(user_level.Expired.timestamp()), user_uuid))
            self.Database.Commit()
            status  = True
        return status

    def Exists(self, user_uuid: str):
        status = False
        if type(user_uuid) == str:
            stmt = self.Database.Execute("SELECT * FROM {0} WHERE (user_uuid=?)".format(self.Name), (user_uuid,))
            if stmt is not None:
                if stmt.RowCount > 0:
                    status = True
        return status


if __name__ == "__main__":
    repo = AdministratorLevelRepository(db=Database(name="../server/dbtest.db"))

    level = UserLevel(user_uuid="9087890876", status=AdminLevelStatusType.NORMAL,
                      admin_level=AdminLevelType.DEVELOPER_ADMINISTRATOR_LEVEL)
    result = repo.Create("9087890876", level)
    print(result)

    repo.Database.Close()
