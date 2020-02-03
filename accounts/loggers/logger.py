import logging
import os


class BaseLogger(object):
    __Instance  =  None

    def __new__(cls, *args, **kwargs):
        if cls.__Instance  is None:
            cls.__Instance  = object.__new__(cls)
        return cls.__Instance

    def __init__(self, **kwargs):
        filename = kwargs['filename'] if ('filename' in kwargs) else None
        if filename is None:
            filename  = "../../logs/default.log"
        if os.path.isfile(filename) is not True:
            file = open(filename, 'w+')
            file.close()
        logging.basicConfig(filename=filename, format='%(asctime)s  %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

    def Warning(self, message: str) -> None:
        logging.warning(message)

    def Debug(self, message: str):
        logging.debug(message)

    def Info(self, message: str) -> None:
        logging.info(message)

    def Error(self, message:str)-> None:
        logging.error(message)




if __name__ == "__main__":
    logger  =  BaseLogger(filename="test.log")
    logger.Info("Started.")
    print("done")
