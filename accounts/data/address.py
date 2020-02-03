import datetime as dt;


class AddressType(int):
    HOME_ADDRESS    = 0x01;
    OFFICE_ADDRESS  = 0x02;


class Address(object):

    def __init__(self, **kwargs):

        self.__Number = kwargs['number'] if ('number' in kwargs) else 0;
        self.__Street = kwargs['street'] if ('street' in kwargs) else "";
        self.__County = kwargs['county'] if ('county' in kwargs) else "";
        self.__Country = kwargs['country'] if ('country' in kwargs) else "";
        self.__Postcode = kwargs['postcode'] if ('postcode' in kwargs) else "";
        self.__AddressType = kwargs['address_type'] if ('address_type' in kwargs) else AddressType.HOME_ADDRESS;
        self.__UserID = kwargs['user_uid'] if ('user_uid' in kwargs) else "";
        self.__AddressUID = kwargs['uuid'] if ('uuid' in kwargs) else None;
        self.__RegisteredDate = dt.datetime.now();
        self.__UpdatedDate = self.__RegisteredDate;

    @property
    def RegisteredDate(self):
        return self.__RegisteredDate;

    @RegisteredDate.setter
    def RegisteredDate(self, date_registered: dt.datetime):
        if isinstance(date_registered, dt.datetime):
            self.__RegisteredDate = date_registered;
        return self;

    @property
    def UpdatedDate(self):
        return self.__UpdatedDate;

    @UpdatedDate.setter
    def UpdatedDate(self, updated_date: dt.datetime):
        if isinstance(updated_date, dt.datetime):
            self.__UpdatedDate = updated_date;
        return self;

    @property
    def UUID(self):
        return self.__AddressUID;

    @UUID.setter
    def UUID(self, addressuid: str):
        if (type(addressuid) == str):
            self.__AddressUID = addressuid;
        return self;

    @property
    def UserID(self):
        return self.__UserID;

    @UserID.setter
    def UserID(self, userid: str):
        if type(userid) != str:
            raise TypeError("@UserID: expecting a string value");
        self.__UserID = userid;
        return self;

    @property
    def Type(self):
        return self.__AddressType;

    @Type.setter
    def Type(self, addresstype: AddressType):
        value = addresstype;
        if (type(addresstype) != int):
            if (isinstance(addresstype, AddressType) != True):
                raise TypeError("@AddressType: expecting an int or AddressType enum object.");
            else:
                value = addresstype.Value;
        self.__AddressType = value;
        return self;

    @property
    def Postcode(self):
        return self.__Postcode;

    @Postcode.setter
    def Postcode(self, postcode: str):
        if type(postcode) != str:
            raise TypeError("@Postcode: expecting a string value");
        self.__Postcode = postcode;
        return self;

    @property
    def Street(self):
        return self.__Street;

    @Street.setter
    def Street(self, street: str):
        if (type(street) != str):
            raise TypeError("Expecting a street to be a string value");
        self.__Street = street;
        return self;

    @property
    def County(self):
        return self.__County;

    @County.setter
    def County(self, county: str):
        if (type(county) != str):
            raise TypeError("@County: expecting a string value");
        self.__County = county;
        return self;

    @property
    def Country(self):
        return self.__Country;

    @Country.setter
    def Country(self, country: str):
        if (type(country) != str):
            raise TypeError("@Country: expecting a str value");
        self.__Country = country;
        return self;

    @property
    def Number(self):
        return self.__Number;

    @Number.setter
    def Number(self, value: int):
        if (type(value) == int):
            self.__Number = value;
        return self;

    def __eq__(self, other):
        status = False;
        if (isinstance(other, Address)):
            if ((other.UserID == self.UserID) and
                    (other.Number == self.Number) and
                    (other.Country == self.Country) and
                    (other.County == self.County) and
                    (other.Street == self.Street) and
                    (other.Postcode == self.Postcode) and
                    (other.Type == self.Type)):
                status = True;
        return status;

    def __repr__(self):
        return '''Address(uuid ={0},user_uid={1})'''.format(self.UUID, self.UserID);


if (__name__ == "__main__"):
    address = Address(uuid="001", user_uid="987689098768",
                      county="Middlesex",
                      number=891,
                      country="United Kingdom",
                      postcode="TW13 4TP",
                      street="Redford Close");

    if (address == address):
        print(address);
        pass;
