import os
from flask import Flask
import threading
import json
import importlib
from flask_cors import CORS
from reporter.make_result import *
from reporter.config import config
from reporter.utils import *
from reporter.exceptions import *

# 引入的 tasks 对应的 app
import tasks

app = Flask(__name__)
handle_request_exceptions(app)
# 设置可跨域访问
CORS(app, supports_credentials=True)
api_prefix = config.data['api_server']['api_prefix']


def get_apis() -> dict:
    return {
        api_prefix: {
            "description": 'Index and description of the API',
            'method': ['GET'],
            'args': {},
            'rets': {
                'apis': "Lists of API urls and args"
            }
        }
    }


@app.route("/")
def index():
    apis = {}
    for task in tasks.get_tasks():
        logger.info(f"trying to import {task}")
        try:
            task_apis = task.get_apis()
            task_apis_modified = {}
            for api in task_apis:
                task_apis_modified[api_prefix + task.app.name + api] = task_apis[api]
            apis.update(task_apis_modified)
        except AttributeError:
            logger.warning(f'{task.app.name} has no get_apis function')

    return make_result(data={
        'description': f'HItsz-daily-reporter API v{config.data.get("version", None)}',
        'apis': apis
    })


if __name__ == '__main__':
    app.run("0.0.0.0", port=os.environ.get("PORT", 8001), debug=False)
