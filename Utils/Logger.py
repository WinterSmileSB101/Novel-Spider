import logging.handlers


class Logger:
    __LOG_FILE__ = "r'logs/insert.log'"
    __LOG_FMT__ = "%(asctime)s - %(levelname)s - %(message)s"

    @classmethod
    def get_info_logger(self, logfilepath: str=r'../logs', name: str="log", fmts: str = "%(asctime)s - [ %(levelname)s ] - [ %(message)s ]"):
        logfilepath = logfilepath+"/"+name+".log"
        handler = logging.handlers.RotatingFileHandler(logfilepath, maxBytes=1024*1024,backupCount=5,encoding='UTF-8')
        formatter = logging.Formatter(fmts)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
