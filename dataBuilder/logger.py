import logging, os
from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv('DEBUG_LEVEL', 'PROD')
file = os.getenv('LOG_FILE', 'N')

TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")
def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)
logging.Logger.trace = trace

log_levels = {
    "TRACE": TRACE_LEVEL,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}
if log_level == 'PROD':
    debug_level = log_levels.get('INFO', logging.INFO)
elif log_level == 'TESTING':
    debug_level = log_levels.get('TRACE', logging.DEBUG)
else:
    debug_level = log_levels.get(log_level, logging.INFO)

logger = logging.getLogger('chess_vs_checkers')
logger.setLevel(debug_level)

console_handler = logging.StreamHandler()
console_handler.setLevel(debug_level)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

if file != 'N':
    log_dir = os.path.dirname('/output/app.log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_handler = logging.FileHandler('/output/app.log')
    file_handler.setLevel(debug_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(f"Starting file transmission in {'app.log'}")
else:
    logger.debug("log file not running")
def is_testing():
    """
    Function for debugging that tells you if the DEBUG_LEVEL is TESTING or not
    """
    if os.getenv("DEBUG_LEVEL") == 'TESTING':
        return True
    else:
        return False

if debug_level == logging.INFO and log_level != "INFO":
    if log_level == 'PROD':
        pass
    else:
        logger.warning(f'Invalid DEBUG_LEVEL "{log_level}" using INFO instead.')
logger.info('logger started')