class ErrorType(int):
    NORMAL:                                 int = 0x1000
    USER_ALREADY_EXISTS_ERROR:              int = 0x1001
    VALIDATION_ERROR:                       int = 0x1002
    UNABLE_TO_CREATE_USER_ERROR:            int = 0x1003
    UNABLE_TO_CREATE_CREDENTIAL_ERROR:      int = 0x1004
    INVALID_DATE :                          int = 0x1005
    UNABLE_ASSIGNED_ADMINISTRATOR_ERROR:    int = 0x1006
    NOT_ACCESS_ERROR:                       int = 0x1007
    ACCOUNT_NOT_ACTIVATED:                  int = 0x1008
    NOT_FOUND:                              int = 0x1009
    ACTIVATED_ALREADY:                      int = 0x100A
    UPDATE_FAIL:                            int = 0x100B
    USER_ACCOUNT_BLOCKED:                   int = 0x100C
    ACCOUNT_BLOCK_ACTIVATED:                int = 0x100D
    INVALID_CREDENTIAL_PROVIDED:            int = 0x100E
    UNABLE_TO_UPDATE_RECORD :               int = 0x100F
