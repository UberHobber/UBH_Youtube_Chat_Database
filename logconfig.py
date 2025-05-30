"""
Pre-made file for initializing logging functionality.
"""
# Import of main package files
import logging,time,atexit,datetime

# Import specific items from a package
from typing import List

# Import custom Python stuff
from Settings import DEBUG,DEBUG_LOG_FILE,LOG_VERBOSE,LOG_NAME


class ConsoleFormatter(logging.Formatter):
    '''Formats the console outputs based on what type of log object they are'''
    grey_light = "\x1b[28;30m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    crit_fmt = 'CRTICAL: %(message)s (%(filename)s:%(lineno)d)'
    err_fmt = 'ERROR: %(message)s (%(filename)s:%(lineno)d)'
    warn_fmt = 'WARN: %(message)s (%(filename)s:%(lineno)d)'
    dbg_fmt = 'DEBUG: %(message)s (%(filename)s:%(lineno)d)'
    info_fmt = '%(message)s'
    format = "%(message)s"

    FORMATS = {
        logging.DEBUG: grey_light + dbg_fmt + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + warn_fmt + reset,
        logging.ERROR: red + err_fmt + reset,
        logging.CRITICAL: bold_red + crit_fmt + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
class LogFormatter(logging.Formatter):
    '''Formats the log file outputs based on what type of log object they are'''
    crit_fmt = 'CRTICAL: %(message)s'
    err_fmt = 'ERROR: %(message)s'
    warn_fmt = 'WARN: %(message)s'
    dbg_fmt = 'DEBUG: %(message)s'
    info_fmt = '%(message)s'

    FORMATS = {
        logging.CRITICAL: crit_fmt,
        logging.ERROR: err_fmt,
        logging.WARNING: warn_fmt,
        logging.DEBUG: dbg_fmt,
        logging.INFO: info_fmt
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class Summary:
    """
    Object to store summary information to place all at once in a log file later.
    """
    def __init__(self):
        self.lines: List[str] = []
        self.lines.append('') # Append blank line to create a spacer from the data above

    def add(self,line: str):
        """
        Add an entry to the Summary Object

        :param line: Given line to store
        :type line: String
        """
        self.lines.append(line)

logger = logging.getLogger('Larry')
logger.setLevel(logging.DEBUG)

def TimeCurrent():
    """Get the current time at moment of function call
    
    :return: Hours:Minutes:Seconds
    :rtype: String
    """
    return f'{time.strftime('%H:%M:%S')}'

def TimeDurration():
    """Gets the start time of the program and calculates how long it's been at moment of function call.
    
    :return: Time elapsed since start of program, in seconds.
    :rtype: String"""
    time_current = time.time()
    time_duration = time_current-time_start
    time_duration = int(round(time_duration,0))
    time_duration = str(datetime.timedelta(seconds=time_duration))
    return time_duration

def FullTimestamp():
    """Formatted combination of both Current Time and Time Elapsed.
    
    :return: {Hours:Minutes:Seconds}, {Seconds} elapsed
    :rtype: String"""
    return f'{TimeCurrent()}, {TimeDurration()} elapsed'

def ProgramComplete():
    """
    Executes at the end of the program, on exit.
    """
    logger.info(f'\n*--------------------*\nPROGRAM COMPLETE AT {TimeCurrent()}\nEXECUTION DURATION: {TimeDurration()}\n*--------------------*\n')

def StreamLog():
    """
    The Log Handler for the console output. Control log level with LOG_VERBOSE
    """
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO) if LOG_VERBOSE == False else ch.setLevel(logging.DEBUG)
    ch.setFormatter(ConsoleFormatter())
    logger.addHandler(ch)

def FileLog(debug_filename='debug',log_filename='log'):
    """
    The Log Handler for the file output. Control log level with LOG_VERBOSE.

    :param debug_filename: Name of the debug log file
    :type debug_filename: String
    :param log_filename: Prefix of the main log file
    :type log_filename: String
    """
    if DEBUG == False:
        fh = logging.FileHandler(f'{log_filename} ({time.strftime('%Y.%m.%d-%H.%M.%S')}).log',encoding='utf-8')
    else:
        fh = logging.FileHandler(f'{debug_filename}.log',encoding='utf-8')
    fh.setLevel(logging.INFO) if LOG_VERBOSE == False else fh.setLevel(logging.DEBUG)
    fh.setFormatter(LogFormatter())
    logger.addHandler(fh)

StreamLog()
#Uncomment FileLog() to enable outputting log information to a file
FileLog(DEBUG_LOG_FILE,LOG_NAME)

time_start = time.time()
time_epoch = int(round(time_start,0))

logger.info(f'CURRENT TIME OF EXECUTION:\n{TimeCurrent()}\n----------------------')

# Will run TimeDuration function when the program finishes
atexit.register(ProgramComplete)