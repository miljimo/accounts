import datetime as dt;



class GenderType(int):
    MALE    = 0x00;
    FEMALE  = 0x01;

    def __init__(self, value):
        self.__Value   = value;

    @property
    def Value(self):
        return self.__Value;
    

class User(object):
    def __init__(self, **kwargs):
        self.__UUID          = kwargs['uuid'] if('uuid' in kwargs) else None;
        self.__Lastname      = kwargs['lastname'] if('lastname' in kwargs) else "";
        self.__Firstname     = kwargs['firstname'] if('firstname' in kwargs) else "";
        
        self.__EmailAddress  = kwargs['email'] if('email' in kwargs) else "";
        self.__Gender        = kwargs['gender'] if('gender' in kwargs) else GenderType.MALE;
        self.__Credential    = None;
        self.__Addresses     = dict();
        self.__DateRegistered     =  kwargs['registered_date'] if('registered_date' in kwargs) else dt.datetime.now();
        self.__LastDateUpdated    =  kwargs['last_update_date'] if('last_update_date' in kwargs) else dt.datetime.now();  
        
    @property
    def LastDateUpdated(self):
        return self.__LastDateUpdated;

    @LastDateUpdated.setter
    def LastDateUpdated(self, value):
        if(isinstance(value, dt.datetime) != True):
            raise TypeError("@LastDateUpdated : expecting a datetime object");
        self.__LastDateUpdated  =  value;
        return self;
    
    @property
    def DateRegistered(self):
        return self.__DateRegistered;

    @DateRegistered.setter
    def DateRegistered(self, value):
        if(isinstance(value, dt.datetime) != True):
            raise TypeError("@DateRegistered : expecting a datetime object");
        self.__DateRegistered  =  value;
        return self;
    
    @property
    def UUID(self):
        return self.__UUID;

    @UUID.setter
    def UUID(self, value):
        if(type(value) == str):
            self.__UUID  = value;
        return self;
    
    @property
    def Firstname(self):
        return self.__Firstname;

    @Firstname.setter
    def Firstname(self, value):
        if(type(value) == str):
            self.__Firstname  =  value;
        return self;
    
    @property
    def Gender(self):
        return self.__Gender;
    
    @Gender.setter
    def Gender(self, value):
        if(type(value) == int):
            self.__Gender  =  value;
        return self;

    @property
    def Email(self):
        return self.__EmailAddress;

    @Email.setter
    def Email(self, value):
        if(type(value) == str):
            self.__EmailAddress  =  value;
        return self;
    
    @property
    def Lastname(self):
        return self.__Lastname;

    @Lastname.setter
    def Lastname(self, value):
        if(type(value) == str):
            self.__Lastname = value;
        return self;            
    
    @property
    def Addresses(self):
        return self.__Addresses;


if(__name__ =="__main__"):
    user  =  User();
    print(user);
