LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'large': {
            'format': '%(asctime)s  %(levelname)s  %(funcName)s    %(message)s  '
        },
        'tiny': {
            'format': '%(asctime)s  %(message)s  '
        }
    },
    'handlers': {
        'db_log': {
            'level': 'ERROR',
            'formatter': 'large',
            'class': 'common.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        },
    },
}