import os
from reporter.utils import logger
from reporter.config import config
from reporter.server_api import app as app_api
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# 导入apps
import tasks
apps = tasks.get_apps()
apps_path = {}
for a in apps:
    try:
        apps_path[config.data[a.name]['api_prefix']] = a
    except KeyError:
        logger.error(f'Cannot parse module {a}')
# 中间件
app = DispatcherMiddleware(app_api, apps_path)

if __name__ == '__main__':
    run_simple('0.0.0.0', int(os.environ.get("PORT", '8081')), app, use_reloader=False)
