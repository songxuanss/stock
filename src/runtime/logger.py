import logging
from logging import handlers


class Logger:
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    _logger_lvl = 'error'
    _logger_format_str = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    _logger_rotate_cycle = 'D'
    _logger = None

    def __init__(self):
        raise NotImplementedError("the Logger class is singleton, cannot be instantiated")

    @classmethod
    def get_logger(cls, logger_name):
        _logger = logging.getLogger(logger_name)
        _logger.setLevel(cls.level_relations.get(cls._logger_lvl))
        format_str = logging.Formatter(cls._logger_format_str)
        sh = logging.StreamHandler()
        th = handlers.TimedRotatingFileHandler(filename=logger_name, when=cls._logger_rotate_cycle, backupCount=3,
                                               encoding='utf-8')
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        _logger.addHandler(sh)  # 把对象加到logger里
        _logger.addHandler(th)
        return _logger

