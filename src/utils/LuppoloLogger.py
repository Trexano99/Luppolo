import logging
import os

class LuppoloLogger(logging.Logger):
    '''
    The LuppoloLogger class is a custom logger that extends the logging.Logger class.
    It is used to log messages to the console and to a file.
    For default it has some basic configurations, but it can be customized through the setCustomLogger method.
    '''
    __DEFAULT_LOG_FILE_PATH = '../data/luppolo.log'
    __logger = None

    def __init__(self, name, level=logging.NOTSET, logFile = __DEFAULT_LOG_FILE_PATH):
        '''
        The constructor of the LuppoloLogger class. 
        It initializes the logger with the given name and level. 
        The logger process is configured to log messages to the console and to a file, 
        located at the path specified by the __DEFAULT_LOG_FILE_PATH attribute.
        '''
        super().__init__(name, level)
        self.setLevel(level)
        self.__createLuppoloLogFile(logFile)

        # File handler
        file_handler = logging.FileHandler(logFile)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        console_handler.setLevel(level)
        self.addHandler(console_handler)

        print("Luppolo logger initialized. Logging level " + logging.getLevelName(level)+" in file: "+logFile)


    def __createLuppoloLogFile(self, logFilePath):
        ''' 
        This method creates the log file if it does not exist. 
        This method also ensure that the data directory exists and creates it if it does not exist.
        '''
        log_dir = os.path.dirname(logFilePath)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        with open(logFilePath, 'w+') as log_file:
            log_file.write('')

    @staticmethod
    def getLogger():
        ''' This method returns the logger. '''
        return LuppoloLogger.__logger

    @staticmethod
    def setCustomLogger(logger):
        ''' This method sets a custom logger for the LuppoloLogger class. '''
        LuppoloLogger.__logger = logger

    @staticmethod
    def logInfo(message):
        ''' This method logs an info message. '''
        LuppoloLogger.__log(message, logging.INFO)

    @staticmethod
    def logDebug(message):
        ''' This method logs a debug message. '''
        LuppoloLogger.__log(message, logging.DEBUG)

    @staticmethod
    def logWarning(message):
        ''' This method logs a warning message. '''
        LuppoloLogger.__log(message, logging.WARNING)

    @staticmethod
    def logError(message):
        ''' This method logs an error message. '''
        LuppoloLogger.__log(message, logging.ERROR)

    @staticmethod
    def __log(message, level=logging.NOTSET):
        if LuppoloLogger.__logger is None:
            LuppoloLogger.__logger = LuppoloLogger('LuppoloLogger', logging.DEBUG)
        if LuppoloLogger.__logger.isEnabledFor(level):
            LuppoloLogger.__logger.log(level, message)
    
    @staticmethod
    def getLoggingLevelFromString(loggingLvlStr):
        ''' This method returns the logging level from a string. '''
        return {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }[loggingLvlStr]
