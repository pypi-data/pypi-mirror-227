# # Utilitarios generales
# # Creado por: Totem Bear
# # Fecha: 23-Ago-2023

# # ****************************************************************
# # *********** Manage the logs ***********

import logging


# Dictionary to manage the log levels
logLevels = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50,
    'notset': 0,
    'debug': 10,
    'info': 20,
    'warning': 30,
    'error': 40,
    'critical': 50
}

# Get the logger - general
logger = logging.getLogger('logGeneral')
# Configure the logger for the "general" log file
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(logger)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# To use logger in the application - function printLogger or:
# utils.logger.debug('Este es un mensaje de registro de nivel DEBUG')
# utils.logger.info('Este es un mensaje de registro de nivel INFO')
# utils.logger.warning('Este es un mensaje de registro de nivel WARNING')
# utils.logger.error('Este es un mensaje de registro de nivel ERROR')
# utils.logger.critical('Este es un mensaje de registro de nivel CRITICAL')


# Print the msg into the logger file "logFileStr" by level and encrypt
def printLog(logFileStr: str, msg: str, level: str):
    # TODO: remove this print
    print(f"***** printLog: logFileStr={logFileStr} - msg={msg}")
    if logFileStr == 'general':
        logFile = logger
    else:
        logFile = logger

    logFile.log(logLevels[level], msg)
