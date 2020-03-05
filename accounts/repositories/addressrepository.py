import datetime as dt
from accounts.repositories.repository   import Repository
from accounts.data.address              import Address
from accounts.databases.database        import Database
from accounts.databases.sqlresult       import SQLResult


class AddressRepository(Repository):

    def __init__(self, **kwargs):
        kwargs['name'] = "tbl_user_address"
        super().__init__(**kwargs)
        if (self.Database != None):
            stmt = self.Database.Execute('''CREATE TABLE IF NOT EXISTS {0} (
                                            uuid VARCHAR(50) primary key not null,
                                            user_uuid VARCHAR(50) not null,
                                            number VARCHAR(10) not null,
                                            address_type INTEGER,
                                            postcode VARCHAR(20),
                                            street TEXT ,
                                            county TEXT,
                                            country VARCHAR(100),
                                            date_registered VARCHAR(100),
                                            updated_date VARCHAR(100))'''.format(self.Name))
        self.__Addresses = None

    def Exists(self, user_uuid: str, address_uuid: str):
        status = False
        if (type(address_uuid) == str):
            if (type(user_uuid) == str):
                stmt = self.Database.Execute("SELECT *from {0} where (uuid=? and user_uuid=?) ".format(self.Name),
                                             (address_uuid, user_uuid));
                if (stmt.RowCount > 0):
                    status = True
        return status

    def Create(self, user_uuid: str, address: Address):
        result = None
        if type(user_uuid) == str:
            if (isinstance(address, Address)) and (self.Exists(user_uuid, address.UUID) is not True):
                address.UUID = self.NextUUID;
                now = dt.datetime.now();
                address.RegisteredDate = now;
                address.UpdatedDate = now;
                timestamp = str(now.timestamp());
                sql = "INSERT into {0}(uuid, user_uuid,number, address_type,postcode, street, county, country, date_registered, updated_date)values(?,?,?,?,?,?,?,?,?,?)".format(
                    self.Name);
                stmt = self.Database.Execute(sql, (
                address.UUID, user_uuid, address.Number, address.Type, address.Postcode, address.Street,
                address.County, address.Country, timestamp, timestamp));
                self.Database.Commit();
                result = address;

        return result;

    def Delete(self, user_uuid: str, address_uuid):
        address = None;
        if (type(user_uuid) == str):
            if (type(address_uuid) == str):
                address = self.Get(user_uuid, address_uuid);
                if (address != None):
                    stmt = self.Database.Execute("DELETE from {0} where (user_uuid=? AND uuid=?)".format(self.Name),
                                                 (user_uuid, address_uuid));
                    self.Database.Commit();
        return address;

    def Update(self, user_uuid: str, address: Address):
        status = False;
        user_uuid = str(user_uuid);
        if (type(user_uuid) == str):

            if (isinstance(address, Address)):
                tempaddress = self.Get(user_uuid, address.UUID);
                if (tempaddress != None):
                    update_timestamp = str(dt.datetime.now().timestamp());

                    stmt = self.Database.Execute('''UPDATE {0} set address_type=?, street=?, county=?, postcode=?, number=?, country=?, updated_date=?
                                                WHERE (user_uuid=? AND uuid=?)'''.format(self.Name),
                                                 (address.Type, address.Street, address.County,
                                                  address.Postcode, address.Number,
                                                  address.Country, update_timestamp,
                                                  user_uuid, address.UUID));
                    self.Database.Commit();
                    status = True;

        return status;

    def _ParseAddress(self, record: SQLResult):
        address = None;
        if (isinstance(record, SQLResult)):
            address = Address(uuid=record.Get("uuid"));
            address.UserID = record.Get("user_uuid");
            address.Street = record.Get("street");
            address.County = record.Get("county");
            address.Country = record.Get("country");
            address.AddressType = record.Get("address_type");
            address.Postcode = record.Get("postcode");
            address.Number = int(record.Get("number"));
        return address;

    def Get(self, users__uid: str, address_uuid=None):
        addresses = list();
        if (type(users__uid) == str):
            stmt = None;
            if (type(address_uuid) == str):
                stmt = self.Database.Execute("SELECT *from {0} where (user_uuid=? and uuid=?) ".format(self.Name),
                                             (users__uid, address_uuid));
            else:
                stmt = self.Database.Execute("SELECT *from {0} where (user_uuid=?) ".format(self.Name), (users__uid,));
            if (stmt.RowCount > 0):
                record = stmt.Next;
                while (record != None):
                    address = self._ParseAddress(record);
                    if (address != None):
                        addresses.append(address);
                    record = stmt.Next;
        return addresses;


if (__name__ == "__main__"):
    db = Database(name="../server/dbtest.db");
    respo = AddressRepository(db=db);

    address = Address(user_uid="987689098768", number=67,
                      county="Middlesex",
                      country="United Kingdom",
                      postcode="TW13 4TP",
                      street="Redford Close");

    address2 = Address(user_uid="987689098768", number=67,
                       county="Middlesex",
                       country="United Kingdom",
                       postcode="TW13 4TP",
                       street="Redford Close");

    (respo.Create("001", address));
    (respo.Create("001", address2));
    add = respo.Delete("001", address.UUID);
    address2.Street = "Ealing Street";
    address2.Country = "Nigeria";
    respo.Update("001", address2);

    adddreses = respo.Get("001");
    print(adddreses[0].Street);
    print("Address = {0}, uuid={1}".format(adddreses[0].Country, adddreses[0].UUID));

    respo.Drop();
    db.Close();
