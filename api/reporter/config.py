import os
import json
import threading
from reporter.utils import logger


# debug开关:
# 1. 使用默认配置
# 2. #配置文件保持最新
# 3. 不读写配置文件


class Config:
    FILE_NAME = "hitsz-daily-reporter.json"
    FILE_PATH = '.'
    # DES 加密秘钥
    KEY = '_chiro#*'
    AUTH_API = ''

    def __init__(self):
        self.data_default = {
            "debug": True,
            "version": 0.1,
            "epidemic-report-version": 0.1,
            "api_server": {
                "upgradable": True,
                "api_prefix": "/"
            },
            "epidemic-report": {
                "upgradable": True,
                "api_prefix": "/epidemic"
            },
            # 'postgresql': os.environ.get()
        }
        self.data = self.data_default
        self.lock = threading.RLock()
        self.load()

    def load_data(self):
        pass

    def load(self):
        if self.data_default['debug']:
            self.data = self.data_default
            self.load_data()
            logger.debug(f'config load from default data and got data: {self.data}')
        else:
            try:
                with open(os.path.join(Config.FILE_PATH, Config.FILE_NAME), "r") as f:
                    data = json.load(f)
                    # 如果在程序中设置了debug模式就直接替换文件
                    if self.data_default['debug']:
                        self.data = self.data_default
                        self.load_data()
                    else:
                        for k in data:
                            self.data[k] = data[k]
                        # 检查文件是否需要和做版本更新，用default更新内容
                        for k in self.data_default:
                            if k not in self.data:
                                self.data[k] = self.data_default[k]
                                continue
                            if data['version'] < self.data_default['version']:
                                # 在版本更新时候才会更新dict内的upgradable项
                                if type(self.data_default[k]) is dict and 'upgradable' in self.data_default[k]:
                                    self.data[k] = self.data_default[k]
                            # 不含upgradable就直接更新
                            if not (type(self.data_default[k]) is dict and 'upgradable' in self.data_default[k]):
                                self.data[k] = self.data_default[k]
            except KeyError:
                logger.error("Err loading, KeyError.")
                self.data = self.data_default
            except json.decoder.JSONDecodeError:
                logger.error("Err loading, DecodeError.")
                self.data = self.data_default
            except FileNotFoundError:
                logger.info("Using default loader")
                self.data = self.data_default
            finally:
                self.load_data()
                logger.debug(
                    f'config load from: {os.path.abspath(os.path.join(Config.FILE_PATH, Config.FILE_NAME))} got data: {self.data}')
                self.save()

    def save(self):
        with open(os.path.join(Config.FILE_PATH, Config.FILE_NAME), "w") as f:
            json.dump(self.data, f)
        logger.debug(
            f'config saved to:  {os.path.abspath(os.path.join(Config.FILE_PATH, Config.FILE_NAME))} and data: {self.data}')


config = Config()
