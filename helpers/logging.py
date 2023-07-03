import structlog
import logging
import datetime
import os
import pytz


def get_logger(loggerName):
    LOG_LEVEL = logging.INFO
    # Get the current date and time
    now = datetime.datetime.now(pytz.utc)

    # Format the date and time as strings
    date = now.strftime("%Y-%m-%d")  # This will format the date as 'YYYY-MM-DD'
    time = now.strftime("%H:%M:%S")  # This will format the time as 'HH-MM-SS'

    log_directory = f"logs/{loggerName}/{date}"
    file_name = f"{time}.log"

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, file_name)

    SHARED_PROCESSORS = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        # structlog.processors.format_exc_info,  # NOTE: Comment out this line for prettier, but more detailed, exception printing
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.THREAD,
                structlog.processors.CallsiteParameter.THREAD_NAME,
            ]
        ),
    ]

    structlog.configure(
        processors=SHARED_PROCESSORS
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=SHARED_PROCESSORS,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(),
        ],
    )

    root_logger = logging.getLogger()

    console_handler_exists = any(
        isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers
    )

    if not console_handler_exists:
        handler = logging.StreamHandler()
        # Use OUR `ProcessorFormatter` to format all `logging` entries.
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        root_logger.setLevel(LOG_LEVEL)

    handler_json = logging.FileHandler(str(log_file_path))  # Convert to string
    handler_json.setFormatter(logging.Formatter("%(message)s"))
    handler_json.setLevel(LOG_LEVEL)
    root_logger.addHandler(handler_json)

    return structlog.get_logger(loggerName)
