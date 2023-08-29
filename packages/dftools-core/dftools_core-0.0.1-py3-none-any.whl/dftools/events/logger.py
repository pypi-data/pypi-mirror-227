import logging

from dftools.events.base import EventLevel, BaseEvent
    
class DfLogger(logging.Logger):
    """
        This logger should be set as the logger class for the package 
        logging, by using the following line of code in the main method
            - logging.setLoggerClass(DfLogger)
    """
    def __init__(self, name: str, level = 0) -> None:
        super().__init__(name, level)
    
    def log_event(self, event : BaseEvent):
        self.log(event.level(), event.message())

def log_event_default(event : BaseEvent):
    lcl_logger : DfLogger = logging.getLogger('df')
    lcl_logger.log_event(event)

def log_event(logger : DfLogger, event : BaseEvent):
    if logger is not None and isinstance(type(logger), DfLogger):
        logger.log_event(event)
    else :
        log_event_default(event)

class LoggerManager():
    """
        This logger manager initializes the default logging with the custom DF classes and levels
    """
    def __init__(self, level : int = logging.DEBUG, format : str = '[%(asctime)s] [%(levelname)s] - %(message)s') -> None:
        logging.setLoggerClass(DfLogger)
        logging.basicConfig(level=level, format=format)
        logging.addLevelName(EventLevel.TEST, "TEST")
        logging.addLevelName(EventLevel.EXTENDED_INFO, "EXTENDED_INFO")
