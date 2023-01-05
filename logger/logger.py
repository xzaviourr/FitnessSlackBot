import logging

apiLogger = logging.getLogger('apiLogger')  # Log all the logs generated from API hits
apiLogger.setLevel(logging.INFO)

consoleHandler_apiLogger = logging.StreamHandler()
consoleHandler_apiLogger.setLevel(logging.INFO)

formatter_apiLogger = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s : %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")
consoleHandler_apiLogger.setFormatter(formatter_apiLogger)
apiLogger.addHandler(consoleHandler_apiLogger)


messageLogger = logging.getLogger("messageLogger")  # Log all the logs generated from sending messages
messageLogger.setLevel(logging.INFO)

consoleHandler_messageLogger = logging.StreamHandler()
consoleHandler_messageLogger.setLevel(logging.INFO)

formatter_messageLogger = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s : %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")
consoleHandler_messageLogger.setFormatter(formatter_messageLogger)
messageLogger.addHandler(consoleHandler_messageLogger)




