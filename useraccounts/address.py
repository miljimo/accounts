class AddressType(int):
    HOME_ADDRESS    =  0x01;
    OFFICE_ADDRESS  =  0x02;
    

class Address(object):

    def __init__(self, **kwargs):
        self.__Number       =  None;
        self.__Street       =  None;
        self.__County       =  None;
        self.__Country      =  None;
        self.__LocalGovt    =  None;
        self.__AddressType  =  AddressType.HOME_ADDRESS;
        
    @property
    def Number(self):
        return self.__Number;
    
    @Number.setter
    def Number(self, value: int):
        if(type(value) == int):
            self.__Number  =  value;
        return self;

