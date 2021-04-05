import binascii
import logging
from colorlog import ColoredFormatter
import os
import sys
import time
import datetime
import re
import traceback
from reporter.make_result import make_result


# from gbk.config import config


# 时间单位默认为毫秒，但是末尾请使用000
# 时间被更新为最近下一次的时间
def fmt_time(time_stamp) -> int:
    return int(time_stamp / 1000) * 1000


def get_logger(name=__name__):
    logger_base = logging.getLogger(name)
    logger_base.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    color_formatter = ColoredFormatter('%(log_color)s[%(module)-15s][%(funcName)-15s][%(levelname)-7s] %(message)s')
    stream_handler.setFormatter(color_formatter)
    logger_base.addHandler(stream_handler)
    return logger_base


logger = get_logger(__name__)


def restart_program(timeout=3):
    time.sleep(timeout)
    python = sys.executable
    os.execl(python, python, *sys.argv)


def get_request_json(req):
    js = req.json
    return js


def get_date_timestamp(date) -> int:
    return int(datetime.datetime.timestamp(datetime.datetime.fromisoformat(date)) * 1000)


def get_timestamp_date(timestamp) -> str:
    return datetime.datetime.fromtimestamp(timestamp / 1000).isoformat()[:10]


# YYYY-MM-DD 格式
def get_date_today() -> str:
    return get_timestamp_date(datetime.datetime.today().timestamp() * 1000)


def get_traceback():
    traceback.print_exc()  # 打印异常信息
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error = str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))  # 将异常信息转为字符串
    return error


def handle_request_exceptions(app):
    # 统一错误处理信息
    @app.errorhandler(404)
    def handler_404(error):
        logger.error(f"{error}")
        return make_result(404, message=str(error))

    # 统一错误处理信息
    @app.errorhandler(500)
    def handler_500(error):
        logger.error(f"{error}")
        return make_result(500, message=str(error))
