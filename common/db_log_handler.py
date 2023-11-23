import logging

DJANGO_DB_LOGGER_ENABLE_FORMATTER = True

db_default_formatter = logging.Formatter()


def log_error(exc, code):
    db_logger = logging.getLogger('db')
    db_logger = logging.LoggerAdapter(db_logger, {'error': code, 'method': 'get'})
    db_logger.exception(exc)


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        from .models import CustomLog

        trace = None

        if record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)

        if DJANGO_DB_LOGGER_ENABLE_FORMATTER:
            msg = self.format(record)
        else:
            msg = record.getMessage()

        kwargs = {
            'error': record.error,
            'level': record.levelno,
            'msg': msg,
            'trace': trace,
            'method': record.method
        }

        CustomLog.objects.create(**kwargs)

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = db_default_formatter

        if type(fmt) == logging.Formatter:
            record.message = record.getMessage()

            if fmt.usesTime():
                record.asctime = fmt.formatTime(record, fmt.datefmt)

            # ignore exception traceback and stack info

            return fmt.formatMessage(record)
        else:
            return fmt.format(record)
