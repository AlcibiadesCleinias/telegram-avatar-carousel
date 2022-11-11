from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1: str = '/api/v1'
    LOG_LEVEL: str = 'INFO'
    LOGGER_NAME: str = 'app_logger'

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379

    TG_API_HASH: str = "foofoofoofoofoo"
    TG_API_KEY: int = 999
    TG_API_PHONE: str = "+90...77"
    # TODO: there is a problem if I ended name with numbers for redis...
    TG_SESSION: str = 'session'
    ROTATE_AVATAR_TASK_CORO: str = "*/30 * * * *"
    DATA_AVATARS: str = "./data_avatars"
    TASK_RANDOM_DELAY_PERIOD: str = 30

    class Config:
        case_sensitive = True


settings = Settings()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        'root': {
            'handlers': ['default'],
            'level': settings.LOG_LEVEL,
        },
        settings.LOGGER_NAME: {
            'handlers': ['default'],
            'level': settings.LOG_LEVEL,
            "propagate": "false",
        },
    },
}
